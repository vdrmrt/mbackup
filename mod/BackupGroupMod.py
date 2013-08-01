from ._BaseMod import BaseMod

class BackupGroupMod(BaseMod):
    def __init__(self,id = None,name = None,description = None,destination = None):
        self.set('id',id)
        self.set('name',name)   
        self.set('description',description)
        self.set('destination',destination)