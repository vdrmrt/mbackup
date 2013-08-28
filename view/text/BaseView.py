from view.text.helper.colorama import init
from view.text.helper.termcolor import colored
init()
from resources import flash 

class BaseView(object):
    
    def flash(self,*msg):        
        print(colored(self._prepMsg(msg),'green'))
        
    def flashError(self,*msg):
        print(colored(self._prepMsg(msg),'red'))
        
    def _prepMsg(self,msg):
        return ' '.join(map(str,msg))