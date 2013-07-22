import os
import sqlite3
import mod #modules

import pprint

connection = None
db_filename = 'mbackup.db'

def getConnection():
    global connection
    if not connection:
        db_is_new = not os.path.exists(db_filename)
                
        with sqlite3.connect(db_filename) as connection:
            if db_is_new:
                createSchema();
            connection.row_factory = sqlite3.Row
        return connection


class DbBackupGroups:
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
        
        return mod.BackupGroup(res['backup_group_id'],res['backup_group_name'],res['backup_group_destination'])
    
    def save(self,backup_group):
        print(backup_group.backup_group_id)
        if backup_group.backup_group_id:
            print('Updating:', backup_group.backup_group_id,backup_group.backup_group_name)         
            query = 'UPDATE %s SET backup_group_name = ?, backup_group_destination = ? WHERE %s = ?' % (self._name, self._key)
            try:
                cursor = self.connection.cursor()
                cursor.execute(query,(backup_group.backup_group_name,backup_group.backup_group_destination,backup_group.backup_group_id))
                print('Updated %i record(s)' %cursor.rowcount)
                self.connection.commit()               
            except sqlite3.Error as e:
                self.connection.rollback()   
                print('Could not update record', e)
        else:
            print('Inserting:', backup_group.backup_group_name)         
            query = 'INSERT INTO %s (backup_group_name,backup_group_destination) VALUES (?,?)' %self._name
            try:
               cursor = self.connection.cursor()
               cursor.execute(query,(backup_group.backup_group_name,backup_group.backup_group_destination))
               print('Inserted %i record(s)' %cursor.rowcount)
               print('Inserted record rowid:', cursor.lastrowid)
               self.connection.commit()               
            except sqlite3.Error as e:
                print('Could not insert record', e)

    def delete(self,backup_group_id):
        print('Deleting record:', backup_group_id)         
        query = 'DELETE FROM %s WHERE %s = ?' %(self._name, self._key)
        try:
             cursor = self.connection.cursor()
             cursor.execute(query,(backup_group_id,))                          
             print('Deleted %i record(s)' %cursor.rowcount)
             self.connection.commit()             
        except sqlite3.Error as e:
            print('Could not delete record', e)
    
    def getGroupNames(self):
        query = 'SELECT backup_group_name FROM backup_groups'
        cursor = self.connection.cursor()
        cursor.execute(query)
        res = []
        for row in cursor.fetchall():
            res.append(row['backup_group_name'])
        return res
                    
def createSchema():
    schema_filename = 'mbackup_schema.sql'
    print('Creating schema')
                         