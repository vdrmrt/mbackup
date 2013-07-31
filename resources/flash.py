stack = []

def add(type,msg):
    stack.append({'type': type,'msg': msg})
    
def pop():
    return stack.pop()