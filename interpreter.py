
import re
from syntree import *
from Exceptions import *
import copy

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

def match(n1, n2 = None): 
    print 'N1'
    print n1
    print 'N2'
    print n2
    if isinstance(n1,bool):
        return match(n2,NodoGen("BOOLEANO",str(n1)))
    elif isinstance(n2,bool):
        return match(n1,NodoGen("BOOLEANO",str(n2)))
    if isinstance(n2,int)  and not isinstance(n2,bool):
        return match(n1,NodoGen("ENTERO",str(n2)))
    elif isinstance(n1,int) and not isinstance(n1,bool):
        return match(n2,NodoGen("ENTERO",str(n1)))
   # elif isinstance(n1,str):
   #     return match(n1,NodoGen("BOOLEANO",n1))
   # elif isinstance(n2,str):
   #     return match(n2,NodoGen("BOOLEANO",n2))
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
        print 'ENTRE'
        if n1.hijo == 'True' and n2.hijo == 'True':
            return True
        elif n1.hijo == 'False' and n2.hijo == 'False':
            return True
        else: 
            return False
    elif n1.tipo == 'LISTAVACIA' and n2.tipo == 'LISTAVACIA':
        return True
    elif n1.tipo == 'VARIABLE' or n2.tipo == 'VARIABLE':
        return True
    elif n1.tipo == 'LISTA' and n2.tipo == 'LISTA':
        return igualdad_listas([],n1,n2)
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
    if isinstance(y,bool):
        env[x] = str(y)
    else:
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
			
# Verificacion de que ambos parametros no son booleanos 
def no_bool(x,y):
    if not isinstance(x,bool) and not isinstance(y,bool):
        return True
    else:
        return False

# Verificacion de que ambos parametros son booleanos	
def is_bool(x,y):
    if  isinstance(x,bool) and isinstance(y,bool):
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
            if nodo.hijo == 'True':
                return True
            else:
                return False
        elif nodo.tipo == 'LISTA':
            k1 = eval(env,nodo.hijo1)
            k2 = eval(env,nodo.hijo2)
            if isinstance(k1,int) and not isinstance(k1,bool):
                nod1 = NodoGen('ENTERO',str(k1))
            elif isinstance(k1,bool):
                nod1 = NodoGen('BOOLEANO',str(k1))
            elif isinstance(k1,str):
                nod1 = NodoGen('LISTAVACIA',k1)
            else:
                nod1 = k1
            if isinstance(k2,int) and not isinstance(k2,bool):
                nod2 = NodoGen('ENTERO',str(k2))
            elif isinstance(k2,bool):
                nod2 = NodoGen('BOOLEANO',str(k2))
            elif isinstance(k2,str):
                nod2 = NodoGen('LISTAVACIA',k2)
            else:
                nod2 = k2
            return NodoBin('LISTA',nod1,nod2)

        elif nodo.tipo == 'MENOR':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y) and no_bool(x,y):
                return x < y
            else:
                raise TypeError('En la operacion de mayor.')
        elif nodo.tipo == 'MAYOR':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y) and no_bool(x,y):
                return x > y
            else:
                raise TypeError('En la operacion de menor.')
        elif nodo.tipo == 'NEGATIVO':
            x = eval(env,nodo.hijo2)
            if isinstance(x,int) and no_bool(x,y):
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
            if is_int(x,y) and no_bool(x,y):
                 return x <= y
            else:
                raise TypeError('En la operacion de menor o igual.')
        elif nodo.tipo == 'MAYOROIGUAL':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y) and no_bool(x,y):
                    return  x >= y
            else:
                raise TypeError('En la operacion de mayor.')
        elif nodo.tipo == 'DISTINTO':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if (is_int(x,y) and no_bool(x,y)):
                return  x != y 
            elif is_bool(x,y):
                return x != y
            else:
                raise TypeError('En la operacion de diferencia.')	
        elif nodo.tipo == 'IGUAL':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if (is_int(x,y) and no_bool(x,y)):
                return  x == y
            elif is_bool(x,y):
                return x == y
            #else:
            #    raise TypeError('En la operacion de igualdad.')	
        elif nodo.tipo == 'ENTERO':
            return int(nodo.hijo)
        elif nodo.tipo == 'VARIABLE':
           # if lookup(env,nodo.hijo): 
            return lookup(env,nodo.hijo)
            # else:
            #    raise LookUpError('Variable "' +str(nodo.hijo) + '" no declarada.')
        elif nodo.tipo == 'MAS':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            #if is_int(x,y) and no_bool(x,y):
            return x + y
            #else:
               # raise TypeError('En la operacion de suma.')
        elif nodo.tipo == 'MENOS':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            #if is_int(x,y) and no_bool(x,y):
            return x - y 
            #else:
             #   raise TypeError('En la operacion de resta.')
        elif nodo.tipo == 'PRODUCTO':
            x = eval(env,nodo.hijo1)
            y = eval(env,nodo.hijo2)
            if is_int(x,y) and no_bool(x,y):
                return x*y
            else:
                raise TypeError('En la operacion de producto.')
        elif nodo.tipo == 'COCIENTE':
            x = eval(env,nodo.hijo1) 
            y = eval(env,nodo.hijo2) 
            if is_int(x,y) and no_bool(x,y):
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
#            env1 = extend(copy.deepcopy(env),nodo.hijo1.hijo.hijo,'fake')
            env1 = extend(env,nodo.hijo1.hijo.hijo,'fake')
            v1 = eval(env1,nodo.hijo2)
            return eval(replace(env1,nodo.hijo1.hijo.hijo,v1),nodo.hijo3)
        elif re.match(nodo.tipo,'FUN'):
 #           print 'SERA'
            hijos = hijos_fun(nodo)
            tuplas = []
            for i in hijos: # i : NodoFunH
                if len(i.hijo1.hijo) > 1: # chequeo multiples valores
                    nueva_fun = transformar(nodo)
                    return eval(env,nueva_fun)
                else:
                    tuplas.append((i.hijo1.hijo[0],i.hijo2)) # Se toma el unico hijo de NLP
                    clausura = CLS(env,tuplas)
            return clausura
        elif re.match(nodo.tipo,'APLICAR'):
            return apply(eval(env,nodo.hijo1),eval(env,nodo.hijo2))
    else:
        return nodo

class PatExp:
    def __init__(self,lista,exp):
        self.lista = lista
        self.exp = exp


def getPatrones(hijos):
    ref = []
    for i in hijos:
        patexp = PatExp([],None)        
        for j in i.hijo1.hijo:
            patexp.lista.append(j)
        patexp.exp = i.hijo2
        ref.append(patexp)
    return ref
    
def transformar(nodofun):
    # Se obtienen los patrones
    patrones = getPatrones(nodofun.hijo)
    # Se agrega el primer elemento de patron
    length = len(patrones[0].lista)
    nuevoarb = NodoFunP('FUN',[NodoFunH(NodoListaPatron('LISTAPATRON',[patrones[0].lista[0]]),NodoFunP('FUN',[NodoFunH(NodoListaPatron('LISTAPATRON',patrones[0].lista[1:length]),patrones[0].exp)]))]) #p
    for i in range(len(patrones)):
        if i == len(patrones)-1:
            break
        else:
            if match(patrones[0].lista[0],patrones[i+1].lista[0]):
                # Se lo agrego al hijo del primer hijo de p 
                nuevoarb.hijo[0].hijo2.hijo.append(NodoFunH(NodoListaPatron('LISTAPATRON',patrones[i+1].lista[1:length]),patrones[i+1].exp))
            else:
                nuevoarb.hijo.append(NodoFunH(NodoListaPatron('LISTAPATRON',[patrones[i+1].lista[0]]),NodoFunP('FUN',[NodoFunH(NodoListaPatron('LISTAPATRON',patrones[i+1].lista[1:length]),patrones[i+1].exp)])))
                
    return nuevoarb


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

def igualdad_listas(lista,a,b):
    if match(a.hijo1,b.hijo1):
        lista.append((bajar(a.hijo1),b.hijo1))
        if a.hijo2.tipo == 'LISTA' and b.hijo2.tipo == 'LISTA':
            igualdad_listas(lista,a.hijo2,b.hijo2)
        elif a.hijo2.tipo != 'LISTA' and b.hijo2.tipo == 'LISTA':
            if match(a.hijo2,b.hijo2):
                lista.append((bajar(a.hijo2),b.hijo2))
            else:
                lista = []
        else:
            if match(a.hijo2,b.hijo2):
                lista.append((bajar(a.hijo2),b.hijo2))
            else:
                lista = []
        if lista == []: return False
        return lista
    else:
        lista = []
        return False
            
def apply(cls,v):
    if isinstance(cls,CLS):
        ltuplas = cls.getLista()
        head = ltuplas[0]
        print 'CLS'
        if isinstance(match(head[0],v),list):
            b = match(head[0],v)
            for i in range(len(b)):
                cls.env[b[i][0]] = b[i][1]
            return eval(extend(copy.deepcopy(cls.env),bajar(head[0]),v),head[1])
        if match(head[0],v):   
            return eval(extend(copy.deepcopy(cls.env),bajar(head[0]),v),head[1])
        else:
            ltuplas = ltuplas[1:len(ltuplas)] # Cola de la lista
            cls_cola = CLS(cls.env,ltuplas)
            if len(cls_cola.lista) == 0:
                raise MatchingError('no hubo match con '+ str(v) + str(head[0]))
            else:
                return apply(cls_cola,v)
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
       
