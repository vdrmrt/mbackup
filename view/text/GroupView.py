from .BaseView import BaseView
from view.text.helper.prettytable import PrettyTable

class GroupView(BaseView):
    def info(self,bg):
        print("Id:",bg.id)
        print("Name:",bg.name)
        print("Description:",bg.description)
        print("Destination:",bg.destination)
        
    def list(self,list):
        pt = PrettyTable(['id','Name','Description','Destination'])
        pt.align = 'l'
        pt.align['id'] = 'r'            
        for row in list:
            pt.add_row(row)
        print(pt)