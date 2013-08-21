import os
import sqlite3
import importlib
import ctypes.wintypes

CSIDL_PERSONAL= 5        # My Documents
CSIDL_LOCAL_APPDATA = 28 # Applicaiton Data (non roaming)
SHGFP_TYPE_CURRENT= 0    # Want current, not default value

connection = None

dbObjs = {}

def getConnection():
    global connection
    if not connection:
        dbFilename = getDbPath()
        print(dbFilename)
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
    print('Creating.... need to implement.')
    
def getDbPath():
    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0,CSIDL_LOCAL_APPDATA, 0, SHGFP_TYPE_CURRENT, buf)
    appdataDir = buf.value
    if not os.path.isdir(appdataDir):
        raise('App data directroy does not exist ({p})'.format(p=appdataDir))
    
    dbDir = appdataDir + "\mbackup\db"
    os.makedirs(dbDir,exist_ok=True)

    return dbDir + '\mbackup.db'