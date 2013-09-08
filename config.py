import configparser
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

def getConfigObj():
    global config
    if config is None:
        configPath = configDir + "\config.ini"

        defaultConfigText = """[view]
type=text
[connection]
host=mvsrv.be
port=5555
"""

        if not os.path.isfile(configPath):
            try:
                with open(configPath,'w') as f:
                    f.write(defaultConfigText)
            except Exception as e:
                raise Exception('Error while creating config file:',e)
            
        config = configparser.ConfigParser()
        config.read(configPath)

    return config
    
def get(section,key,default = None):
    config = getConfigObj()
    
    if config is not None:
        if section in config:
            c = config[section].get(key,default)
            if c is None:
                raise Exception ('Config key {k} does not exist'.format(k=key))
            else: 
                return config[section].get(key,default)
        else:
            raise Exception ('Config section {s} does not exist'.format(s=section))
    else:
        raise Exception ('Unable to get config')
    
def getCurrentDir():
    if hasattr(sys, "frozen"):
        return os.path.dirname(os.path.realpath(sys.executable))
    else:
        return os.path.dirname(os.path.realpath(sys.argv[0]))
