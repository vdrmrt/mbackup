import config
from resources import flash
import db
from mod.BackupGroupMod import BackupGroupMod

from ._BaseCtrl import BaseCtrl

class GroupCtrl(BaseCtrl):

    def __init__(self):
        self.backup_groups = db.getDbObj('BackupGroups');
        self.setView('GroupView')
    
    def add(self,name = None,description = None,destination = None):
        try:            
            if not name:            
                raise Exception('Name not provided')
            if not description:
                raise Exception('Description not provided')
            if not destination:
                raise Exception('Destination not provided')
            
            bg = BackupGroupMod(name = name,
                                description = description,
                                destination = destination)    
            rowcount = self.backup_groups.save(bg)           
            flash.addNotice('Inserted record with id:', bg.id)
        except Exception as e:    
            flash.addError('An error occurred when inserting record:', e)
        
    def update(self,name = None,values = None):    
        try:
            bg = self.backup_groups.getByBackupGroupName(name)
            if not bg:
                raise Exception('Group {g} does not exist.'.format(g=name))                
            for attr, value in values.items():                         
                if hasattr(bg,attr):
                    setattr(bg,attr,value)
                else:
                    raise Exception('{a} is not a valid field.'.format(a=attr))            
            rowcount = self.backup_groups.save(bg)
            flash.addNotice('Updated {c} record(s)'.format(c=rowcount))    
        except Exception as e:
            flash.addError('An error occurred when updating record:',e)               

    def delete(self,name):        
        try:
            bg = self.backup_groups.getByBackupGroupName(name)
            rowcount = self.backup_groups.delete(bg.id)
            flash.addNotice('Deleted {c} record(s)'.format(c=rowcount))
        except Exception as e:
            flash.addError('An error occurred when deleting record:', e)
            
    def list(self):
        try:
            self.view.backupGroupList = self.backup_groups.getList()
        except Exception as e:
            flash.addError('An error occurred when listing records:', e)
                
    def info(self,name):
        try:
            bg = self.backup_groups.getByBackupGroupName(name)
            self.view.bg = bg          
        except Exception as e:
            flash.addError('An error getting record:', e)
                              
    