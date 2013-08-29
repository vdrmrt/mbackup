from ._BaseMod import BaseMod
from resources.rdiffbackup import Rdiffbackup

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
                                            user = 'vdrmrt',
                                            host = 'mvsrv.be',
                                            dest = self.destination,
                                            verbosity = 5,
                                            sshKey = 'keys/rdiffbackup',
                                            sshPort = 5555)
        
        return self._rdiffbackup
            
            