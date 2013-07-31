from view.text.helper.colorama import init
from view.text.helper.termcolor import colored
init()
from resources import flash 

class BaseView(object):
    
    def showFlash(self):        
        while flash.stack:
            msg = flash.pop()
            print(colored(msg['msg'],'red' if msg['type'] == 'error' else 'green'))