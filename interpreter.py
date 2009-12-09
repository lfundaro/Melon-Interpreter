import re
from syntree import *
from Exceptions import *

#Definicion de estructura CLS

class CLS:
    def __init__(self,env,lista):
        self.env = env
        self.lista = lista
        
    def getLista(self):
        return self.lista

    def getEnv(self):
        return self.env

    def remplazar(self,cola):
        self.lista = cola

# def checkListaVac(nodo):
#     if re.match(nodo.tipo,'LISTAVACIA'):
#         return True
#     else:
#         return False

def match(n1, n2 = None):
    if isinstance(n2,int):
        return match(n1,NodoGen("ENTERO",str(n2)))
    elif isinstance(n2,str):
        return match(n1,NodoGen("LISTAVACIA",n2))
    elif n1.tipo == 'LISTAPATRON':
        return match(n1.hijo[0],n2)
    elif n2.tipo == 'LISTAPATRON':
        return match(n1,n2.hijo[0])
    elif n1.tipo == 'PATRON':
        return match(n1.hijo,n2)
    elif n2.tipo == 'PATRON':
        return match(n1,n2.hijo)
    elif n1.tipo == 'BOOLEANO' and n2.tipo == 'BOOLEANO':
        if n1.hijo == 'TRUE' and n2.hijo == 'TRUE':
            return True
        elif n1.hijo == 'FALSE' and n2.hijo == 'FALSE':
            return True
        else: 
            return False
    elif n1.tipo == 'LISTAVACIA' and n2.tipo == 'LISTAVACIA':
        return True
    elif n1.tipo == 'VARIABLE' or n2.tipo == 'VARIABLE':
        return True
    elif n1.tipo == 'LISTA' and n2.tipo == 'LISTA':
        return match(n1.hijo1,n2.hijo1) and match(n1.hijo2,n2.hijo2)
    elif n1.tipo == 'ENTERO' and n2.tipo == 'ENTERO':
        if n1.hijo == n2.hijo:
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
    if env.has_key(x):
        return env[x]
    else:
        return False

# Verificacion de que ambos parametros son numeros enteros.		
def is_int(x,y):
    if isinstance(x, int) and isinstance(y,int):
        return True
    else:
        return False
			
# Verificacion de que ambos parametros son booleanos	
def is_bool(x,y):
    if isinstance(x,bool) and isinstance(y,bool):
        return True
    else:
        return False
	
		
def eval(env,nodo,h=None):
    if h == None:
        if nodo.tipo == '':
            nodo = nodo.hijo
            return eval(env,nodo)
        elif nodo.tipo == 'PAREN':
            nodo = nodo.hijo
            return eval(env,nodo)
        elif nodo.tipo == 'LISTAVACIA':
            return nodo
        elif nodo.tipo == 'BOOLEANO':
            if nodo.hijo == 'TRUE':
                return True
            else:
                return False
        elif nodo.tipo == 'LISTA':
            return NodoBin('LISTA',eval(env,nodo.hijo1),eval(env,nodo.hijo2))
        elif nodo.tipo == 'MENOR':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                return x < y
            else:
                raise TypeError('En la operacion de mayor.')
        elif nodo.tipo == 'MAYOR':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                return x > y
            else:
                raise TypeError('En la operacion de menor.')
        elif nodo.tipo == 'NEGATIVO':
            x = eval(env,nodo.hijo2)
            if isinstance(x,int):
                return -x
        elif nodo.tipo == 'NO':
            x = eval(env,nodo.hijo2)
            if isinstance(x,bool):
                return (not x)
            else:
                raise TypeError('En la negacion')
        elif nodo.tipo == 'MENOROIGUAL':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                 return x <= y
            else:
                raise TypeError('En la operacion de menor o igual.')
        elif nodo.tipo == 'MAYOROIGUAL':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                    return  x >= y
            else:
                raise TypeError('En la operacion de mayor.')
        elif nodo.tipo == 'DISTINTO':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if (is_int(x,y)) or (is_bool(x,y)):
                return  x != y 
            else:
                raise TypeError('En la operacion de diferente.')
        elif nodo.tipo == 'IGUAL':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if (is_int(x,y)) or (is_bool(x,y)):
                    return  x == y
            else:
                raise TypeError('En la operacion de igualdad.')	
        elif nodo.tipo == 'ENTERO':
            return int(nodo.hijo)
        elif nodo.tipo == 'VARIABLE':
            if lookup(env,nodo.hijo): 
                return lookup(env,nodo.hijo)
            else:
                print 'ESTADO ENV'
                print env['sum'].lista
                print env['sum'].env
                raise LookUpError('Variable "' +str(nodo.hijo) + '" no declarada.')
        elif nodo.tipo == 'MAS':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                return x + y
            else:
                raise TypeError('En la operacion de suma.')
        elif nodo.tipo == 'MENOS':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                return x - y 
            else:
                raise TypeError('En la operacion de resta.')
        elif nodo.tipo == 'PRODUCTO':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                return x*y
            else:
                raise TypeError('En la operacion de producto.')
        elif nodo.tipo == 'COCIENTE':
            x = eval(env,nodo.hijo1) 
            y = eval(env,nodo.hijo2) 
            if is_int(x,y):
                if y == 0:
                    raise ZeroDivisionError('Division entre Cero.')
                else:
                    return x / y
            else:
                raise TypeError('En la operacion de division.')
        elif nodo.tipo == 'OR':
            x = eval(env,nodo.hijo1) 
            y = eval(env,nodo.hijo2) 
            if is_bool(x,y):
                return x or y
            else:
                raise TypeError('En or logico')
        elif re.match(nodo.tipo,'AND'):
            x = eval(env,nodo.hijo1) 
            y = eval(env,nodo.hijo2) 
            if is_bool(x,y):
                return x and y
            else:
                raise TypeError('En and logico')
        elif re.match(nodo.tipo,'PATRON'):
            return eval(env,nodo.hijo)
        elif re.match(nodo.tipo, 'IF'):
            if eval(env,nodo.hijo1):
                return eval(env, nodo.hijo2)
            else:
                return eval(env,nodo.hijo3)
        elif re.match(nodo.tipo,'LET'):
            env1 = extend(env,nodo.hijo1.hijo.hijo,'fake')
            v1 = eval(env1,nodo.hijo2)
            print replace(env1,nodo.hijo1.hijo.hijo,v1)
            print env
            return eval(replace(env1,nodo.hijo1.hijo.hijo,v1),nodo.hijo3)
        elif re.match(nodo.tipo,'FUN'):
            hijos = hijos_fun(nodo)
            tuplas = []
            for i in hijos: # i : NodoFunH
                if len(i.hijo1.hijo) > 1:
                    return True
                else:
                    tuplas.append((i.hijo1.hijo[0],i.hijo2)) # Se toma el unico hijo de NLP
            clausura = CLS(env,tuplas)
            return clausura
        elif re.match(nodo.tipo,'APLICAR'):
            return apply(eval(env,nodo.hijo1),eval(env,nodo.hijo2))
    else:
        return nodo

def hijos_fun(arb_fun):
    return arb_fun.hijo

def bajar(nodo):
    if isinstance(nodo,int):
        return nodo
    elif isinstance(nodo,str):
        return nodo
    elif re.match(nodo.tipo,'PATRON'):
        return bajar(nodo.hijo)
    elif re.match(nodo.tipo,'VARIABLE'):
        return bajar(nodo.hijo)

def apply(cls,v):
    if isinstance(cls,CLS):
        ltuplas = cls.getLista()
        head = ltuplas[0]
        if match(head[0],v):
            print 'HEAD 1'
            print head[1]
            print 'extend'
            print extend(cls.env,bajar(head[0]),v)
            return eval(extend(cls.env,bajar(head[0]),v),head[1])
        else:
            ltuplas = ltuplas[1:len(ltuplas)] # Cola de la lista
            cls.remplazar(ltuplas)
            if len(cls.lista) == 0:
                raise MatchingError('no hubo match con '+ str(v) )
            else:
                return apply(cls,v)
    else:
        raise MatchingError('no hubo match con '+ str(v))
                            

# #def apply(env,p1,p2):
# #    if isinstance(p1,CLS):
#         ltuplas = p1.getLista()
#         head = ltuplas[0]
#         if match(head[0],p2):
#            return eval(extend(env,head[0].hijo,p2),head[1])
#         else:
#             ltuplas = ltuplas[1:len(ltuplas)] # Cola de la lista
#             p1.remplazar(ltuplas)
#             if len(p1.lista) == 0:
#                 raise MatchingError('no hubo match con '+ str(p2) )
#             else:
#                 return apply(env,p1,p2)
#  #   else:
#   #      apply(env,eval(env,p1),eval(env,p2))
       
