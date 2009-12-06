import re
from syntree import *

def match(n1, n2):
    if re.match(n1.tipo,'BOOLEANO') and re.match(n2.tipo,'BOOLEANO'):
        if re.match(n1.hijo,'TRUE') and re.match(n2.hijo,'TRUE'):
            return True
        elif re.match(n1.hijo, 'FALSE') and re.match(n2.hijo,'FALSE'):
            return True
        else: 
            return False
    elif re.match(n1.tipo,'^LISTAVACIA$') and re.match(n2.tipo, '^LISTAVACIA$'):
        return True
    elif re.match(n1.tipo,'VARIABLE') or re.match(n2.tipo,'VARIABLE'):
        return True
    elif re.match(n1.tipo,'LISTA') and re.match(n2.tipo,'LISTA'):
        if match(n1.hijo1,n2.hijo1):
            if isinstance(n1.hijo2,NodoBin) and isinstance(n2.hijo2,NodoBin):
                return match(n1.hijo2,n2.hijo2)
            elif not isinstance(n1.hijo2,NodoBin) and not isinstance(n2.hijo2,NodoBin):
                if match(n1.hijo2,n2.hijo2):
                    return True
                else: 
                    return False
            else:
                return False
        else:
            return False
    elif re.match(n1.tipo,'ENTERO') and re.match(n2.tipo,'ENTERO'):
        if re.match(n1.hijo,n2.hijo):
            return True
        else:
            return False
    else:
        return False


def replace(env,x,y):
    env[x] = y
    return env

def extend(env,x,y):
    env[x] = y
    return env

def lookup(env,x):
    if env.has_key[x]:
        return env[x]
    else:
        return False

def eval(env,nodo):
    if re.match(nodo.tipo,''):
        nodo = nodo.hijo
        return eval(env,nodo)
    if re.match(nodo.tipo,'LISTAVACIA'):
        return '[]'
    elif re.match(nodo.tipo,'BOOLEANO'):
        return nodo.hijo
    elif re.match(nodo.tipo,'ENTERO'):
        return int(nodo.hijo)
    elif re.match(nodo.tipo,'VARIABLE'):
        return lookup(env,x)
    elif re.match(nodo.tipo,'MAS'):
        return eval(env,nodo.hijo1) + eval(env,nodo.hijo2) 
    elif re.match(nodo.tipo,'PRODUCTO'):
        return eval(env,nodo.hijo1) * eval(env,nodo.hijo2) 
    elif re.match(nodo.tipo,'COCIENTE'):
        x = eval(env,nodo.hijo1) 
        y = eval(env,nodo.hijo2) 
        if y == 0:
            raise ZeroDivisionError
        else:
            return x / y
    elif re.match(nodo.tipo,'LET'):
        
    

    


        
        
        
    
       

	
        
    
    
