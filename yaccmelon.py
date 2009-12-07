#! /usr/bin/python
# -*- coding: utf-8 -*- 

####################################
# Integrantes:                     #
#     - Lorenzo Fundaro   06-39559 #
#     - Marion  Carambula 06-39312 #
####################################


###############################################################
# yaccmelon.py:                                               #
# En archivo se definen las precedencia de los tokens,        #
# cada una de las gramaticas asociada a cada token,  y        #
# se hace el parseo                                           #
###############################################################

import yacc as lexyacc
from syntree import *
from lexparam import *
import lex as lexmelon
from interpreter import *

# Precendencias de los Simbolos 
precedence = (
    ('left' , 'AND', 'OR') ,
    ('right', 'NOT'),
    ('nonassoc', 'DIFFERENT', 'LESSEREQ', 'LESSER', 'GREATEREQ','GREATER','EQUAL'), 
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDED'),
    ('right', 'DCOLON'),
    ('right', 'UMINUS'), 
    ('left' , 'APLICA'),
    ('nonassoc', 'TRUE', 'FALSE'), 
    )

## -- Definicion de las gramaticas para expresiones -- # 

# Definicion para expresiones aritmeticas
def p_expression_arit(p):
    '''expression :  expression PLUS expression
                  | expression TIMES expression
 		  | expression MINUS expression
                  | expression DIVIDED expression
		  '''
    if p[2] == '+':
        p[0] = NodoBin('MAS',p[1],p[3])
    elif p[2] == '*':
        p[0] = NodoBin('PRODUCTO',p[1], p[3])
    elif p[2] == '/':
        p[0] = NodoBin('COCIENTE',p[1], p[3])
    else: 
        p[0] = NodoBin('MENOS',p[1], p[3])


# Definicion para comparaciones
def p_expression_comp(p):
    '''expression :  expression DIFFERENT expression
		  |  expression EQUAL expression
		  |  expression LESSEREQ expression
		  |  expression GREATEREQ expression
		  |  expression LESSER expression
		  |  expression GREATER expression
		  '''
    if   p[2] == '<>':
        p[0] = NodoBin('DISTINTO', p[1], p[3])
    elif p[2] == '=':
        p[0] = NodoBin('IGUAL',p[1], p[3])
    elif p[2] == '<=':
        p[0] = NodoBin('MENOROIGUAL',p[1], p[3])
    elif p[2] == '>=':
        p[0] = NodoBin('MAYOROIGUAL',p[1], p[3])
    elif p[2] == '>':
        p[0] = NodoBin('MAYOR',p[1], p[3])
    elif p[2] == '<':
        p[0] = NodoBin('MENOR',p[1], p[3])

# Definicion para los numeros negativos
def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = NodoBin('NEGATIVO',None,p[2])

# Definicion para O logico
def p_expression_or(p):
    'expression : expression OR expression'
    p[0] = NodoBin('OR',p[1],p[3])

# Definicion para Y logico
def p_expression_and(p):
    'expression : expression AND expression'		  
    p[0] = NodoBin('AND',p[1], p[3])

    
# Definicion para las expresiones negadas
def p_expression_not(p):
    'expression : NOT expression'
    p[0] = NodoBin('NO',None,p[2])


# Definicion para lista de expresiones
def p_expression_list(p):
    'expression : expression DCOLON expression'
    p[0] = NodoBin('LISTA',p[1],p[3])


# Definicion de if
def p_expression_if(p):
    'expression : IF expression THEN expression ELSE expression FI'
    p[0] =  NodoLetIf('IF',p[2],p[4],p[6])     

# Definicion de let
def p_expression_let(p):
    'expression : LET p EQUAL expression IN expression TEL'
    p[0] =  NodoLetIf('LET',p[2],p[4],p[6])     


# Definicion de fun con una lista de patrones o con dos.
def p_expression_fun(p):
    '''expression : FUN lista ARROW expression NUF
		  | FUN lista ARROW expression PIPE fun_rec'''
    if p[5] != '|':
        # Verificacion del tamano de las listas de patrones
        p_aux = p[2]        # Devuelve Liston de patrones
        patrones = devolver(p_aux.getPack(),[])   # Lista aplanada de patrones
        NLP = NodoListaPatron('LISTAPATRON',patrones)  
        p[0] = NodoFunP('FUN',[NodoFunH(NLP,p[4])]) 
    else:
        # Verificacion del tamano de las listas de patrones
        p_aux = p[2]     # Devuelve Liston de patrones
        patrones = devolver(p_aux.getPack(),[])   # Lista aplanada patrones
        NLP = NodoListaPatron('LISTAPATRON',patrones)
        p_aux2 = p[6]    # Liston de Nodos FunH
        funciones = devolver(p_aux2.getPack(),[]) # Lista aplanada de Nodos FunH
        funciones.reverse()
        funciones = [NodoFunH(NLP,p[4])] + funciones
        check(funciones)   # Chequeo de balance en multiples parametros
        p[0] = NodoFunP('FUN',funciones) 


def p_expression_fun_rec(p):
    '''fun_rec : lista ARROW expression PIPE fun_rec
               | lista ARROW expression NUF'''
    if p[4] == '|':
        p_aux = p[1]    # Devuelve Liston de patrones 
        patrones = devolver(p_aux.getPack(),[])  # Lista aplanada de patrones
        NLP = NodoListaPatron('LISTAPATRON',patrones) 
        p[0] = Liston([p[5],NodoFunH(NLP,p[3])])
    else:
        p_aux = p[1]    # Devuelve Liston de patrones 
        patrones = devolver(p_aux.getPack(),[])  # Lista aplanada de patrones
        NLP = NodoListaPatron('LISTAPATRON',patrones)
        p[0] = Liston([NodoFunH(NLP,p[3])])


# Definicion de lista de patron recursiva.
def p_patron_lista_rec(p):
    'lista : lista p'
    p[0] = Liston([p[1],p[2]])


# Definicion de lista patron.
def p_patron_lista(p):
    'lista :  p'
    p[0] = Liston([p[1]]) 


# Cambio de terminal
def p_expression_e(p):
    'expression : e'
    p[0] = NodoGen('',p[1])


# Definicion de aplica
def p_e_aplica(p):
    'e : e e %prec APLICA'
    p[0] = NodoBin('APLICAR',p[1], p[2])


# Definicion para las numeros
def p_e_num(p):
    'e : NUMBER'
    p[0] = NodoGen("ENTERO",p[1])


# Definicion para las variables
def p_e_ID(p):
    'e : ID'
    p[0] = NodoGen("VARIABLE",p[1])


# Definicion para lista vacia
def p_e_listavac(p):
    'e : OBRAKET CBRAKET'
    p[0] = NodoGen("LISTAVACIA","[]")


# Definicion para las expresiones booleanas
def p_e_bool(p):
    '''e : TRUE
	 | FALSE'''
    p[0] = NodoGen('BOOLEANO',p[1].upper()) 



#Definicion para expresiones parentizadas
def p_e_parentesis(p):
    'e : OPAREN expression CPAREN'
    p[0] = NodoGen('PAREN',p[2]) 
    
# -- Definicion de gramaticas para patrones -- #

# Definicion de patron inicio.
def p_patron_ini(p):
    'p : patron'
    p[0] = NodoPatron('PATRON',p[1])

# Definicion de patron (numero). 
def p_patron_num(p):
    '''patron : NUMBER'''
    p[0] = NodoGen('ENTERO',p[1])
    
# Definicion de patron (booleano). 
def p_patron_bool(p):
    ''' patron : TRUE
	       | FALSE '''
    p[0] = NodoGen('BOOLEANO',p[1].upper())


# Definicion de patron (variable). 
def p_patron_ID(p):
    'patron : ID'
    p[0] = NodoGen('VARIABLE',p[1])

#Definicion para patrones parentizados
def p_patron_parentesis(p):
    'patron : OPAREN patron CPAREN'
    p[0] = NodoPatron('PATRON',p[2]) 


# Definicion para lista de patrones
def p_patron_list(p):
    '''patron : p DCOLON p'''
    p[0] = NodoBin('LISTA',p[1], p[3])


# Definicion para lista vacia
def p_patron_listavac(p):
    'patron : OBRAKET CBRAKET'
    p[0] = NodoGen("LISTAVACIA","[]")

# Definicion de errores
def p_error(p):
    raise SyntaxError(p)

# Se comienza el parseo
def beginParse(program):
    yacc = lexyacc.yacc()
    try:
        result = yacc.parse(program.read(),lexer = lexmelon.lex())
        print eval({},result)
    except SyntaxError, e:
        token = e.token
        if token:
            print 'Error de sintaxis en linea ' + str(token.lineno) \
                + ' cerca de token ' + '"' + str(token.value) + '"'
        else:
            print 'Error al final del programa'
    except TokenError, tk_error:
        token = tk_error.token
        print 'Token desconocido ' + '"'+ str(token.value.split()[0]).strip(' \n') + '"' \
            + ' en liea ' + str(token.lineno) + str(token.lexpos)
    except FunctionError, messag :
        messag = messag.messg
        print 'Error en funcion:' + messag
    except LookUpError, messag :
        messag = messag.messg
        print 'Error de LookUp: ' + messag
    except TypeError, messag :
        messag = messag.messg
        print 'Error de Tipos: ' + messag
    except ZeroDivisionError, messag:
        messag = messag.messg
        print 'Error: ' + messag


