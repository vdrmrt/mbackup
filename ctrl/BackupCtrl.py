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
            
            bg = self.backup_groups.getByBackupGroupName(group)
            b = BackupMod(name = name,
                          description = description,
                          destination = destination,
                          group = bg)
            rowcount = self.backups.save(b)           
            flash.add('notice','Inserted record with id:',b.id)
        except Exception as e:
            flash.add('error','An error occurred when inserting record:',e)
                
    def update(self,name = None,values = None):        
        try:
            b = self.backups.getByBackupName(name)
            if not b:
                raise Exception('Backup {b} does not exist.'.format(b=name))
        
            # replace group with object
            if 'group' in values and isinstance(values['group'],str):
                values['group'] = self.backup_groups.getByBackupGroupName(values['group'])
        
            for attr, value in values.items():                         
                if hasattr(b,attr):
                    setattr(b,attr,value)
                else:
                    raise Exception('{a} is not a valid field.'.format(a=attr))            
            rowcount = self.backups.save(b)
            flash.addNotice('Updated {c} record(s)'.format(c=rowcount))    
        except Exception as e:
            flash.addError('An error occurred when updating record:',e)               
    
    def info(self,name):
        try:
            b = self.backups.getByBackupName(name)
            self.view.b = b        
        except Exception as e:
            flash.addError('An error getting record:', e)
    
    def list(self):
        try:
            self.view.backupList = self.backups.getList()
            print 
        except Exception as e:
            print('An error occurred when listing records:', e)
