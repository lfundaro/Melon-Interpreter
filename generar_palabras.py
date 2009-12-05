#
#Esto es una adaptacion del programa del capitulo de NLP del libro AIMA
#de Rusell y Norvig para probar programas en MeLon. 
#
#Carlos Castillo (carlos.d.castillo@gmail.com), version 0.1,
#

from __future__ import generators
import operator, math, random, copy, sys, os.path, bisect

#______________________________________________________________________________
# Simple Data Structures: infinity, Dict, Struct
                
infinity = 1.0e400

def Dict(**entries):  
    """Create a dict out of the argument=value arguments. 
    >>> Dict(a=1, b=2, c=3)
    {'a': 1, 'c': 3, 'b': 2}
    """
    return entries

class DefaultDict(dict):
    """Dictionary with a default value for unknown keys."""
    def __init__(self, default):
        self.default = default

    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, copy.deepcopy(self.default))
    
    def __copy__(self):
        copy = DefaultDict(self.default)
        copy.update(self)
        return copy
    
class Struct:
    """Create an instance with argument=value slots.
    This is for making a lightweight object whose class doesn't matter."""
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __cmp__(self, other):
        if isinstance(other, Struct):
            return cmp(self.__dict__, other.__dict__)
        else:
            return cmp(self.__dict__, other)

    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)

def update(x, **entries):
    """Update a dict; or an object with slots; according to entries.
    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >>> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(x, dict):
        x.update(entries)   
    else:
        x.__dict__.update(entries) 
    return x 



# Grammars and Lexicons

def Rules(**rules):
    """Create a dictionary mapping symbols to alternative sequences.
    >>> Rules(A = "B C | D E")
    {'A': [['B', 'C'], ['D', 'E']]}
    """
    for (lhs, rhs) in rules.items():
        rules[lhs] = [alt.strip().split() for alt in rhs.split('|')]
    return rules

def Lexicon(**rules):
    """Create a dictionary mapping symbols to alternative words.
    >>> Lexicon(Art = "the | a | an")
    {'Art': ['the', 'a', 'an']}
    """
    for (lhs, rhs) in rules.items():
        rules[lhs] = [word.strip() for word in rhs.split('|')]
    return rules

class Grammar:
    def __init__(self, name, rules, lexicon):
        "A grammar has a set of rules and a lexicon."
        update(self, name=name, rules=rules, lexicon=lexicon)
        self.categories = DefaultDict([])
        for lhs in lexicon:
            for word in lexicon[lhs]:
                self.categories[word].append(lhs)

    def rewrites_for(self, cat):
        "Return a sequence of possible rhs's that cat can be rewritten as."
        return self.rules.get(cat, ())

    def isa(self, word, cat):
        "Return True iff word is of category cat"
        return cat in self.categories[word]

    def __repr__(self):
        return '<Grammar %s>' % self.name

Melon = Grammar('Melon',
    Rules(
      S = 'E',
      E = '''Booleano|Variable|Entero|Booleano|Variable|Entero|Booleano|Variable|Entero|
             Booleano|Variable|Entero|Booleano|Variable|Entero|Booleano|Variable|Entero|
             Booleano|Variable|Entero|Booleano|Variable|Entero|%[]%|
             E % E|E :: E|- E| E / E| E * E | E + E| E - E| ! E| E \/ E | E /\ E|E < E| E > E| 
             E <= E| E >= E| E = E| E <> E| %let P = E in E tel%| %fun PL -> E PLOP nuf%|%if E then E else E fi% 
             |%( E )% 
            ''',
      P = '''Booleano|Variable| P :: P| %( P )%
          ''',
      PLOP = '| & PL -> E PLOP',
      Digito = " 1 | 2 | 3|4 |5 | 6|7|8|9",
      EnteroI = "Digito | EnteroI Digito",
      Entero = "% EnteroI %",
      Letra = 'a|b|c|d|g|h|j|k|m|o|p|q|r|s|u|v|w|x|y|z',
      VariableI = 'Letra | VariableI Letra',
      Variable = '% VariableI %',
      PL = 'P | P PL',
      Booleano= ' %true%| %false%'
            ),
    Lexicon( 
    ))


def generate_random(grammar, s='S'):
    """Replace each token in s by a random entry in grammar (recursively).
    This is useful for testing a grammar, e.g. generate_random(E_)"""
    import random

    def rewrite(tokens, into,alpha):
        for token in tokens:
            if token in grammar.rules:
                try:
                    vl = alpha[token];
                except:
                    vl=9999;
                p = random.randint(0,len(grammar.rules[token])-1);
                q = [];
                ll = grammar.rules[token];
                if token=='E':
                    if (p>vl and ll[p]!='Booleano' and ll[p]!='Variable' and ll[p]!='Entero') or (p>=35 and p<40):
                        q= ['%('];
                        for item in ll[p]:
                            q.append(item)
                        q.append(')%')
                    else:
                        q = ll[p];
                else:
                    q = ll[p];

                alpha[token] = min(p,vl);
                rewrite(q, into,alpha)
            elif token in grammar.lexicon:
                into.append(random.choice(grammar.lexicon[token]))
            else:
                into.append(token)
        return into
    rv = ''.join(rewrite(s.split(), [],{})) 
    return rv.replace('%',' ').replace('&','|'); 

print generate_random(Melon)
