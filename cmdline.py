import cmd

class Cmdline(cmd.Cmd):
    """Simple command processor example."""
    
    prompt = 'mbackup> '

    tableArgs = [
                  ['backup_groups','backups'], # table
                  ['query','new','update','delete'] # actions                
                 ]
    

    def do_table(self, action):
        arg = action.split()
        
        try:
            if len(arg) < 1:
                raise Exception('No table specified')                    
            else:
                table = arg[0]
                if table not in self.tableArgs[0]:
                    raise Exception('Table "%s" does not exist' %table)                    
        
            if len(arg) < 2:
                raise Exception('No action specified')                                
            else:
                action = arg[1]
                if action not in self.tableArgs[1]:
                    raise Exception('Action "%s" does not exist' %action)
                  
        except Exception as e:
            print(e)            
                        
            
    def complete_table(self,text,line,begidx,endidx):
#        print('\n')
#        print('text|' + text + '|end')
#        print('line|' + line + '|end')
#        print('begidx: ',begidx)
#        print('endidx: ',endidx)
      
        args = line.split()
        args.pop(0)       
#        print('args: ',args)
#        print('\n')
        
        if len(text) == 0: # return all possible options when no input is available
            completions = self.tableArgs[len(args)]
        elif text not in self.tableArgs[len(args) -1]: # check if input is a valid value if not run it against allowed values
            completions = [f for f in self.tableArgs[len(args) -1] if f.startswith(text)]
                
        return completions
            
    def help_table(self):
        print('\n'.join([ 'table <table name> <action> <parameters>','Do an action on a table.',]))

    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print()