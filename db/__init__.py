import os
import sqlite3
import importlib
import config
import logging

connection = None
logger = logging.getLogger(__name__)
dbObjs = {}
appDbVersion = (0,0,2)


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
                dbVersion = getCurrentDbVersion(connection)
                logger.info('Current database version: {v}'.format(v=formatDbVersion(dbVersion)))
                if appDbVersion != dbVersion:
                    logger.info('Application needs version: {v}'.format(v=formatDbVersion(appDbVersion)))                    
                    try:               
                        newDbVersion = upgradeDb(appDbVersion,dbVersion,connection)                                                
                    except Exception as e:                        
                        raise Exception('An error occurred while upgrading db: ',e)
                    else:                    
                        logger.info('Upgraded database, current db Version: {v}'.format(v=formatDbVersion(newDbVersion)))
                        if appDbVersion != newDbVersion:
                            raise Exception('Unable to upgrade to requested version, were are missing some changescripts or something is wrong in the changescripts')
                else:
                    logger.info('DB version check ok.')
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
        
def upgradeDb(appDbVersion,dbVersion,connection):
    logger.info("Database dbVersion don't match trying to upgrade")
    try:
        import glob
        
        changeScripts = []
        for name in glob.glob(config.getCurrentDir() + '/db/changescripts/mbackup-*.*.*-*.*.*.sql'):
            fullpath = (os.path.abspath(name))
            file = os.path.splitext(os.path.basename(fullpath))[0] #get the file name with extension
            spl = file.split('-')
            fromV = tuple(map(int,spl[1].split('.')))
            toV = tuple(map(int,spl[2].split('.')))
            if fromV >= dbVersion and toV <= appDbVersion:                    
                changeScripts.append((fromV,toV,fullpath))                        
        changeScripts = sorted(changeScripts, key=lambda tup: tup[0])
        sql = ""
        for changeScript in changeScripts:
            with open (changeScript[2], "r") as sqlfile:
                sql += "-- From {f} to {t}".format(f=formatDbVersion(changeScript[0]),t=formatDbVersion(changeScript[1])) + "\n" + sqlfile.read() + "\n\n"
        logger.debug("Sql changescript:\n {s}".format(s=sql))
        connection.cursor().executescript(sql)
        connection.commit()                    
    except sqlite3.Error as e:        
        raise
    else:        
        return getCurrentDbVersion(connection)
    
def getCurrentDbVersion(connection):
    try:
        cursor = connection.cursor()         
        cursor.execute("SELECT version_major,version_minor,version_revision FROM versions WHERE (version_major || '.' || version_minor || '.' || version_revision)  = (SELECT max(version_major || '.' || version_minor || '.' || version_revision) FROM versions)")                
        return tuple(cursor.fetchone())
    except sqlite3.Error as e:
        raise

def formatDbVersion(v):
    return '{ma}.{mi}.{re}'.format(ma=v[0],mi=v[1],re=v[2])
    
def getDbPath():
    appdataDir = config.getAppDataDir()
    
    dbDir = appdataDir + "\mbackup\db"
    os.makedirs(dbDir,exist_ok=True)

    return dbDir + '\mbackup.db'