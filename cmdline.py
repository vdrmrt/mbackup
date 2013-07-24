import cmd
import ctrl
import db
import shlex

class Cmdline(cmd.Cmd):    
    prompt = 'mbackup> '
    
    
    # args define the allowed arguments 
    # the arguments are defined in a dictionary this dictionary defines all the arguments in dictionaries or lists
    # the keys of the main dictionary must correspond the command methods of cmd.Cmd kike do_XXXXX
    # the keys in the dictionaries represents the arguments
    # the lists must contains only 2 elements:
    # * the first element is a string which represents a method that needs to be executed to get the arguments 
    #   the previous argument is passed to the method
    # * the second element is a again a dictionary or a list (providing the second element of list as a list allows chaining of methods)
    # When further arguments are available the dictionary and list end with None.           
    args = {'group': {'add': None,
                      'update': ['getGroupNames',{'name': None,
                                                  'desc': None,
                                                  'dest': None,
                                                  'expr': None
                                                 }
                                ],
                      'delete': ['getGroupNames',None],
                      'info':   ['getGroupNames',{'size': None,
                                                  'lastrun': None,
                                                  'nextrun': None
                                                 }
                                ],
                      'run': None
                      },
            'backup': {'add': None,
                      'update': ['getGroupNames',None],
                      'delete': ['getGroupNames',None],
                      'info':   ['getGroupNames',{'size': None,
                                                  'lastrun': None,
                                                  'nextrun': None
                                                 }
                                ],
                      'run': None
                      },
            }    
    
    
    groupNames = None
                
    def do_group(self,line):        
        arg = self.parseLine(line)
        try:
            if len(arg) == 0:
                 raise Exception('No command specified')      
            
            cmd = arg.pop(0)
                                   
            ctrlObj = ctrl.getCtrl('Group')            
            ctrlAction = getattr(ctrlObj,cmd)   
        except AttributeError as ae:
            print('Command %s is not defined' %cmd)
        except Exception as e:
            print(e)
        else:
            ctrlAction(arg)
    
    def complete_group(self,text,line,begidx,endidx):                
        return self.getCompletions('group',line,text)
    
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
        
    def getCompletions(self,cmd,line,text):
        
        cmdArgs = line.split()
        cmdArgs.pop(0) # remove the first argument which is the command  
        
        # remove the last element of the given arguments when the last argument is not finished
        if len(text) > 0:
            cmdArgs.pop() 
        
        # count the entered arguments
        c = len(cmdArgs)
        
        # get the possible arguments for the command
        posArg = self.args[cmd]
                        
        # loop over the entered arguments to reduce the possible arguments with the arguments already given
        for x in range(0,c):                        
            if isinstance(posArg, dict):
                posArg = posArg[cmdArgs[x]]              
                continue                            
            if isinstance(posArg,list):             
                posArg = posArg[1]                        
                
        # get the possible arguments in a list                                                          
        if isinstance(posArg, dict):
            posArgList = list(posArg.keys())
        elif isinstance(posArg, list):
            # execute method to get a list pass the last argument as a parameter      
            posArgList = getattr(self, posArg[0])(cmdArgs if c > 0 else None)  

        if len(text) == 0: # return all possible options when no input is available
            completions = posArgList
        elif text not in posArg: # check if input is finished if not run it against allowed values
            completions = [f for f in posArgList if f.startswith(text)]
        
        return completions
    
    def parseLine(self,line):
        arg = None        
        try:
            arg = shlex.split(line)
        except Exception as e:
            print('Error:',e)
        return arg
        
    def getGroupNames(self,arg):        
        if not self.groupNames:            
            bgs = db.getDbObj('BackupGroups');            
            self.groupNames = bgs.getGroupNames();            
        return self.groupNames      

    def postcmd(self, stop, line):
        # Reset group names after command so new group names will be fetched with the next command
        self.groupNames = None
        return cmd.Cmd.postcmd(self, stop, line)

    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print()