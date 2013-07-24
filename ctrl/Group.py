import db
from mod.BackupGroup import BackupGroup 

class Group:

    backup_groups = None

    def __init__(self):
        self.backup_groups = db.getDbObj('BackupGroups');
    
    def add(self,arg):
        if len(arg) < 2:
            print('Expecting 2 values {l} found'.format(l=len(arg)))
            return False 
        
        backup_group_name = arg[0]
        backup_group_description = arg[1]
        backup_group_destination = arg[2]
        
        bg = BackupGroup(backup_group_name = backup_group_name,
                         backup_group_description = backup_group_description,
                         backup_group_destination = backup_group_destination)
    
        self.backup_groups.save(bg)
        
    def update(self,arg):
        fields = {'name': backup_group_name,
                  'desc': backup_group_description,
                  'dest': backup_group_destination}
               
        if len(arg) < 3:
            print('Expecting 3 values {l} found.'.format(l=len(arg)))
            return False     
        
        bg = self.backup_groups.getByBackupGroupName(arg[0])
        
        try:
            if not bg:
                raise Exception('Group {g} does not exist.'.format(g=arg[0]))
            if arg[1] == 'name':  
                bg.backup_group_name = arg[2]
            elif arg[1] == 'desc':
                bg.backup_group_description = arg[2]
            elif arg[1] == 'dest':
                bg.backup_group_destination = arg[2]
            else:
                raise Exception('{a} is not a valid field.'.format(a=arg[1]))        
        except Exception as e:
            print(e)
        else:
            self.backup_groups.save(bg)
                
                              
    