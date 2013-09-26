import db
import logging
from ._BaseCtrl import BaseCtrl

class SettingsCtrl(BaseCtrl):
    def __init__(self):
        self.settings = db.getDbObj('Settings');
        self.setView('SettingsView')
    
    def set(self,section = None,name = None, value = None):
        try:
            s = self.settings.getBySettingSectionAndName(section,name)
            if not s:
                raise Exception('Setting with section "{s}" and name "{n}" not found'.format(s=section,n=name))
        
            #if other actions then updating the db are required handle them here:
            self.handleSettings(section, name,value)
        
            rowcount = self.settings.save(section,name,value)
            self.view.flash('Changed setting {n} to {v} in section {s}'.format(n=name,v=value,s=section))    
        except Exception as e:
            self.view.flashError('An error occurred while changing setting:',e)
            
    def handleSettings(self,section,name,value):
        if section == 'application' and name == 'loglevel':
            self.handleLogLevel(value)
            return True
        return False
            
    def handleLogLevel(self,level):
        try:
            l = getattr(logging,level)
        except AttributeError:
            raise Exception('Invalid logging level {l}'.format(l=level))
        else:
            logging.getLogger().setLevel(l)
            self.view.flash('Changed logging level to: {l}'.format(l=level))