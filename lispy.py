from __future__ import division
import math
import operator as op


# parse and tokenize
def parse(program_string):
    def atomize(token):
        # Numbers become numbers; every other token is a symbol
        try: return int(token)
        except ValueError:
            try: return float(token)
            except ValueError: return str(token)
    def parse_string(string): return program_string.replace('(', ' ( ').replace(')', ' ) ').split()
    def tokenize(tokens):
        if len(tokens) == 0: raise SyntaxError('unexpected EOF while reading')
        token = tokens.pop(0)
        if '(' == token:
            L = []
            while tokens[0] != ')':
                L.append(tokenize(tokens))
            tokens.pop(0)  # pop off ')'
            return L
        elif ')' == token: raise SyntaxError('unexpected )')
        else: return atomize(token)

    return tokenize(parse_string(program_string))


# a modified dictionary that can be connected
# to another dictionary (find check both dict)
class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        return self if (var in self) else self.outer.find(var)


# basic env initializing
def basic_env_initializing():
    "An environment with some Scheme standard procedures."
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, (int, float)),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, str),
    })
    return env

# creating the env
basic_env=basic_env_initializing()


# eval function
def eval(x, env=basic_env):
    if isinstance(x, str):
        return env.find(x)[x]
    elif not isinstance(x, list):
        return x
    elif x[0] == 'quote':
        (_, exp) = x
        return exp
    elif x[0] == 'cond':
        if len(x[1])==0: return False
        check = x[1].pop(0)
        exp = (check[1] if eval(check[0], env) else x)
        return eval(exp, env)
    elif x[0] == 'define':
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'set!':
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'lambda':
        (_, parms, body) = x
        return lambda *args: eval(body, Env(parms, args, env))
    else:
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)


# recursively turns python output into lisp output
def lisp_str(exp):
    if isinstance(exp, list): return '(' + ' '.join(map(lisp_str, exp)) + ')'
    else: return str(exp)


if __name__=="__main__":
    from sys import exc_info
    while True:
        try:
            val = eval(parse(input('lisp> ')))
            if val is not None: print(lisp_str(val))
        except: print(exc_info()[0])
