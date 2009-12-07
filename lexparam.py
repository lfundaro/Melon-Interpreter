#! /usr/bin/python
# -*- coding: utf-8 -*- 
from Exceptions import *

####################################
# Integrantes:                     #
#     - Lorenzo Fundaro   06-39559 #
#     - Marion  Carambula 06-39312 #
####################################

###############################################################
# lexparam.py:                                                #
# En este script se definiran las palabras reservadas         #
# los tokens, las reglas gramaticas para cada token,          #
# los caracteres ignorados y los errores.                     #
###############################################################

# Lista de palabras reservadas 
reserved = {
    'fun' : 'FUN',
    'nuf' : 'NUF',
    'let' : 'LET',
    'tel' : 'TEL',
    'in'  : 'IN',
    'if'  : 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi'  : 'FI',
    'true': 'TRUE',
    'false' : 'FALSE'   
    }

# Lista de tokens      
tokens = [
    'ID',      # Variables
    'NUMBER',
    'OBRAKET', # [
    'CBRAKET', # ]
    'DCOLON',  # ::
    'TIMES',  
    'DIVIDED',
    'PLUS',
    'MINUS',
    'DIFFERENT',
    'LESSEREQ',
    'LESSER',
    'GREATEREQ', 
    'GREATER', 
    'EQUAL',   
    'NOT',     
    'AND',     
    'OR',      
    'OPAREN',  # (
    'CPAREN',  # )
    'ARROW',   # ->
    'PIPE'     # |
    ] + list(reserved.values())

# Lista de las reglas para las expresiones regulares

# Definicion para la gramatica de las variables
def t_ID(t):
    r'\b[a-zA-Z][a-zA-Z0-9_]*\b'
    t.type = reserved.get(t.value,'ID') 
    return t

t_NUMBER = r'[0-9]+'
t_OBRAKET = r'\['
t_CBRAKET = r'\]'
t_DCOLON = r'::'
t_TIMES = r'\*'
t_DIVIDED = r'/'
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIFFERENT = r'<>'
t_LESSEREQ = r'<='
t_LESSER = r'<'
t_GREATEREQ = r'>='
t_GREATER = r'>'
t_EQUAL = r'='
t_NOT = r'!'
t_AND = r'/\\'
t_OR = r'\\/'
t_OPAREN = r'\('
t_CPAREN = r'\)'
t_ARROW = r'\->'
t_PIPE =  r'\|'

# Llevar seguimiento del numero de linea 

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados

t_ignore = ' \t\n'
            
# Error            
def t_error(t):
    raise TokenError(t) 
