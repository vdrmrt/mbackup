import db
from mod.BackupGroup import BackupGroup 

class Group:

    backup_groups = None

    def __init__(self):
        self.backup_groups = db.getDbObj('BackupGroups');
    
    def add(self,name = None,description = None,destination = None):
        try:            
            if not name:            
                raise Exception('Name not provided')
            if not description:
                raise Exception('Description not provided')
            if not destination:
                raise Exception('Destination not provided')
        except Exception as e:
            print(e)
        else:
            try:
                bg = BackupGroup(name = name,
                                 description = description,
                                 destination = destination)    
                rowcount = self.backup_groups.save(bg)
                print('Inserted {c} record(s)'.format(c=rowcount))
                print('Inserted record with id:', bg.id)
            except Exception as e:    
                print('An error occurred when inserting record:', e)
        
    def update(self,name = None,values = None):        
        bg = self.backup_groups.getByBackupGroupName(name)    
        try:
            if not bg:
                raise Exception('Group {g} does not exist.'.format(g=name))                
            for attr, value in values.items():                         
                if hasattr(bg,attr):
                    setattr(bg,attr,value)
                else:
                    raise Exception('{a} is not a valid field.'.format(a=attr))            
        except Exception as e:
            print(e)
        else:
            try:
                rowcount = self.backup_groups.save(bg)
                print('Updated {c} record(s)'.format(c=rowcount))
            except Exception as e:
                print('An error occurred when updating record:', e)

    def delete(self,name):        
        try:
            bg = self.backup_groups.getByBackupGroupName(name)
            rowcount = self.backup_groups.delete(bg.id)
            print('Deleted {c} record(s)'.format(c=rowcount))
        except Exception as e:
            print('An error occurred when deleting record:', e)
                              
    