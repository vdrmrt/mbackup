import importlib
controllers = {}

def getCtrl(name):    
    global controllers
        
    if name not in controllers:        
        moduleName = 'ctrl.' + name + 'Ctrl'
        module = importlib.import_module(moduleName)
        controllers[name] = getattr(module,name + 'Ctrl')()        
    
    return controllers[name]
        
def run(ctrl,cmd,kargs):
    ctrlObj = getCtrl(ctrl)
    getattr(ctrlObj,cmd)(**kargs)
    
    