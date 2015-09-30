""" Module that defines the main mbackup class."""

from .mbackuperror import MbackupError
from abc import ABCMeta, abstractmethod, abstractproperty

import queue
import os
import sys
import shutil
import subprocess
from threading import Thread
import logging
import errno

class Mbackup(metaclass=ABCMeta):
    """ The Mbackup class is defined as an Abstract Base Clases this
    class implements the main backup functionality other classes extend
    this class to handle the actual interface with the actual backup
    program.
    These are the abstract properties:

    * _exe : the actual backup executable.
    * _hostSeperator : the sperator after the host used in
      target / connection path if the backup program. This seperator is
      different between backup programs.

    These are the abstract methods:

    * _getOptions: the options to pass to the backup program.

    This class uses subprocess to execute the backup program and
    threading to capture and print the output of the backup program.

    When the backup is started, :func:`~mbackup.Mbackup.start` method,
    the backup program is executed with the stdout and stderr pipes
    redirected to subprocess. Then two threads are started,
    :func:`~mbackup.Mbackup.stream_watcher` method, to capture and put
    the output from the stdout and stdin in a queue. In the running
    parent process this queue is read,
    :func:`~mbackup.Mbackup.readOutputQueue` method, untill the
    subprocess is finished.
    """

    @abstractproperty
    def _exe(self):
        """ Abstract property to define the actual backup executable.
        """
        pass

    @abstractproperty
    def _hostSeperator(self):
        """ Abstract property to define the sperator after the host.
        This seperator is different between backup programs.
        """
        pass

    @abstractmethod
    def _getOptions(self,options):
        pass

    def __init__(self,source,dest):
        """ The initialization of the object. Set the source,
        destination and intialize the queue and logger.

        Args:
            source(string): source path to backup
            dest(string): destination path of backup
        """
        self.setSource(source)
        self._dest = dest
        self._io_q = queue.Queue()
        self._logger = logging.getLogger(__name__)
        self.proc = None

    def backup(self):
        """ Start the backup """
        options = [self._source,self.getFullDest()]
        return self.start(options)

    def stream_watcher(self,identifier, stream):
        """ Loop over a stream and put each line in a queue.

        Args:
            identifier(string): used to keep track of different streams
                because all data goes to the same queue.
            stream(stream): stream to read.
        """
        for line in stream:
            dec = line.decode(sys.stdout.encoding)
            self._io_q.put((identifier,dec))

        if not stream.closed:
            stream.close()

    def start(self,options):
        """ Start the backup

        Args:
            options(list): options to pass to backup program.

        Returns:
            Returncode of the backup program.

        """
        popenOptions = self._getOptions(options)


        self._logger.debug('Starting new process with following '
                           'options {o}'.format(o=popenOptions))
        self.proc = subprocess.Popen(popenOptions,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        to = Thread(target=self.stream_watcher,
                    name='stdout-watcher',
                    args=('STDOUT', self.proc.stdout)).start()
        te = Thread(target=self.stream_watcher,
                    name='stderr-watcher',
                    args=('STDERR', self.proc.stderr)).start()

        self.readOutputQueue()
        return self.proc.returncode

    # Read output queue from subprocess
    def readOutputQueue(self):
        """Reads the queue and passes output to logger."""

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

    def kill(self):
        """ Kills the running backup program """
        if self.proc is not None and self.proc.poll() is None:
            self.proc.kill()

    def isFinished(self):
        """ Check if backup program is finished

        Returns:
            True or false
        """

        if self.proc is not None and self.proc.poll() is not None:
            return True
        else:
            return False

    def getFullDest(self):
        """ Add host and user to the destination path to create a
        target path used by the backup program.

        Retruns:
            Target path containg the target path and if set the host and
            user.
        """
        str = ''
        if hasattr(self,'_host'):
            if hasattr(self,'_user'):
                str += self._user + '@'
            str += self._host + self._hostSeperator
        str += self._dest
        return str

    def setSource(self,s):
        """ Set the source path check if the path is absolote or
        readable.

        Raises:
            MbackupError: If path is not absolute or readable.

        """
        spath = os.path.normpath(s)
        if not os.path.isabs(spath):
            raise MbackupError('Source path {s} is not absolute'
                                 .format(s=s))
        if os.access(spath,os.R_OK):
            self._source = spath
        else:
            raise MbackupError('Source path {s} does not exist or '
                                 'is not readable'.format(s=s))

    def setHost(self,h):
        """ Set the target host."""
        self._host = h

    def setUser(self,u):
        """ Set the user to be used on target host."""
        self._user = u
