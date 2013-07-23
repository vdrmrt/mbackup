import os
import sqlite3
import importlib

connection = None
dbFilename = 'mbackup.db'

dbObjs = {}

def getConnection():
    global connection
    if not connection:
        db_is_new = not os.path.exists(dbFilename)
                
        with sqlite3.connect(dbFilename) as connection:
            if db_is_new:
                createSchema();
            connection.row_factory = sqlite3.Row
    
    return connection

def getDbObj(name):    
    global dbObjs
        
    if name not in dbObjs:        
        moduleName = 'db.' + name    
        module = importlib.import_module(moduleName)        
        dbObjs[name] = getattr(module,name)()    
    
    return dbObjs[name]