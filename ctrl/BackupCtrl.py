import config
from resources import flash
import db
from mod.BackupGroupMod import BackupGroupMod
from mod.BackupMod import BackupMod

from ._BaseCtrl import BaseCtrl

class BackupCtrl(BaseCtrl):
    
    def __init__(self):
        self.backups = db.getDbObj('Backups');
        self.backup_groups = db.getDbObj('BackupGroups');
        self.setView('BackupView')
        
    def add(self,name = None,description = None,destination = None,group = None):
        try:            
            if not name:            
                raise Exception('Name not provided')
            if not description:
                raise Exception('Description not provided')
            if not destination:
                raise Exception('Destination not provided')
            if not destination:
                raise Exception('Group not provided')
        except Exception as e:
            print(e)
        else:
            try:
                bg = self.backup_groups.getByBackupGroupName(group)
                b = BackupMod(name = name,
                              description = description,
                              destination = destination,
                              group = bg)
                rowcount = self.backups.save(b)           
                flash.add('notice','Inserted record with id:' + str(b.id))
            except Exception as e:
                raise e 
                flash.add('error','An error occurred when inserting record: ' + str(e))
    
    def list(self):
        try:
            self.view.backupList = self.backups.getList()
            print 
        except Exception as e:
            print('An error occurred when listing records:', e)
