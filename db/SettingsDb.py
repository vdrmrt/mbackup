import db
import sqlite3
from mod.BackupMod import BackupMod 
from mod.BackupGroupMod import BackupGroupMod

class SettingsDb(object):
    '''Represents the settings table'''
    
    connection = None
    _key = 'setting_id'
    _name = 'settings'
        
    def __init__(self):                
        self.connection = db.getConnection();
    
    def getBySettingSectionAndName(self,section,name):        
        cursor = self.connection.cursor()
        query = 'SELECT {k}, setting_section, setting_name, setting_value FROM {t} WHERE setting_section = ? and setting_name = ?'.format(k=self._key,t=self._name)
        cursor.execute(query,(section,name))
        res = cursor.fetchone()       
        return res

    def save(self,section,name,value,new=False):
        try:
            if new == False:                 
                query = 'UPDATE {t} SET setting_value = ? WHERE setting_section = ? and setting_name = ?'.format(t=self._name)
            
                cursor = self.connection.cursor()
                cursor.execute(query,(value,section,name))                                                    
            else:                   
                query = 'INSERT INTO {t} (setting_section,setting_name,setting_value) VALUES (?,?,?)'.format(t=self._name)
                
                cursor = self.connection.cursor()
                cursor.execute(query,(section,name,value))
                id = cursor.lastrowid
        except sqlite3.Error as e:
            self.connection.rollback()
            raise
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
        query = '''SELECT {t}.setting_id, 
                          {t}.setting_section,
                          {t}.setting_name,
                          {t}.setting_value
                    FROM {t} '''.format(t=self._name)
        cursor = self.connection.cursor() 
        cursor.execute(query)
        return cursor.fetchall()