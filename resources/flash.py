stack = []

def addError(msg,*args):
    add('error',msg,*args)

def addNotice(msg,*args):
    add('notice',msg,*args)

def add(type,msg,*args):
    msg = msg + ' ' + ' '.join(map(str,args))
    stack.append({'type': type,'msg': msg})
    
def pop():
    return stack.pop()