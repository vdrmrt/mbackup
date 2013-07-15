import os
import sqlite3

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
            connection.row_factory = dict_factory
    
    return connection

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

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
        return res
    
    def save(self,row):
        if row[self._key]:
            print('Updating:', row[self._key],row['backup_group_name'])         
            query = 'UPDATE %s SET backup_group_name = ?, backup_group_destination = ? WHERE backup_group_id = ?' %self._name          
            try:
                with self.connection:
                    self.connection.execute(query,(row['backup_group_name'],row['backup_group_destination'],row[self._key]))
            except sqlite3.Error:
                print('Could not update record')
            
            
            
                         