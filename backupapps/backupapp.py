from abc import ABCMeta, abstractmethod, abstractproperty

import queue
import os,sys
import shutil
import subprocess
from threading import Thread
import logging
import errno
import paramiko

class BackupApp(metaclass=ABCMeta):

    __metaclass__ = ABCMeta

    @abstractproperty
    def _exe(self):
        pass

    def __init__(self,source,dest):
        self.setSource(source)
        self.setDest(dest)
        self._io_q = queue.Queue()
        self._logger = logging.getLogger(__name__)
        self.proc = None

    def makeSurePathExists(self,path):
        if hasattr(self,'_host'):
            client=paramiko.SSHClient()
            client.load_system_host_keys()
            client.connect('lambda')
            stdin,stdout,stderr=client.exec_command(
                "mkdir -p '" + self._dest + "'")
            print(stdout.readlines())
            print(stderr.readlines())
            print(stdout.channel.recv_exit_status())    # status is 0

        else:
            try:
                os.makedirs(path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise BackupAppError(
                        'Unable to create destination path {p}'
                        .format(s=s))

    def stream_watcher(self,identifier, stream):
        for line in stream:
            self._io_q.put((identifier,
                            line.decode(sys.stdout.encoding)))

        if not stream.closed:
            stream.close()

    def start(self,options):
        popenOptions = self._getOptions(options)

        self.proc = subprocess.Popen(popenOptions,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

        to = Thread(target=self.stream_watcher,
                    name='stdout-watcher',
                    args=('STDOUT', self.proc.stdout)).start()
        te = Thread(target=self.stream_watcher,
                    name='stderr-watcher',
                    args=('STDERR', self.proc.stderr)).start()

        return self.readOutputQueue()

    # Read output queue from subprocess
    def readOutputQueue(self):
        while True:
            try:
                # Block for 0.1 second.
                qitem = self._io_q.get(True,0.1)
            except queue.Empty:
                # No output in either streams for the specified
                # timeout. Check if done?
                if self.isFinished():
                    break
            else:
                identifier, line = qitem
                if identifier == 'STDOUT':
                    self._logger.info(line.rstrip())
                else:
                    self._logger.error(line.rstrip())
        return self.proc.returncode

    def kill(self):
        if self.proc is not None and self.proc.poll() is None:
            self.proc.kill()

    def isFinished(self):
        if self.proc is not None and self.proc.poll() is not None:
            self.returncode = self.proc.returncode
            return True
        else:
            return False

    def setDest(self,d):
        self._dest = d

    def getFullDest(self):
        self.makeSurePathExists(self._dest)
        str = ''
        if hasattr(self,'_host'):
            if hasattr(self,'_user'):
                str += self._user + '@'
            str += self._host + '::'
        str += self._dest
        return str

    def setSource(self,s):
        spath = os.path.normpath(s)
        if not os.path.isabs(spath):
            raise BackupAppError('Source path {s} is not absolute'
                                 .format(s=s))
        if os.access(spath,os.R_OK):
            self._source = spath
        else:
            raise BackupAppError('Source path {s} does not exist or '
                                 'is not readable'.format(s=s))

    def setHost(self,h):
        self._host = h

    def setUser(self,u):
        self._user = u

    @abstractmethod
    def backup(self):
        return

    @abstractmethod
    def _getOptions(self,options):
        pass
