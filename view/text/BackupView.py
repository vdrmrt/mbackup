from .BaseView import BaseView
from view.text.helper.prettytable import PrettyTable
import sys

class BackupView(BaseView):
    
    def info(self,b):
        print("Id:",b.id)
        print("Name:",b.name)
        print("Description:",b.description)
        print("Source:",b.source)
        print("Destination:",b.destination)
        print("Group id:",b.group.id)
        print("Group name:",b.group.name)
        print("Group description:",b.group.description)
        print("Group destination:",b.group.destination)
        
    def list(self,backupList):        
        pt = PrettyTable(['id','Name','Description','Source','Destination','Group id','Group name'])
        pt.align = 'l'
        pt.align['id'] = 'r'
        pt.align['Group id'] = 'r'         
        for row in backupList:
            pt.add_row(row)
        print(pt)
        
    def displayOutput(self,output):
        for out in output:
            sys.stdout.write(out)