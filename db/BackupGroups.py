import db
import sqlite3
from mod.BackupGroup import BackupGroup 

class BackupGroups(object):
    '''Represents the backup_groups table'''
    
    connection = None
    _key = 'backup_group_id'
    _name = 'backup_groups'
        
    def __init__(self):                
        self.connection = db.getConnection();        
    
    def getByBackupGroupId(self,backup_group_id):
        cursor = self.connection.cursor()
        query = 'SELECT backup_group_id, backup_group_name, backup_group_description, backup_group_destination FROM {t} WHERE {k} = ?'.format(t=self._name,k=self._key)
        cursor.execute(query,(backup_group_id,))
        res = cursor.fetchone()
        if res:
            return BackupGroup(res['backup_group_id'],res['backup_group_name'],res['backup_group_description'],res['backup_group_destination'])
        else:
            raise Exception('Record with id {id} not found'.format(id=id))       
    
    def getByBackupGroupName(self,name):        
        cursor = self.connection.cursor()
        query = 'SELECT backup_group_id, backup_group_name, backup_group_description, backup_group_destination FROM {t} WHERE backup_group_name = ?'.format(t=self._name)
        cursor.execute(query,(name,))
        res = cursor.fetchone()       
        if res:
            return BackupGroup(res['backup_group_id'],res['backup_group_name'],res['backup_group_description'],res['backup_group_destination'])
        else:
            raise Exception('Record with name {name} not found'.format(name=name))
    
    def save(self,bg):
        if not isinstance(bg,BackupGroup):
            raise Exception('Provided object is not an BackupGroup instance')
         
        try:
            if bg.id:                 
                query = 'UPDATE {t} SET backup_group_name = ?, backup_group_description = ? ,backup_group_destination = ? WHERE {k} = ?'.format(t=self._name,k=self._key)
            
                cursor = self.connection.cursor()
                cursor.execute(query,(bg.name,
                                      bg.description,
                                      bg.destination,
                                      bg.id))                                                    
            else:                   
                query = 'INSERT INTO {t} (backup_group_name,backup_group_description,backup_group_destination) VALUES (?,?,?)'.format(t=self._name)
                
                cursor = self.connection.cursor()
                cursor.execute(query,(bg.name,
                                      bg.description,
                                      bg.destination))
                bg.id = cursor.lastrowid
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
        query = 'SELECT backup_group_id, backup_group_name, backup_group_description, backup_group_destination FROM {t}'.format(t=self._name)
        cursor = self.connection.cursor() 
        cursor.execute(query)
        return cursor.fetchall()                
    
    def getGroupNames(self):    
        query = 'SELECT backup_group_name FROM backup_groups'        
        cursor = self.connection.cursor()        
        cursor.execute(query)            
        res = []
        for row in cursor.fetchall():
            res.append(row['backup_group_name'])
        return res            
                         