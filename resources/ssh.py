import os,sys,re

class Ssh(object):
    def __init__(self,exe = 'bin\\openssh\\bin\\ssh.exe',quiet = False,compression = True,port=None,key = None,options=[]):
        # Setting default values
        self.setSshExe(exe)
        self.setQuiet(quiet)
        self.setCompression(compression)
        self.setPort(port)
        self.setKey(key)                        
        self.setOptions(options)        
    
    def setSshExe(self,exe):
        filepath = os.path.join(self.getCurrentDir(),exe)
        if os.path.isfile(filepath):            
            self._exe = filepath
        else:
            raise Exception('Ssh executable {p} does not exist'.format(p=filepath))
        
    def setQuiet(self,q = True):
        if q:
            self._quiet = True
        else:
            self._quiet = False
            
    def getQuietString(self):
        if self._quiet:
            return '-q'
        
    def setCompression(self,c = True):
        if c:
            self._compression = True
        else:
            self._compression = False
    
    def getCompressionString(self):
        if self._compression:
            return '-C'
    
    def setPort(self,p):
        if p is not None:
            try:
                val = int(p)
                if val < 1:
                    Raise("Port value is not valid")
                self._port = val            
            except (TypeError,ValueError) as e:
                raise Exception("Port value is not valid")
            
    def getPortString(self):
        if hasattr(self,'_port'):
            return '-p ' + str(self._port)
        return ''
        
    def setKey(self,k):
        if k:
            filepath = os.path.join(self.getCurrentDir(),k)
            if os.path.isfile(filepath):            
                self._key = filepath
            else:
                raise Exception('Ssh key does not exist')
        
    def getKeyString(self):
        if hasattr(self,'_key'):
            return '-i "' + self.convertToCygwinPath(self._key)+ '"'
        return ''
        
    def setOptions(self,o):
        self._options = o
        
    def getOptionsString(self):
        if hasattr(self,'_options'):
            str = ''
            for key,val in self._options.items():
                str = str + ' -o ' + key + '=' + val
            return str
        return ''
    
    def getCommandStr(self,cmd):
        return self._exe + ' ' + self.getQuietString() + ' ' + self.getCompressionString() + ' ' + self.getPortString() + ' ' + self.getKeyString() + ' ' + self.getOptionsString() + ' ' + cmd
    
    def getCurrentDir(self):
        if not hasattr(self,'_path'):
            if hasattr(sys, "frozen"):
                self._path =  os.path.dirname(os.path.realpath(sys.executable))
            else:
                #self._path = os.path.dirname(os.path.realpath(__file__))
                self._path = os.path.dirname(os.path.realpath(sys.argv[0]))
        return self._path
        
    def convertToCygwinPath(self,path):
        path = path.replace('\\', '/')
        path = re.sub(r'^([a-zA-Z])(:)',r'/cygdrive/\1',path,1)
        return path