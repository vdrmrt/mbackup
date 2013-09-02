import subprocess
from threading import Thread
import queue
import sys
import os
import re
import io
import time,datetime
import logging
from resources.ssh import Ssh
      
class Rdiffbackup(object):
    
    def __init__(self,source = None,host = None,user = None,dest = None,exe = 'bin\\rdiff-backup\\rdiff-backup.exe',verbosity = 3,sshPort = None,sshKey= None):        
        self._io_q = queue.Queue()
        
        # Setting default values
        self.setSource(source)
        self.setUser(user)
        self.setHost(host)
        self.setDest(dest)
        self.setRdiffBackupExe(exe)
        self.setVerbosity(verbosity)
               
        ssh = Ssh(quiet = True,
                  compression = True,
                  port = sshPort,
                  key = sshKey,
                  options = {'StrictHostKeyChecking':'no','UserKnownHostsFile':'/dev/null','PasswordAuthentication':'no'})
        self._remoteSchema = ssh.getCommandStr('%s "rdiff-backup --server"')
    
        self.setFiltering(True)
        
        self.proc = None
                
        self.logger = logging.getLogger(__name__)        

    def stream_watcher(self,identifier, stream,filter):        
        for line in stream:
            line = line.decode(sys.stdout.encoding)
            self.logger.debug(identifier + ' ' + line)
            if filter is not None and self._filtering == True:        
                line = filter(identifier,line)
            if line != False:     
                self._io_q.put((identifier,line))           
                
        if not stream.closed:            
            stream.close()    
                   
    def start(self,options,filterName = None):
        popenOptions = [self._exe,self.getVerbosityString()]
        if hasattr(self,'_host'):
            popenOptions.extend(['--remote-schema',self._remoteSchema])
        popenOptions.extend(options)
        
        if filterName is not None:
            filter = getattr(self,'_' + filterName + 'OutputFilter')
        else:
            filter = None
        
        self.proc = subprocess.Popen(popenOptions,stdout=subprocess.PIPE,stderr=subprocess.PIPE)  
                
        to = Thread(target=self.stream_watcher, name='stdout-watcher',args=('STDOUT', self.proc.stdout,filter)).start()
        te = Thread(target=self.stream_watcher, name='stderr-watcher',args=('STDERR', self.proc.stderr,filter)).start()                            
     
    def kill(self):      
        if self.proc is not None and self.proc.poll() is None:
            self.proc.kill()
            
    def isFinished(self):
        if self.proc is not None and self.proc.poll() is not None:
            self.returncode = self.proc.returncode
            return True
        else:
            return False

    def backup(self):
        options = [self._source,self.getFullDest()]        
        self.start(options,'backup')
        
    def _backupOutputFilter(self,identifier,out):
        outFatal = self._fatalOutputFilter(identifier,out)
        if outFatal != False:
            return outFatal
        if out.startswith("Processing changed file"):
            return out
        return False

    def restore(self,target,asof = '0B'):        
        tpath = os.path.normpath(target)        
        if not os.path.isabs(tpath):
            raise Exception('Rdiff-backup restore target path {t} is not absolute'.format(t=tpath))
        if not os.access(tpath,os.W_OK):
            raise Exception('Rdiff-backup restore target path {t} does not exist or is not writable'.format(t=tpath))
        
        options = ['-r',asof.strip(),self.getFullDest(),tpath]
        self.start(options,'restore')
        
    def _restoreOutputFilter(self,identifier,out):
        outFatal = self._fatalOutputFilter(identifier,out)
        if outFatal != False:
            return outFatal
        if out.startswith("Processing changed file"):
            return out
        return False
        
    def remove(self,time):        
        options = ['--force','--remove-older-than',time,self.getFullDest()]
        self.start(options)    
        
    def testServer(self):
        options = ['--test-server',self.getFullDest()]
        self.start(options)
        
    def verify(self):
        options = ['--verify',self.getFullDest()]
        self.start(options)
    
    def listIncrements(self):
        options = ['--list-increments','--parsable-output',self.getFullDest()]
        self.start(options,'listIncrements')
        
    def _listIncrementsOutputFilter(self,identifier,out):
        if identifier == 'STDOUT' and \
           not out.startswith("Using rdiff-backup version") and \
           not out.startswith("Executing"):
            try:
                return datetime.datetime.fromtimestamp(int(out.split(' ', 1)[0])).strftime('%Y-%m-%d %H:%M:%S') + "\n"
            except e:
                return 'Error converting date format from server'
        return False
        
    
    def _fatalOutputFilter(self,identifier,out):
        if out.startswith("Fatal Error:"): 
            return out
        if out.startswith("Couldn't start up the remote connection by executing"):
            return "Couldn't start up the remote connection\n"            
        return False
    
    def getOutput(self):
         while True:
            try:
                # Block for 1 second.
                item = self._io_q.get(True,0.1)
            except queue.Empty:                
                # No output in either streams for the specified timeout. Are we done?
                if self.isFinished():
                    break            
            else:
                identifier, line = item
                yield line
                
        
    def setSource(self,s):
        spath = os.path.normpath(s)
        if not os.path.isabs(spath):
            raise Exception('Rdiff-backup source path {s} is not absolute'.format(s=s))        
        if os.access(spath,os.R_OK):
            self._source = spath
        else:
            raise Exception('Rdiff-backup source path {s} does not exist or is not readable'.format(s=s))

    def setHost(self,h):
        self._host = h
        
    def setUser(self,u):
        self._user = u
        
    def setDest(self,d):
        self._dest = d
        
    def getFullDest(self):
        str = ''
        if hasattr(self,'_host'):
            if hasattr(self,'_user'):
                str += self._user + '@'
            str += self._host + '::'
        str += self._dest
        return str                

    def setRdiffBackupExe(self,exe):
        filepath = os.path.join(self.getCurrentDir(),exe)
        if os.path.isfile(filepath):            
            self._exe = filepath
        else:
            raise Exception('Rdiff-backup executable {p} does not exist'.format(p=filepath))
        
    def setVerbosity(self,v):
        if v in range(0,9):
            self._verbosity = v
        else:
            raise Exception('Invalid verbosity level')
        
    def setFiltering(self,f):
        if f:
            self._filtering = True
        else:
            self._filtering = False
    
    def getVerbosityString(self):
        if hasattr(self,'_verbosity'):
            return '-v' + str(self._verbosity)
              
    def getCurrentDir(self):
        if not hasattr(self,'_path'):
            if hasattr(sys, "frozen"):
                self._path =  os.path.dirname(os.path.realpath(sys.executable))
            else:
                #self._path = os.path.dirname(os.path.realpath(__file__))
                self._path = os.path.dirname(os.path.realpath(sys.argv[0]))
        return self._path
   