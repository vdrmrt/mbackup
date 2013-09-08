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
        
        self.set('_rdiffbackup',None)
        
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
        if self._rdiffbackup is None:            
            self._rdiffbackup = Rdiffbackup(source = self.source,
                                            user = config.get('connection','user'),
                                            host = config.get('connection','host'),
                                            dest = self.destination,
                                            verbosity = 5,
                                            sshKey = config.get('connection','key'),
                                            sshPort = config.get('connection','port',22))
        
        return self._rdiffbackup
            
            