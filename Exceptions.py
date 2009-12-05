#! /usr/bin/python
# -*- coding: utf-8 -*- 

class TokenError(Exception):
    def __init__(self,token):
        self.token = token
        

class SyntaxError(Exception):
    def __init__(self,token):
        self.token = token

class FunctionError(Exception):
    def __init__(self,messg):
        self.messg = messg
    


