import re

def match(n1, n2):
    if (re.match(n1.tipo,'BOOLEANO') and re.match(n2.tipo,'BOOLEANO')):
		if (re.match(n1.hijo,'TRUE') and re.match(n2.hijo,'TRUE')):
			return true
		elif (re.match(n1.hijo, 'FALSE') and re.match(n2.hijo,'FALSE'):
			return true
		elif: 
			return false
	elif (re.match(n1.tipo,'LISTAVACIA') and re.match(n2.tipo, 'LISTAVACIA'):
		return true
	
        
    
    
