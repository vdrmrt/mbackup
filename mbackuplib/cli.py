"""Command-line interface for mbackup."""

import argparse
import logging
import logging.handlers
import os
import shlex
import shutil
import subprocess
import sys

import mbackuplib


def readBackupList(listFile):
    """Read the configured list of locations to back up."""
    backupTypes = ['rdiff-backup', 'rsync']
    backupList = []
    lineCounter = 0
    for line in listFile:
        lineCounter += 1
        if not line.startswith('#'):
            bItem = shlex.split(line.rstrip())
            if bItem[0] in backupTypes:
                backupList.append(bItem)
            else:
                raise ValueError('Invalid backup type in {f} '
                                 'on line {c} for {b}'
                                 .format(f=listFile.name,
                                         c=lineCounter,
                                         b=bItem[1]))
    listFile.close()
    return backupList


def parsArguments():
    """Set up argparse to handle the CLI arguments."""
    description = ('mbackup is a Python application to create '
                   'backups with rdiff-backup and rsync.')
    epilog = '''
mbackup reads a file with the locations to back up.
If no file is supplied with -l, mbackup will look for .mbackup-list in
the user's home directory. If run as root, mbackup will look in
/etc/mbackup-list.

The file format used to list the directories to back up is one line per
backup location. Each line contains two or three parameters separated by
whitespace:

* the backup type, rdiff-backup or rsync
* the directory to back up
* the target directory, which is optional. Relative paths are appended
  to the global target path

Lines starting with a # are ignored. Directories with whitespace need
to be wrapped in double quotes.
For example:
# Backup list for mbackup
# type[rdiff-backup | rsync] directory target
rdiff-backup /home/user/documents /backups/documents
rsync /mnt/archive_1
rsync "/mnt/archive 2" backups/archive

Options -i and -m are ignored for rsync backups.
'''

    parser = argparse.ArgumentParser(
                prog='mbackup',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description=description,
                epilog=epilog
                )

    if os.geteuid() == 0:
        defaultBackupList = '/etc/mbackup-list'
        defaultLogFile = '/var/log/mbackup.log'
    else:
        defaultBackupList = os.path.expanduser("~") + '/.mbackup-list'
        defaultLogFile = os.path.expanduser("~") + '/.mbackup.log'

    parser.add_argument('-d', action='store_true', default=False,
                        help='do a dummy run')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='enable debugging output')
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
    parser.add_argument('-m', action='store', default=False,
                        metavar='time',
                        help='how long to keep increments for '
                             'rdiff-backups')
    parser.add_argument('-v', action='store_true', default=False,
                        help='enable verbose output')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {v}'.format(v=mbackuplib.__version__),
                        help='show version and exit')
    parser.add_argument('-w', action='store_true', default=False,
                        help='wait on user input to start the backup')
    parser.add_argument('t', action='store', default=False,
                        metavar='target-dir',
                        help='directory to store the backups')

    return parser.parse_args()


def createLogger(logFile, debug=False):
    """Create and configure the application logger."""
    logger = logging.getLogger()
    logger.handlers.clear()

    consoleFormatter = logging.Formatter('%(message)s')
    fileFormatter = logging.Formatter(
                        '%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S')
    fileHandler = logging.handlers.RotatingFileHandler(
                    logFile, encoding='utf8',
                    maxBytes=100000, backupCount=2)
    streamHandler = logging.StreamHandler()

    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    fileHandler.setFormatter(fileFormatter)
    streamHandler.setFormatter(consoleFormatter)

    return logger


def logDebugList(backupList):
    """Send the backup list to the debug logger."""
    logger = logging.getLogger()
    for line in backupList:
        s = ''
        for item in line:
            s += item + ' '
        logger.debug('{s}'.format(s=s))


def getBackupExecutable(backupType):
    """Return the executable name for the selected backup type."""
    executables = {
        'rdiff-backup': 'rdiff-backup',
        'rsync': 'rsync',
    }
    try:
        return executables[backupType]
    except KeyError as exc:
        raise mbackuplib.MbackupError(
            'Unknown backup type {t}'.format(t=backupType)
        ) from exc


def checkLocalExecutable(executable):
    """Verify that the required local executable is available."""
    if shutil.which(executable) is None:
        raise mbackuplib.MbackupError(
            'Required executable {e} was not found on this system'
            .format(e=executable)
        )


def checkRemoteExecutable(host, user, executable):
    """Verify that the required executable exists on the remote host."""
    remote = host if not user else '{u}@{h}'.format(u=user, h=host)
    command = [
        'ssh',
        remote,
        'command -v {e} >/dev/null 2>&1'.format(e=shlex.quote(executable)),
    ]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip()
        if details:
            raise mbackuplib.MbackupError(
                'Required executable {e} was not found on remote host {h}: {d}'
                .format(e=executable, h=remote, d=details)
            )
        raise mbackuplib.MbackupError(
            'Required executable {e} was not found on remote host {h}'
            .format(e=executable, h=remote)
        )


def runPreflightChecks(backupType, host=False, user=False,
                       verifiedLocal=None, verifiedRemote=None):
    """Verify backend executables before starting a backup job."""
    executable = getBackupExecutable(backupType)
    verifiedLocal = set() if verifiedLocal is None else verifiedLocal
    verifiedRemote = set() if verifiedRemote is None else verifiedRemote

    if executable not in verifiedLocal:
        checkLocalExecutable(executable)
        verifiedLocal.add(executable)

    if host:
        if 'ssh' not in verifiedLocal:
            checkLocalExecutable('ssh')
            verifiedLocal.add('ssh')

        remoteKey = (host, user, executable)
        if remoteKey not in verifiedRemote:
            checkRemoteExecutable(host, user, executable)
            verifiedRemote.add(remoteKey)


def main():
    """Run the mbackup command-line interface."""
    args = parsArguments()

    logger = createLogger(args.log, args.debug)
    verifiedLocal = set()
    verifiedRemote = set()

    rdiffbackupVerbosityLevel = 5 if args.v else 3

    if args.d:
        logger.debug('dummy run enabled')
    logger.debug('backup list set to {f}'.format(f=args.l.name))
    logger.debug('log file set to {f}'.format(f=args.log))
    logger.debug('target backup directory set to {f}'.format(f=args.t))

    logger.debug('Backup list')
    logger.debug('type[rdiff-backup | rsync] directory target_dir')
    backupList = readBackupList(args.l)
    logDebugList(backupList)

    if args.w:
        input("Press Enter to start the backups...")

    if args.d:
        logger.info('Doing a dummy run')

    for backupItem in backupList:
        try:
            backupType = backupItem[0]
            logger.debug('Starting new {t} backup:'
                         .format(t=backupType))
            source = backupItem[1]
            logger.debug('Source set to: {b}'.format(b=backupItem[1]))
            runPreflightChecks(
                backupType,
                host=args.host,
                user=args.user,
                verifiedLocal=verifiedLocal,
                verifiedRemote=verifiedRemote,
            )

            try:
                target = backupItem[2]
            except IndexError:
                target = source.lstrip('/')

            if os.path.isabs(target):
                dest = target.rstrip('/')
            else:
                dest = os.path.join(args.t, target.rstrip('/'))

            logger.debug('Destination set to: {d}'.format(d=dest))

            logger.info('Starting {t} of {s}'
                        .format(t=backupType, s=source))
            if backupType == 'rdiff-backup':
                ba = mbackuplib.Rdiffbackup(
                        source=source,
                        dest=dest,
                        verbosity=rdiffbackupVerbosityLevel)
            elif backupType == 'rsync':
                ba = mbackuplib.Rsyncbackup(
                        source=source,
                        dest=dest,
                        verbosity=args.v)
            else:
                logger.error('Unkown backup type')
                rc == 1

            if args.host:
                ba.setHost(args.host)
            if args.user:
                ba.setUser(args.user)

            rc = ba.backup() if not args.d else 0

            if rc == 0:
                logger.info('\033[1;32m{t} of {s} successfull\033[1;m'
                            .format(t=backupType, s=source))
                if backupType == 'rdiff-backup':
                    if args.m:
                        logger.info('Deleting increments '
                                    'older than {m}'.format(m=args.m))
                        if not args.d:
                            ba.remove(args.m)
                    if args.i:
                        logger.info('Listing increments')
                        if not args.d:
                            ba.listIncrementSizes()
            else:
                logger.error('\033[1;31m {t} of {s} failed\033[1;m'
                             .format(t=backupType, s=source))

            logger.info('')
        except mbackuplib.MbackupError as inst:
            logger.error('{t}: {m}'.format(t=type(inst).__name__,
                                           m=inst))

    if args.w:
        input("Backup has finished press Enter to continue...")


if __name__ == '__main__':
    sys.exit(main())
