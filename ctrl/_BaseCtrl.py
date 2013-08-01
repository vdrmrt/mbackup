import view

class BaseCtrl(object):
           
    def setView(self,name):
        self.view = view.getViewObj(name)
        
    def getView(self):
        return self.view