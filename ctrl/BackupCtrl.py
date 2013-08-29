import config
import db
from mod.BackupGroupMod import BackupGroupMod
from mod.BackupMod import BackupMod

from ._BaseCtrl import BaseCtrl

class BackupCtrl(BaseCtrl):
    
    def __init__(self):
        self.backups = db.getDbObj('Backups');
        self.backup_groups = db.getDbObj('BackupGroups');
        self.setView('BackupView')
        
    def add(self,name = None,description = None,source = None, destination = None,group = None):
        try:            
            if not name:            
                raise Exception('Name not provided')
            if not description:
                raise Exception('Description not provided')
            if not source:
                raise Exception('Source not provided')
            if not destination:
                raise Exception('Group not provided')
            
            bg = self.backup_groups.getByBackupGroupName(group)
            b = BackupMod(name = name,
                          description = description,
                          source = source,
                          destination = destination,
                          group = bg)
            rowcount = self.backups.save(b)           
            self.view.flash('Inserted record with id:',b.id)
        except Exception as e:
            self.view.flashError('An error occurred when inserting record:',e)
                
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
            self.view.flash('Updated {c} record(s)'.format(c=rowcount))    
        except Exception as e:
            self.view.flashError('An error occurred when updating record:',e)
            
    def delete(self,name):        
        try:
            bg = self.backups.getByBackupName(name)
            rowcount = self.backups.delete(bg.id)
            self.view.flash('Deleted {c} record(s)'.format(c=rowcount))
        except Exception as e:
            self.view.flashError('An error occurred when deleting record:', e)         
    
    def info(self,name):
        b = None
        try:
            b = self.backups.getByBackupName(name)
        except Exception as e:
            self.view.flashError('An error getting record:', e)
        else:
            self.view.info(b)        
    
    def list(self):
        try:
            self.view.list(self.backups.getList())
        except Exception as e:
            print('An error occurred when listing records:', e)
    
    def run(self,name):
        b = self.backups.getByBackupName(name)
        b.run()
        self.view.flash('Starting backup {n}.'.format(n=b.name))
        
        self.view.displayOutput(b.getRunOutput())
                
        if b.getRunReturncode() == 0:
            self.view.flash('Backup finished successfully.')
        else:
            self.view.flashError('An error occurred while backing up.')
    
    def listincr(self,name):
        b = self.backups.getByBackupName(name)
        b.listIncrements()
        self.view.flash('Getting increments from server.')
        
        self.view.displayOutput(b.getRunOutput())
        
        if not b.getRunReturncode() == 0:            
            self.view.flashError('An error occurred while getting increments.')
           