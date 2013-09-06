import logging
from ._BaseCtrl import BaseCtrl

class SettingsCtrl(BaseCtrl):
    def __init__(self):            
        self.setView('SettingsView')
    
    def loglevel(self,level):
        try:
            l = getattr(logging,level)
        except AttributeError:
            raise Exception('Invalid logging level {l}'.format(l=level))
        else:
            logging.getLogger().setLevel(l)
            self.view.flash('Changed logging level to: {l}'.format(l=level))