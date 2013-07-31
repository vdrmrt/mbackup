class BaseMod(object):       
    def set(self,name,value):
        object.__setattr__(self, name, value)    

    def __setattr__(self, name, value):
        if hasattr(self, name):
            self.set(name,value)
        else:
            raise AttributeError('Unable to add attribute {a} to {c}'.format(a=name,c=self.__class__.__name__))