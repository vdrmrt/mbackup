import config
import importlib

viewObjs = {}

def getViewObj(name):    
    global viewObjs
        
    if name not in viewObjs:        
        moduleName = 'view.' + config.viewType +'.' + name    
        module = importlib.import_module(moduleName)        
        viewObjs[name] = getattr(module,name)()    
    
    return viewObjs[name]