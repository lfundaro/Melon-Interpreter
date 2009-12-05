#! /usr/bin/python
# -*- coding: utf-8 -*- 

####################################
# Integrantes:                     #
#     - Lorenzo Fundaro   06-39559 #
#     - Marion  Carambula 06-39312 #
####################################

import lex as lexmelon
from lexparam import *
#

# Analizador lexicografico 
def startlex(input):
# Se crea el lexer 
    lexer = lexmelon.lex()
    tokenlist = []
    # Se obtiene la lista de tokens validos.
    for line in input:
        lexer.input(line)
        while True:
            tok = lexer.token()
            if not tok: break
            tokenlist.append(tok)

    return tokenlist
                        
