#!/usr/bin/env python3

import argparse
import shlex
import os
import sys
import logging
import logging.handlers

import backupapps

def readBackupList(listFile):
    backupTypes = ['rdiff-backup','rsync']
    backupList = []
    lineCounter = 0
    for line in listFile:
        lineCounter+=1
        if not line.startswith('#'):
            bItem = shlex.split(line.rstrip())
            if bItem[1] in backupTypes:
                backupList.append(bItem)
            else:
                raise ValueError('Invalid backup type in {f} '
                                 'on line {c} for {b}'
                                 .format(f=listFile.name,
                                         c=lineCounter,
                                         b=bItem[0]))
    listFile.close()
    return backupList

def parsArguments():
    parser = argparse.ArgumentParser(
                prog='mbackup',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='mbackup tool to create backups with'
                            'rdiff-backup and rsync.',
                epilog='''
The file format used to list the directories to backup is one line per
backup location. Each line contains two parameters separated with a
white space (space or tab): the directory to backup and the type of
backup (rdiff-backup or rsync). Lines starting with a # are ignored.
Directories with whitespace need to be wrapped in double quotes.
For example:
# Backup list for mbackup
# directory type[rdiff-backup | rsync]
/home/user/documents rdiff-backup
/mnt/archive_1 rsync
"/mnt/archive 2" rsync

Options -i and -m are ignored for rsync backups.
''')

    if os.geteuid() == 0:
        defaultBackupList = '/etc/mbackup-list'
        defaultLogFile = '/var/log/mbackup.log'
    else:
        defaultBackupList = os.path.expanduser("~") + '/.mbackup-list'
        defaultLogFile = os.path.expanduser("~") + '/.mbackup.log'

    parser.add_argument('-d', action='store_true', default=False,
                        help='do a dummy run')
    parser.add_argument('-i', action='store_true', default=False,
                        help='for rdiff-backup show previous '
                             'increments')
    parser.add_argument('--host', action='store', default=False,
                        help='ssh host to backup to')
    parser.add_argument('--user', action='store', default=False,
                        help='ssh user to login to backup host')
    parser.add_argument('-l', action='store',
                        type=argparse.FileType('r'),
                        default=defaultBackupList,
                        metavar='file',
                        help='file path of list of directories '
                             'to backup')
    parser.add_argument('--log', action='store',
                        default=defaultLogFile,
                        help='set log file')
    parser.add_argument('-m',action='store', default=False,
                        metavar='time',
                        help='how long to keep increments for '
                             'rdiff-backups')
    parser.add_argument('-v', action='store_true',default=False,
                        help='enable verbose output')
    parser.add_argument('-w', action='store_true', default=False,
                        help='wait on user input to start the backup')
    parser.add_argument('t', action='store',default=False,
                        metavar='target-dir',
                        help='directory to store the backups')

    return parser.parse_args()

def createLogger(logFile,verbose = False):
    logger = logging.getLogger() #Get root logger

    consoleFormatter = logging.Formatter('%(message)s')
    fileFormatter = logging.Formatter(
                        '%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S')
    fileHandler = logging.handlers.RotatingFileHandler(
                    logFile,encoding='utf8',
                    maxBytes=100000, backupCount=2)
    streamHandler = logging.StreamHandler()

    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    fileHandler.setFormatter(fileFormatter)
    streamHandler.setFormatter(consoleFormatter)

    return logger

def main():
    args = parsArguments()

    logger = createLogger(args.log)

    rdiffbackupVerbosityLevel = 5 if args.v else 3

    if args.d: logger.debug('dummy run enabled')
    logger.debug('backup list set to {f}'.format(f=args.l.name))
    logger.debug('log file set to {f}'.format(f=args.log))
    logger.debug('target backup directory set to {f}'.format(f=args.t))

    backupList = readBackupList(args.l)

    if args.w : input("Press Enter to start the backups...")

    if args.d : logger.info('Doing a dummy run')

    for backupItem in backupList:
        try:
            source = backupItem[0]
            dest = os.path.join(args.t,backupItem[0].strip('/'))
            logger.info('{t} of {s}'.format(t=backupItem[1],s=source))
            if backupItem[1] =='rdiff-backup':
                rdb = backupapps.Rdiffbackup(
                        source=source,
                        dest=dest,
                        verbosity=rdiffbackupVerbosityLevel)
                if args.host: rdb.setHost(args.host)
                if args.user: rdb.setUser(args.user)
                rc = rdb.backup() if not args.d else 0

                if rc == 0:
                    logger.info('\033[1;32m[OK]\033[1;m') #Green OK

                    if args.m:
                        logger.info('Deleting increments'
                                    'older than {m}'.format(m=args.m))
                        if not args.d: rdb.remove(args.m)

                    logger.info('Listing increments')
                    if not args.d: rdb.listIncrementSizes()
                else:
                    logger.error('\033[1;31m[FAIL]\033[1;m') #Red FAIL
            elif backupItem[1] =='rsync':
                None
                #todo
            logger.info('')
        except backupapps.BackupAppError as inst:
            logger.error('{t}: {m}'.format(t=type(inst).__name__,
                                    m=inst))

    if args.w : input("Backup has finished press Enter to continue...")


if __name__ == '__main__':
    sys.exit(main())
