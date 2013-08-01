from ._BaseMod import BaseMod

class BackupMod(BaseMod):
    def __init__(self,id = None,name = None,description = None,destination = None,group = None):
        self.set('id',id)        
        self.set('name',name)   
        self.set('description',description)
        self.set('destination',destination)
        self.set('group',group)