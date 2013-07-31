import importlib
controllers = {}

def getCtrl(name):    
    global controllers
        
    if name not in controllers:        
        moduleName = 'ctrl.' + name
        module = importlib.import_module(moduleName)
        controllers[name] = getattr(module,name)()        
    
    return controllers[name]
        
def run(ctrl,cmd,kargs):
    
    ctrlObj = getCtrl(ctrl)
    getattr(ctrlObj,cmd)(**kargs)
    
    ctrlObj.view.showFlash()
    getattr(ctrlObj.view,'show_' + cmd)()
    
    