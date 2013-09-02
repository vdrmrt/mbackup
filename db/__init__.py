import os
import sqlite3
import importlib
import config
import logging

connection = None
logger = logging.getLogger(__name__)
dbObjs = {}

def getConnection():
    global connection
    if not connection:
        dbFilename = getDbPath()
        db_is_new = not os.path.exists(dbFilename)
                
        with sqlite3.connect(dbFilename) as connection:
            if db_is_new:
                createSchema();
            connection.row_factory = sqlite3.Row
    
    return connection

def getDbObj(name):    
    global dbObjs
        
    if name not in dbObjs:        
        moduleName = 'db.' + name + 'Db'
        module = importlib.import_module(moduleName)        
        dbObjs[name] = getattr(module,name + 'Db')()    
    
    return dbObjs[name]

def createSchema():
    logger.info('Creating.... need to implement.')
    
def getDbPath():
    appdataDir = config.getAppDataDir()
    
    dbDir = appdataDir + "\mbackup\db"
    os.makedirs(dbDir,exist_ok=True)

    return dbDir + '\mbackup.db'