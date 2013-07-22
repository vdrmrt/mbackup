import cmd
import ctrl
import db

class Cmdline(cmd.Cmd):
    """Simple command processor example."""
    
    prompt = 'mbackup> '

    args = {'group': {'add': None,
                      'update': ['getGroupNames',None],
                      'delete': ['getGroupNames',None],
                      'info':   ['getGroupNames',{'size': None,
                                                  'lastrun': None,
                                                  'nextrun': None
                                                 }
                                ],
                      'run': None
                      },
#             'backup': {'add': None,
#                       'update': ['getGroupNames',None],
#                       'delete': ['getGroupNames',None],
#                       'info':   ['getGroupNames',{'size': None,
#                                                   'lastrun': None,
#                                                   'nextrun': None
#                                                  }
#                                 ],
#                       'run': None
#                       },
            'backup': ['getGroupNames',{'size': None,
                                        'lastrun': None,
                                        'nextrun': {'size': None,
                                                  'lastrun': ['getGroupNames',None],
                                                  'nextrun': None
                                                 }
                                        }
                      ]
                                            
            }
    
    groupNames = None
                
    def do_group(self,action):
        pass
    
    def complete_group(self,text,line,begidx,endidx):
        args = line.split()
        args.pop(0)   
        
        return self.getCompletions('group',args,text)
    
    def help_group(self):
        pass
        
    def do_backup(self,action):
        pass
    
    def complete_backup(self,text,line,begidx,endidx):
        args = line.split()
        args.pop(0)   
        
        return self.getCompletions('backup',args,text)
    
    def help_backup(self):
        pass
        
    def getCompletions(self,cmd,args,text):
        if len(text) > 0:
            args.pop() 
        
        posArg = self.args[cmd]
                        
        for x in range(0,len(args)):                        
            if isinstance(posArg, dict):                                                  
                posArg = posArg[args[x]]              
                continue                            
            if isinstance(posArg,list):                
                posArg = posArg[1]                                           
                                                                        
        if isinstance(posArg, dict):
            posArg = list(posArg.keys())
        elif isinstance(posArg, list):
            posArg = getattr(self, posArg[0])()  

        if len(text) == 0: # return all possible options when no input is available
            completions = posArg
        elif text not in posArg: # check if input is finished if not run it against allowed values
            completions = [f for f in posArg if f.startswith(text)]
        
        return completions      
        
    def getGroupNames(self):        
        if not self.groupNames:            
            backup_groups = db.DbBackupGroups();            
            self.groupNames = backup_groups.getGroupNames();        
        return self.groupNames
    
    def getTable(self,tableName):
        if tableName not in self.tables:
            self.tables['tableName'] = ctrl.Table(tableName)
        return self.tables['tableName']

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
                        
            tbl = self.getTable(table)
            getattr(tbl,action + 'Action')()
                  
        except Exception as e:
            print(e)            
                        
            
    def complete_table(self,text,line,begidx,endidx):                
        pass
            
    def help_table(self):
        print('\n'.join([ 'table <table name> <action> <parameters>','Do an action on a table.',]))
    
    
    
    
    
    
    

    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print()