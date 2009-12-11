#! /usr/bin/python
# -*- coding: utf-8 -*-

####################################
# Integrantes:                     #
#     - Lorenzo Fundaro   06-39559 #
#     - Marion  Carambula 06-39312 #
####################################


###############################################################
# syntree.py:                                                 #
# En este archivo se crea el arbol sintactico con diferente   #
# clases de nodos y se verifica la longitud de la lista       #
# de los patrones                                             #
###############################################################

from Exceptions import FunctionError

###################################################################
# NodoGen: Clase de nodo que consta de un solo hijo, usada para   #
# ingresar en el arbol sintactico los tokens VARIABLE, CONSTANTE, #
# NUMERO.                                                         #
###################################################################
class NodoGen:
        def __init__(self,tipo,hijo=None):
                if hijo == 'h':
                        self.tipo = tipo
                        self.hijo = '0'
                else:
                        self.tipo = tipo
                        self.hijo = hijo

        def __str__(self):
                if self.hijo:
                        if self.tipo == 'PAREN':
                                # Se imprime solo el hijo parentizado.
                                return '(' + str(self.hijo).strip() + ')'
                        elif self.tipo == '':
                                # Se imprime el hijo sin los parentesis
                                return str(self.hijo).strip()
                        else:
                                # Se imprime el tipo y el hijo parentizado.
                                return '(' + str(self.tipo).strip() + ' ' + str(self.hijo).strip() + ')'
                else:
                        # Se imprime solo el tipo (Caso de LISTAVACIA)
                        return '(' + str(self.tipo).strip() +  ')'
                                

###################################################################
# NodoBin: Clase de nodo que consta de dos hijos, usada para      #
# ingresar en el arbol sintactico los tokens binarios tales como  #
# SUMA, RESTA, MAYOROIGUAL, entre otros. Asi como tambien los     #
# tokens NO y NEGADO.                                             #
###################################################################
class NodoBin:
        def __init__(self,tipo,hijo1,hijo2):
                self.tipo = tipo
                self.hijo1 = hijo1
                self.hijo2 = hijo2
        def __str__(self):
                if self.hijo1:
                        # Se imprime el tipo y  ambos hijos
                        return '(' + str(self.tipo).strip() + ' ' + str(self.hijo1).strip() + ' ' + str(self.hijo2).strip() + ')'
                else:
                        # Se imprime solo el hijo derecho (Caso del NO y NEGADO)
                        return '(' + str(self.tipo).strip() + ' ' + str(self.hijo2).strip() + ')'

###################################################################
# NodoPatron: Clase de nodo que consta de un solo hijo usada para #
# ingresar en el arbol sintactico los tokens VARIABLE, CONSTANTE, #
# NUMERO.                                                         #
###################################################################
class NodoPatron:
        def __init__(self,tipo,hijo):
                self.tipo = tipo
                self.hijo = hijo

        def __str__(self):
                return '(' + str(self.tipo).strip() + ' ' + str(self.hijo).strip() + ')' + ' '
 
###################################################################
# NodoLetIf: Clase de nodo que consta de tres hijos, usada para   #
# ingresar en el arbol sintactico los tokens IF y let             #
###################################################################
class NodoLetIf:
        def __init__(self,tipo,hijo1,hijo2,hijo3):
                self.tipo = tipo
                self.hijo1 = hijo1
                self.hijo2 = hijo2
                self.hijo3 = hijo3

        def __str__(self):
                return '(' + str(self.tipo).strip() + ' ' + str(self.hijo1).strip() + ' ' + str(self.hijo2).strip() + ' ' + str(self.hijo3).strip() + ')'

 
#####################################################################
# NodoListaPatron: Clase de nodo que consta de un solo hijo, usada  #
# para ingresar en el arbol sintactico la lista de patrones         #
#####################################################################
class NodoListaPatron:
        def __init__(self,tipo,hijo):
                self.tipo = tipo
                self.hijo = hijo

        def __str__(self):
                a = ''
                for i in self.hijo:
                        a = a + str(i)
                return '(' + str(self.tipo).strip() + ' ' + a.strip() + ')'

        def getLista(self):
                return self.hijo
 
#####################################################################
# NodoFunP: Clase de nodo que representa la raiz del arbol funcion  #
# el cual consta de un solo hijo. Dicho hijo es una lista de nodos  #
# NodoFunH, los cuales representan los argumentos y las expresiones #
# de una funcion (e.g: p1 p2 -> e ).                                #
#####################################################################
class NodoFunP:
        def __init__(self,tipo,hijo):
                self.tipo = tipo
                self.hijo = hijo

        def __str__(self):
                a = ''
                for i in self.hijo:
                        a = a + str(i)
                return '(' + str(self.tipo).strip() + ' ' + a.strip() + ')'

 
#####################################################################
# NodoFunH: Clase de nodo que representa argumentos de una funcion  #
# (e.g: p1 p2 -> e). El nodo tiene dos hijos, el hijo1 es del tipo  #
# NodoListaPatron, mientras que el hijo2 es la expresion que corres-#
# ponde a la lista de patrones que se encuentran en hijo1           #
#####################################################################
class NodoFunH:
        def __init__(self,hijo1,hijo2):
                self.hijo1 = hijo1
                self.hijo2 = hijo2
                self.tipo = 'NodoFunH'
        
        def __str__(self):
                return str(self.hijo1).strip() + ' ' + str(self.hijo2).strip() + ' '


##############################################################
# Liston: Objeto que representa una lista de dos elementos,  #
# la cabeza de la lista es un objeto patron, y la cola       #  
# se define recursivamente como un objeto Liston.            #
# Esta estructura se usa para recolectar en las producciones # 
# recursivas como lista -> lista p , los objetos patrones    #
##############################################################
class Liston:
        def __init__(self,pack):
                self.pack = pack
                self.tipo = 'Liston'
        
        def getPack(self):
                return self.pack

 
##############################################################
# Devolver: Funcion que recibe un objeto Liston y lo aplana, #
# es decir, devuelve una lista simple con objetos Patron u   #
# objetos NodoFunH.                                          #
##############################################################
def devolver(pack,lista):
        if pack[0].tipo == 'Liston':       #Verificacion de tipo 
                lista.append(pack.pop())   #Saca un patron de la lista
                tail = pack.pop()          #Pido el objeto Liston de la lista
                pack = tail.getPack()      #Pido la lista asociada a Liston
                return devolver(pack,[]) + lista 
        else:
                return pack + lista
        

#######################################################################
# check: Funcion que recibe una lista de NodosFunH, busca en cada uno #
# de ellos las listas de patrones y compara sus tamanos. Cuando el    #
# tamano de una lista difiera con el de las otras listas se lanza una #
# excepcion que indica un desbalance en los parametros de una funcion #
#######################################################################
def check(funciones):
        z = len(funciones[0].hijo1.getLista()) #Longitud de lista del primer NodoFunH
        # Se itera sobre lista de funciones
        for i in funciones:
                x = len(i.hijo1.getLista())
                if x != z:      # Chequeo de longitudes
                        raise FunctionError(' parametros desbalanceados')


