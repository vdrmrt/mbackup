from .BaseView import BaseView
from view.text.helper.prettytable import PrettyTable

class GroupView(BaseView):
    
    def show_add(self):
        pass
    
    def show_update(self):
        pass
    
    def show_info(self):
        print("Id:",self.bg.id)
        print("Name:",self.bg.name)
        print("Description:",self.bg.description)
        print("Destination:",self.bg.destination)
        
    def show_list(self):
        if hasattr(self,'backupGroupList'):
            pt = PrettyTable(['id','Name','Description','Destination'])
            pt.align = 'l'
            pt.align['id'] = 'r'            
            for row in self.backupGroupList:
                pt.add_row(row)
            print(pt)