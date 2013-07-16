class Backup_group:
    backup_group_id = None
    backup_group_name = None
    backup_group_destination = None
    
    def __init__(self,backup_group_id = None,backup_group_name = None,backup_group_destination = None):
        self.backup_group_id = backup_group_id
        self.backup_group_name = backup_group_name
        self.backup_group_destination = backup_group_destination
        