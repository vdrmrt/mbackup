import cmd

class Cmdline(cmd.Cmd):
    """Simple command processor example."""
    
    prompt = 'mbackup> '

    tables = [ 'backup_groups','backups']
    tableActions = ['query','new','update','delete']
    

    def do_table(self, action):
        arg = action.split()
        
        try:
            if len(arg) < 1:
                raise Exception('No table specified')                    
            else:
                table = arg[0]
                if table not in self.tables:
                    raise Exception('Table "%s" does not exist' %table)                    
        
            if len(arg) < 2:
                raise Exception('No action specified')                                
            else:
                action = arg[1]
                if action not in self.tableActions:
                    raise Exception('Action "%s" does not exist' %action)
                  
        except Exception as e:
            print(e)            
                        
            
    def complete_table(self,text,line,begidx,endidx):
#       print('\n')
#       print('text: ',text)
#       print('line: ',line)
#       print('begidx: ',begidx)
#       print('endidx: ',endidx)

        arg = line.split()
#        print('arg: ',arg)
            
        
        # when the last argument and text are not equal (arg[-1] == text) we have an invalid action and we don't have complete any further         
        if len(arg) < 2:
            completions = self.tables
        elif arg[1] in self.tables:
            if len(arg) < 3:
                completions = self.tableActions
            else:                
                completions = [f for f in self.tableActions if arg[-1] == text and f.startswith(text)]
        else:
            completions = [f for f in self.tables if arg[-1] == text and f.startswith(text)]
                    
        return completions
            
    def help_table(self):
        print('\n'.join([ 'table <table name> <action> <parameters>','Do an action on a table.',]))

    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print()