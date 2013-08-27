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
        posArg.group.add('info')
        posArg.group.info.addFunction('groups','getGroupNames')
        posArg.group.add('delete')    
        posArg.group.delete.addFunction('groups','getGroupNames')
        posArg.group.add('list')
        posArg.add('backup')
        posArg.backup.add('add')
        posArg.backup.add('update')
        posArg.backup.update.addFunction('backups','getBackupNames')
        posArg.backup.update.backups.add('name')
        posArg.backup.update.backups.add('desc')
        posArg.backup.update.backups.add('src')
        posArg.backup.update.backups.add('dest')
        posArg.backup.update.backups.add('group')             
        posArg.backup.update.backups.add('expr')
        posArg.backup.add('info')
        posArg.backup.info.addFunction('groups','getBackupNames')
        posArg.backup.add('delete')    
        posArg.backup.delete.addFunction('groups','getBackupNames')
        posArg.backup.add('list')
        posArg.backup.add('run')
        posArg.backup.run.addFunction('backups','getBackupNames')    
        self.posArg = posArg
                
    def do_group(self,line):
        arg = self.parseLine(line)
        try:
            if len(arg) == 0:
                 raise Exception('No command specified')      
            
            cmd = arg.pop(0)
                                               
            if cmd == 'add':                 
                par = {'name': arg.pop(0), 'description': arg.pop(0),'destination': arg.pop(0)}                     
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
            elif cmd == 'delete':
                par = {'name': arg.pop(0)}                
            elif cmd == 'info':
                par = {'name': arg.pop(0)}
            elif cmd == 'list':
                par = {}
            else:
                raise Exception('Command {cmd} not initialized'.format(cmd=cmd))
        except AttributeError as ae:
            print('Command  is not defined'.format(cmd=cmd))
        except IndexError as ie:
            print('To few arguments for {cmd}'.format(cmd=cmd))
        except SyntaxError as se:
            print('Invalid syntax')
        except Exception as e:
            print(e)
        else:
            ctrl.run('Group',cmd,par)
    
    def complete_group(self,text,line,begidx,endidx):                
        return self.getCompletions('group',line,text)
    
    def help_group(self):
        pass
        
    def do_backup(self,line):        
        arg = self.parseLine(line)
        try:
            if len(arg) == 0:
                 raise Exception('No command specified')      
            
            cmd = arg.pop(0)
                                               
            if cmd == 'add':                 
                par = {'name': arg.pop(0), 'description': arg.pop(0),'source': arg.pop(0),'destination': arg.pop(0), 'group': arg.pop(0) }                     
            elif cmd == 'update':
                par = {'name': arg.pop(0)}
                field = arg.pop(0)
                if field == 'name':    
                    values = {'name': arg.pop(0)}
                elif field == 'src':
                    values = {'source': arg.pop(0)}
                elif field == 'dest':
                    values = {'destination': arg.pop(0)}
                elif field == 'desc':
                    values = {'description': arg.pop(0)}
                elif field == 'group':
                    values = {'group': arg.pop(0)}
                elif field == 'expr':
                    values = ast.literal_eval(arg.pop(0))
                else:
                    raise Exception('Field {f} unknown'.format(f=field))              
                par['values'] = values
            elif cmd == 'delete':
                par = {'name': arg.pop(0)}                
            elif cmd == 'info':
                par = {'name': arg.pop(0)}
            elif cmd == 'list':
                par = {}
            elif cmd == 'run':
                par = {'name': arg.pop(0)}
            else:
                raise Exception('Command {cmd} not initialized'.format(cmd=cmd))
        except AttributeError as ae:
            print('Command  is not defined'.format(cmd=cmd))
        except IndexError as ie:
            print('To few arguments for {cmd}'.format(cmd=cmd))
        except SyntaxError as se:
            print('Invalid syntax')
        except Exception as e:
            print(e)
        else:
            ctrl.run('Backup',cmd,par)
    
    def complete_backup(self,text,line,begidx,endidx):
        return self.getCompletions('backup',line,text)
    
    def help_backup(self):
        pass
        
    def getCompletions(self,cmd,line,text):
        # text from line, because last argument is not completed
        if len(text) > 0:
            line = line.replace(text,'')
            
        cmdArgs = self.parseLine(line)
        
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
        else:
            completions = []
            
        completions = list(map(lambda s: '"'+ s + '"' if " " in s else s,completions))
        
        return completions
    
    def parseLine(self,line):
        arg = []       
        try:
            arg = shlex.split(line)
        except Exception as e:
            print('Error:',e)
        return arg
    
    def getBackupNames(self,arg):        
        if not self.groupNames:            
            bs = db.getDbObj('Backups');            
            self.backupNames = bs.getBackupNames();            
        return self.backupNames
        
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