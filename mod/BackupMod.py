from ._BaseMod import BaseMod
from resources.rdiffbackup import Rdiffbackup
import queue,sys

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
        
        oq = rdb.getOutputQueue()
        while True:
            try:
                # Block for 1 second.
                item = oq.get(True,0.1)
            except queue.Empty:                
                # No output in either streams for the specified timeout. Are we done?
                if rdb.isFinished():
                    break            
            else:
                identifier, line = item
                sys.stdout.write(identifier + ' ' + line)
    
        print('Rdb finished with return code: ',rdb.returncode)

    
    def getRdiffBackup(self):
        if self._rdiffbackup is None:
            self._rdiffbackup = Rdiffbackup(source = self.source,
                                            user = 'vdrmrt',
                                            host = 'mvsrv.be',
                                            dest = self.destination,
                                            verbosity = 5,
                                            sshKey='keys/rdiffbackup',
                                            sshPort=5555)
        
        return self._rdiffbackup
            
            