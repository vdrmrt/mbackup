import db
import ctypes.wintypes
import os,sys

CSIDL_PERSONAL= 5        # My Documents
CSIDL_LOCAL_APPDATA = 28 # Applicaiton Data (non roaming)
SHGFP_TYPE_CURRENT= 0    # Want current, not default value

config = None

def getAppDataDir():
    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0,CSIDL_LOCAL_APPDATA, 0, SHGFP_TYPE_CURRENT, buf)
    appdataDir = buf.value
    
    if not os.path.isdir(appdataDir):
        raise('App data directory does not exist ({p})'.format(p=appdataDir))
    
    return appdataDir

configDir = getAppDataDir() + "\mbackup\config"
os.makedirs(configDir,exist_ok=True)
    
def getCurrentDir():
    if hasattr(sys, "frozen"):
        return os.path.dirname(os.path.realpath(sys.executable))
    else:
        return os.path.dirname(os.path.realpath(sys.argv[0]))
    
def getSetting(section,name,default = None):
    settings = db.getDbObj('Settings');
    
    s = settings.getBySettingSectionAndName(section,name)    
    if not s:
        if default == None:
            raise Exception('Setting with section "{s}" and name "{n}" not found'.format(s=section,n=name))
        else:
            return default
    else:
        return s['setting_value']
