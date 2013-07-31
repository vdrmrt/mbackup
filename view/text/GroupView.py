from .BaseView import BaseView
from view.text.helper.prettytable import PrettyTable

class GroupView(BaseView):
    
    def show_update(self):
        pass
    
    def show_info(self):
        print("Id:",self.bg.id)
        print("Name:",self.bg.name)
        print("Description:",self.bg.description)
        print("Destination:",self.bg.destination) 