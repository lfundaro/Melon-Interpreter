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

# def checkParen(nodo):
#     if re.match(nodo.tipo,'PAREN'):
#         return True
#     else:
#         return False

def checkListaVac(nodo):
    if re.match(nodo.tipo,'LISTAVACIA'):
        return True
    else:
        return False

def match(n1, n2 = None):
    if isinstance(n2,int):
        return match(n1,NodoGen("ENTERO",str(n2)))
    elif isinstance(n2,str):
        return match(n1,NodoGen("LISTAVACIA",n2))
    elif re.match(n1.tipo,'PATRON') and re.match(n2.tipo,'LISTA'):
        return match(n1.hijo, n2)
    elif re.match(n1.tipo,'BOOLEANO') and re.match(n2.tipo,'BOOLEANO'):
        if re.match(n1.hijo,'TRUE') and re.match(n2.hijo,'TRUE'):
            return True
        elif re.match(n1.hijo, 'FALSE') and re.match(n2.hijo,'FALSE'):
            return True
        else: 
            return False
    elif re.match(n1.tipo,'LISTA') and re.match(n2.tipo,'LISTA'):
        return match(n1.hijo1,n2.hijo1) and match(n1.hijo2,n2.hijo2)
	if  re.match(n1.tipo,'PATRON') or re.match(n1.tipo,'LISTAPATRON'):
        return match(n1.hijo,n2)
    if  re.match(n2.tipo,'PATRON') or re.match(n2.tipo,'LISTAPATRON'):
        return match(n1, n2.hijo)
    elif re.match(n1.tipo,'VARIABLE') or re.match(n2.tipo,'VARIABLE'):
        return True
    elif re.match(n1.tipo,'ENTERO'):
        return True
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
			
# Verificacion de que ambos parametros son string para false y true de MeLon.		
def is_string(x,y):
    if isinstance(x,str) and isinstance(y,str):
        return True
    else:
        return False
		
def eval(env,nodo,h=None):
    if h == None:
        if re.match(nodo.tipo,''):
            nodo = nodo.hijo
            return eval(env,nodo)
        elif re.match(nodo.tipo, 'PAREN'):
            nodo = nodo.hijo
            return eval(env,nodo)
        elif re.match(nodo.tipo,'LISTAVACIA'):
            return nodo
        elif re.match(nodo.tipo,'BOOLEANO'):
            return str(nodo.hijo).lower()
        elif re.match(nodo.tipo, 'MENOR'):
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                return str(x < y).lower()
            else:
                raise TypeError('En la operacion de mayor.')
        elif re.match(nodo.tipo, 'MAYOR'):
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                return str( x >y).lower()
            else:
                raise TypeError('En la operacion de menor.')
        elif re.match(nodo.tipo, 'NEGATIVO'):
            x = eval(env,nodo.hijo2)
            if isinstance(x,int):
                return -x
        elif re.match(nodo.tipo, 'MENOROIGUAL'):
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                 return str(x <= y).lower()
            else:
                raise TypeError('En la operacion de menor o igual.')
        elif re.match(nodo.tipo, 'MAYOROIGUAL'):
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                    return str( x >= y).lower()
            else:
                raise TypeError('En la operacion de mayor.')
        elif re.match(nodo.tipo, 'DISTINTO'):
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if (is_int(x,y)) or (is_string(x,y)):
                return str( x != y ).lower()
            else:
                raise TypeError('En la operacion de diferente.')
        elif re.match(nodo.tipo, 'IGUAL'):
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if (is_int(x,y)) or (is_string(x,y)):
                    return str( x == y).lower()
            else:
                raise TypeError('En la operacion de igualdad.')	
        elif re.match(nodo.tipo,'ENTERO'):
            return int(nodo.hijo)
        elif re.match(nodo.tipo,'VARIABLE'):
            if lookup(env,nodo.hijo):
                return lookup(env,nodo.hijo)
            else:
                raise LookUpError('Variable "' +str(nodo.hijo) + '" no declarada.')
        elif re.match(nodo.tipo,'MAS'):
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                return x + y 
            else:
                raise TypeError('En la operacion de suma.')
        elif re.match(nodo.tipo,'MENOS'):
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                return x - y 
            else:
                raise TypeError('En la operacion de resta.')
        elif re.match(nodo.tipo,'PRODUCTO'):
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y):
                return x*y
            else:
                raise TypeError('En la operacion de producto.')
        elif re.match(nodo.tipo,'COCIENTE'):
            x = eval(env,nodo.hijo1) 
            y = eval(env,nodo.hijo2) 
            if is_int(x,y):
                if y == 0:
                    raise ZeroDivisionError('Division entre Cero.')
                else:
                    return x / y
            else:
                raise TypeError
        elif re.match(nodo.tipo,'OR'):
            x = eval(env,nodo.hijo1) 
            y = eval(env,nodo.hijo2) 
            if not is_int(x,y):
                return str( x or y).lower()
            else:
                raise TypeError
        elif re.match(nodo.tipo,'AND'):
            x = eval(env,nodo.hijo1) 
            y = eval(env,nodo.hijo2) 
            if not is_int(x,y) and is_bool(x,y):
                return str(x and y).lower()
            else:
                raise TypeError
        elif re.match(nodo.tipo,'PATRON'):
            return eval(env,nodo.hijo)
        elif re.match(nodo.tipo,'LET'):
            env1 = extend(env,nodo.hijo1.hijo.hijo,'fake')
            v1 = eval(env1,nodo.hijo2)
            return eval(replace(env1,nodo.hijo1.hijo.hijo,v1),nodo.hijo3)
        elif re.match(nodo.tipo,'FUN'):
            hijos = hijos_fun(nodo)
            tuplas = []
            ################################
            # FALTA HACER LA CLAUSURA      #
            # MULTIPLE FUN X -> FUN Y -> Z #
            ################################
            for i in hijos: # i : NodoFunH
                for j in i.hijo1.hijo: # j : patrones en ListaPatron
                    tuplas.append((j.hijo,i.hijo2)) # tupla (patron,expr)
            clausura = CLS(env,tuplas)
            return clausura
        elif re.match(nodo.tipo,'APLICAR'):
            return apply(env,eval(env,nodo.hijo1),eval(env,nodo.hijo2))
    else:
        return nodo

def hijos_fun(arb_fun):
    return arb_fun.hijo

def apply(env,p1,p2):
    if isinstance(p1,CLS):
        ltuplas = p1.getLista()
        head = ltuplas[0]
        if match(head[0],p2):
            return eval(extend(env,head[0].hijo,p2),head[1])
        else:
           ltuplas = ltuplas[1:len(ltuplas)] # Cola de la lista
           p1.remplazar(ltuplas)
           if len(p1.lista) == 0:
               raise MatchingError('no hubo match con '+ str(p2) )
           else:
               return apply(env,p1,p2)
    else:
        apply(env,eval(env,p1),eval(env,p2))
        
