import db
import sqlite3
from mod.BackupMod import BackupMod 
from mod.BackupGroupMod import BackupGroupMod

class BackupsDb(object):
    '''Represents the backups table'''
    
    connection = None
    _key = 'backup_id'
    _name = 'backups'
        
    def __init__(self):                
        self.connection = db.getConnection();
        self.backup_groups = db.getDbObj('BackupGroups');
    
    def getByBackupId(self,id):
        cursor = self.connection.cursor()
        query = 'SELECT backup_id, backup_group_id,backup_name, backup_description, backup_destination FROM {t} WHERE {k} = ?'.format(t=self._name,k=self._key)
        cursor.execute(query,(backup_group_id,))
        res = cursor.fetchone()
        if res:
            bg = self.backup_groups.getDbObj(res['backup_group_id']);
            return BackupMod(res['backup_group_id'],res['backup_group_name'],res['backup_group_description'],res['backup_group_destination'],bg)
        else:
            raise Exception('Record with id {id} not found'.format(id=id))       
    
    def getByBackupName(self,name):        
        cursor = self.connection.cursor()
        query = 'SELECT backup_id, backup_group_id,backup_name, backup_description, backup_destination FROM {t} WHERE backup_name = ?'.format(t=self._name)
        cursor.execute(query,(name,))
        res = cursor.fetchone()       
        if res:
             bg = self.backup_groups.getDbObj(res['backup_group_id'])
             return BackupMod(res['backup_group_id'],res['backup_group_name'],res['backup_group_description'],res['backup_group_destination'],bg)
        else:
            raise Exception('Record with name {name} not found'.format(name=name))
    
    def save(self,b):
        if not isinstance(b,BackupMod):
            raise Exception('Provided object is not an BackupMod instance')
         
        try:
            if b.id:                 
                query = 'UPDATE {t} SET backup_group_id = ?, backup_name = ?, backup_description = ? ,backup_destination = ? WHERE {k} = ?'.format(t=self._name,k=self._key)
            
                cursor = self.connection.cursor()
                cursor.execute(query,(b.group.id,
                                      b.name,                                    
                                      b.description,
                                      b.destination,
                                      b.id))                                                    
            else:                   
                query = 'INSERT INTO {t} (backup_group_id,backup_name,backup_description,backup_destination) VALUES (?,?,?,?)'.format(t=self._name)
                
                cursor = self.connection.cursor()
                cursor.execute(query,(b.group.id,
                                      b.name,
                                      b.description,
                                      b.destination))
                b.id = cursor.lastrowid
        except sqlite3.Error as e:
            self.connection.rollback()
            raise e
        else:
            self.connection.commit()
            return cursor.rowcount

    def delete(self,id):            
        query = 'DELETE FROM {t} WHERE {k} = ?'.format(t=self._name,k=self._key)
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(id,))                                       
            self.connection.commit()             
        except sqlite3.Error as e:
            self.connection.rollback()
            raise('Could not delete record', e)
        else:
            return cursor.rowcount
    
    def getList(self):
        query = '''SELECT {t}.backup_id, 
                          {t}.backup_name,
                          {t}.backup_description,
                          {t}.backup_destination,
                          backup_groups.backup_group_id,
                          backup_groups.backup_group_name
                    FROM {t} 
                        LEFT JOIN backup_groups
                        WHERE backup_groups.backup_group_id = backups.backup_group_id'''.format(t=self._name)
        cursor = self.connection.cursor() 
        cursor.execute(query)
        return cursor.fetchall()
                         