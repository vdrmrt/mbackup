import db
from mod import backupgroup

class Group:

    backup_groups = None

    def __init__(self):
        self.backup_groups = db.getDbObj('BackupGroups');
    
    def add(self,arg):
    
        backup_group_name = arg[0]
        backup_group_destination = arg[1]
    
        bg = backupgroup.BackupGroup(backup_group_name = backup_group_name,
                                     backup_group_destination = backup_group_destination)
    
        self.backup_groups.save(bg)
    