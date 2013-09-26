from ._BaseMod import BaseMod
from resources.rdiffbackup import Rdiffbackup
import config

class BackupMod(BaseMod):
    def __init__(self,id = None,name = None,description = None,source = None,destination = None,group = None):
        self.set('id',id)        
        self.set('name',name)   
        self.set('description',description)
        self.set('source',source)
        self.set('destination',destination)
        self.set('group',group)
                
    def run(self):
        rdb = self.getRdiffBackup()
        rdb.backup()
        
    def getRunOutput(self):
        return self.getRdiffBackup().getOutput()

    def getRunReturncode(self):
        return self.getRdiffBackup().returncode
    
    def restore(self,dest,asof = None):
        return self.getRdiffBackup().restore(dest)
    
    def listIncrements(self):
        return self.getRdiffBackup().listIncrements()
    
    def getRdiffBackup(self):        
        user = config.getSetting('connection','user')
        if user == None or user.strip() == '':
            raise Exception('User setting is empty')        
        host = config.getSetting('connection','host')
        if host == None or host.strip() == '':
            raise Exception('Host setting is empty')        
        port = config.getSetting('connection','port')
        if port == None or port.strip() == '':
            raise Exception('port setting is empty')
                    
        rdb = Rdiffbackup(source = self.source,
                          user = user,
                          host = host,
                          dest = self.destination,
                          verbosity = 5,
                          sshKey = config.getKeyPath(),
                          sshPort = port)
        
        return rdb
            
            