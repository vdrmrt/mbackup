import cmd
import ctrl
import db
import shlex
import ast

class Cmdline(cmd.Cmd):    
    prompt = 'mbackup> '
    
    def __init__(self):
        super().__init__()
    
        self.groupNames = None
        
        # setup the possible arguments
        posArg = arg('arg')
        posArg.add('group')
        posArg.group.add('add')
        posArg.group.add('update')
        posArg.group.update.addFunction('groups','getGroupNames')
        posArg.group.update.groups.add('name')
        posArg.group.update.groups.add('desc')
        posArg.group.update.groups.add('dest')                
        posArg.group.update.groups.add('expr')        
        self.posArg = posArg
                
    def do_group(self,line):        
        arg = self.parseLine(line)
        try:
            if len(arg) == 0:
                 raise Exception('No command specified')      
            
            cmd = arg.pop(0)
                                   
            ctrlObj = ctrl.getCtrl('Group')
            ctrlAction = getattr(ctrlObj,cmd)
            if cmd == 'add':                 
                par = {'name': arg.pop(0), 'description': arg.pop(0),'destination': arg.pop(0) }                     
            elif cmd == 'update':
                par = {'name': arg.pop(0)}
                field = arg.pop(0)
                if field == 'name':    
                    values = {'name': arg.pop(0)}
                elif field == 'dest':
                    values = {'destination': arg.pop(0)}
                elif field == 'desc':
                    values = {'description': arg.pop(0)}
                elif field == 'expr':
                    values = ast.literal_eval(arg.pop(0))
                else:
                    raise Exception('Field {f} unknown'.format(f=field))              
                par['values'] = values                                                        
        except AttributeError as ae:
            print('Command  is not defined'.format(cmd=cmd))
        except IndexError as ie:
            print('To few arguments for {cmd}'.format(cmd=cmd))
        except SyntaxError as se:
            print('Invalid syntax')
        except Exception as e:
            print(e)
        else:
            ctrlAction(**par)
    
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
        
        # remove the last element of the given arguments when the last argument is not finished
        if len(text) > 0:
            cmdArgs.pop() 
        
        # count the entered arguments
        c = len(cmdArgs)
        
        # get the possible arguments for the command   
        posArg = self.posArg
                        
        # loop over the entered arguments to reduce the possible arguments with the arguments already given
        for x in range(0,c):    
            if posArg.getFunction():                
                posArg = posArg.getFirstChild()
            elif posArg.childExsists(cmdArgs[x]):
                posArg = posArg.getChild(cmdArgs[x])        
            else:
                break  
                
        # get the possible arguments in a list                                                          
        if posArg.getFunction():            
            posArgList = getattr(self, posArg.getFunction())(cmdArgs if c > 0 else None)
        else:
            # execute method to get a list pass the last argument as a parameter                  
            posArgList = posArg.getChildNames()

        if len(text) == 0: # return all possible options when no input is available
            completions = posArgList
        elif not posArg.childExsists(text): # check if input is finished if not run it against allowed values
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
        
        
class arg(object):
        
    def __init__(self, name):
        self._name = name
        self._children = {}
        self._function = False       
        
    def add(self,child):
        if isinstance(child,str):
            self._children[child] = arg(child)
        elif isinstance(child,par):
            self._children[child._name] = child
        else:
            raise Exception('Unable to add child, child is not an par object or string.')
        
    def getName(self):
        return self._name
    
    def getChild(self,name):
        if name in self._children:
            return self._children[name]
        else:
            raise AttributeError('{obj} object has no attribute {attr}'.format(obj=type(self).__name__,attr=name))
    
    def __getattr__(self,attr):
        return self.getChild(attr)
    
    def getFirstChild(self):
        return next (iter (self._children.values()))
    
    def childExsists(self,name):
        return name in self._children
        
    def addFunction(self,child,f):
        self.add(child)
        self._function = f
        
    def getFunction(self):
        return self._function       
    
    def getChildNames(self):
        ret = []
        for k in self._children:
            ret.append(k)
        return ret
    
    def __repr__(self,level = 0):
        ret = "\t"*level + self._name + "\n"
        for child in self._children.values():
            ret += child.__repr__(level+1)        
        return ret