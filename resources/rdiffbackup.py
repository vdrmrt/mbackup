import subprocess
from threading import Thread
import queue
import sys
import os
import re
import io
import time
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
    
        self.proc = None

    def stream_watcher(self,identifier, stream):        
        for line in stream:            
            self._io_q.put((identifier, line.decode(sys.stdout.encoding)))           
 
        if not stream.closed:            
            stream.close()    
                   
    def start(self,options):
        popenOptions = [self._exe,self.getVerbosityString()]
        if hasattr(self,'_host'):
            popenOptions.extend(['--remote-schema',self._remoteSchema])
        popenOptions.extend(options)
        
        self.proc = subprocess.Popen(popenOptions,stdout=subprocess.PIPE,stderr=subprocess.PIPE)  
                
        to = Thread(target=self.stream_watcher, name='stdout-watcher',args=('STDOUT', self.proc.stdout)).start()
        te = Thread(target=self.stream_watcher, name='stderr-watcher',args=('STDERR', self.proc.stderr)).start()                            
     
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
        self.start(options)

    def restore(self,asof,target):
        tpath = os.path.normpath(target)        
        if not os.path.isabs(tpath):
            raise Exception('Rdiff-backup restore target path {t} is not absolute'.format(t=tpath))
        if not os.access(tpath,os.W_OK):
            raise Exception('Rdiff-backup restore target path {t} does not exist or is not writable'.format(t=tpath))
        
        options = ['-r',asof.strip(),self.getFullDest(),tpath]
        self.start(options)
        
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
        options = ['--list-increments',self.getFullDest()]
        self.start(options)
    
    def getOutputQueue(self):
        return self._io_q
        
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
   