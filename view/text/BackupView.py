from .BaseView import BaseView
from view.text.helper.prettytable import PrettyTable

class BackupView(BaseView):
    
    def show_info(self):
        if hasattr(self,'b') and self.b is not None:
            print("Id:",self.b.id)
            print("Name:",self.b.name)
            print("Description:",self.b.description)
            print("Source:",self.b.source)
            print("Destination:",self.b.destination)
            print("Group id:",self.b.group.id)
            print("Group name:",self.b.group.name)
            print("Group description:",self.b.group.description)
            print("Group destination:",self.b.group.destination)
        
    def show_list(self):
        if hasattr(self,'backupList'):
            pt = PrettyTable(['id','Name','Description','Source','Destination','Group id','Group name'])
            pt.align = 'l'
            pt.align['id'] = 'r'
            pt.align['Group id'] = 'r'         
            for row in self.backupList:
                pt.add_row(row)
            print(pt)