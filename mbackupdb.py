import os
import sqlite3
import mbackupmodules

connection = None
db_filename = 'mbackup.db'
schema_filename = 'mbackup_schema.sql'

def getConnection():
    global connection
    if not connection:
        db_is_new = not os.path.exists(db_filename)
        
        with sqlite3.connect(db_filename) as connection:
            if db_is_new:
                print('Creating schema')
            connection.row_factory = sqlite3.Row
    
    return connection

class Backup_groups:
    '''Represents the backup_groups table'''
    
    connection = None
    _key = 'backup_group_id'
    _name = 'backup_groups'
        
    def __init__(self):
        self.connection = getConnection();
    
    def getByBackupGroupId(self,backup_group_id):
        print('Getting record',backup_group_id)
        cursor = self.connection.cursor()
        query = 'SELECT backup_group_id, backup_group_name, backup_group_destination FROM %s WHERE backup_group_id = ?' %self._name
        cursor.execute(query,(backup_group_id,))
        res = cursor.fetchone()       
        
        return mbackupmodules.Backup_group(res['backup_group_id'],res['backup_group_name'],res['backup_group_destination'])
    
    def save(self,backup_group):
        print(backup_group.backup_group_id)
        if backup_group.backup_group_id:
            print('Updating:', backup_group.backup_group_id,backup_group.backup_group_name)         
            query = 'UPDATE %s SET backup_group_name = ?, backup_group_destination = ? WHERE backup_group_id = ?' %self._name
            try:
                with self.connection:
                    self.connection.execute(query,(backup_group.backup_group_name,backup_group.backup_group_destination,backup_group.backup_group_id))
            except sqlite3.Error as e:
                print('Could not update record', e)
        else:
            print('Inserting:', backup_group.backup_group_name)         
            query = 'INSERT INTO %s (backup_group_name,backup_group_destination) VALUES (?,?)' %self._name
            try:
                with self.connection:
                    self.connection.execute(query,(backup_group.backup_group_name,backup_group.backup_group_destination))
            except sqlite3.Error as e:
                print('Could not insert record', e)
            
            
                         