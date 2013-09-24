import os
import sqlite3
import importlib
import config
import logging

connection = None
logger = logging.getLogger(__name__)
dbObjs = {}
dbVersion = (0,0,2)


def getConnection():
    global connection
    if not connection:
        dbFilename = getDbPath()
        db_is_new = not os.path.exists(dbFilename)
                
        with sqlite3.connect(dbFilename) as connection:
            if db_is_new:
                createSchema();
            connection.row_factory = sqlite3.Row
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT version_major,version_minor,version_revision FROM versions WHERE (version_major || '.' || version_minor || '.' || version_revision)  = (SELECT max(version_major || '.' || version_minor || '.' || version_revision) FROM versions)")                
                version = tuple(cursor.fetchone())
                logger.info('Current database version: {ma}.{mi}.{re}'.format(ma=version[0],mi=version[1],re=version[2]))
                if dbVersion != version:
                    logger.info("Database version don't match trying to upgrade")
                    try:
                        raise Exception('Database versions do not match.')
                    except:
                        raise
                    else:
                        logger.info('Successfully upgraded database')
                else:
                    logger.info('DB versions match')
            except Exception as e:
                raise
                
    return connection

def getDbObj(name):    
    global dbObjs
        
    if name not in dbObjs:        
        moduleName = 'db.' + name + 'Db'
        module = importlib.import_module(moduleName)        
        dbObjs[name] = getattr(module,name + 'Db')()    
    
    return dbObjs[name]

def createSchema():
    logger.info('Database does not exist. Creating...')
    
    logger.info('Getting sql schema.')
    dir = config.getCurrentDir()
    path = dir + '/db/schema.sql'
    try:
        with open (path, "r") as myfile:
            schema = myfile.read()
    except IOError:
        logger.critical('Unable to read db schema file.')        
    else:    
        getConnection().cursor().executescript(schema)
        getConnection().commit()     
        
    
def getDbPath():
    appdataDir = config.getAppDataDir()
    
    dbDir = appdataDir + "\mbackup\db"
    os.makedirs(dbDir,exist_ok=True)

    return dbDir + '\mbackup.db'