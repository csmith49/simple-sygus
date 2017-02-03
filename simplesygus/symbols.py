from z3 import *
from .sorts import Sorts

class Symbol(object):
    def __init__(self, f, output):
        self.f = f
        self.output_sort = output
    def __call__(self, *args):
        try:
            return self.f(*args)
        except TypeError:
            return self.f

CORE = {
    "="         : Symbol(lambda a, b: a == b, Sorts.NA),
    'ite'		: Symbol(If, Sorts.NA),
	'and'		: Symbol(And, Sorts.BOOL),
	'or'		: Symbol(Or, Sorts.BOOL),
	'not'		: Symbol(Not, Sorts.BOOL),
	'xor'		: Symbol(Xor, Sorts.BOOL),
    '=>'		: Symbol(Implies, Sorts.BOOL)
}

LIA = {
    '+'			: Symbol(lambda a, b: a + b, Sorts.INT),
	'-'			: Symbol(lambda a, b: a - b, Sorts.INT),
	'*'			: Symbol(lambda a, b: a * b, Sorts.INT),
    '<='		: Symbol(lambda a, b: a <= b, Sorts.BOOL),
	'>='		: Symbol(lambda a, b: a >= b, Sorts.BOOL),
	'>'			: Symbol(lambda a, b: a > b, Sorts.BOOL),
	'<'			: Symbol(lambda a, b: a < b, Sorts.BOOL)
}

BV = {
    'bvand'		: Symbol(lambda a, b: a & b, Sorts.BV),
    'bvor'		: Symbol(lambda a, b: a | b, Sorts.BV),
    'bvxor'		: Symbol(lambda a, b: a ^ b, Sorts.BV),
    'bvadd'		: Symbol(lambda a, b: a + b, Sorts.BV),
    'bvsub'		: Symbol(lambda a, b: a - b, Sorts.BV),
    'bvmul'		: Symbol(lambda a, b: a * b, Sorts.BV),
    'bvudiv'	: Symbol(UDiv, Sorts.BV),
    'bvurem'	: Symbol(URem, Sorts.BV),
    'bvlshr'	: Symbol(LShR, Sorts.BV),
    'bvashr'	: Symbol(lambda a, b: a >> b, Sorts.BV),
    'bvshl'		: Symbol(lambda a, b: a << b, Sorts.BV),
    'bvsdiv'	: Symbol(lambda a, b: a / b, Sorts.BV),
    'bvsrem'	: Symbol(SRem, Sorts.BV),
    'bvneg'		: Symbol(lambda a: -a, Sorts.BOOL),
    'bvnot'		: Symbol(lambda a: ~a, Sorts.BOOL),
    'bvugt'		: Symbol(UGT, Sorts.BOOL),
    'bvuge'		: Symbol(UGE, Sorts.BOOL),
    'bvule'		: Symbol(ULE, Sorts.BOOL),
    'bvsle'		: Symbol(lambda a, b: a <= b, Sorts.BOOL),
    'bvult'		: Symbol(ULT, Sorts.BOOL),
    'bvslt'		: Symbol(lambda a, b: a < b, Sorts.BOOL),
    'bvredor'	: Symbol(lambda a: Not(a == BitVecVal(0, a.sort().size())), Sorts.BOOL)
}

# just to make sure we don't try to use the synth fun before it's defined
def bad(*args):
    raise Exception

uninterpreted = Symbol(bad, Sorts.NA)

# convert sexp sorts into z3 sorts
def interpret_sort(sexp):
    # case 1: it's an integer
    if sexp == "Int": return IntSort()
    # case 2: it's a bool
    elif sexp == "Bool": return BoolSort()
    # case 3: it might even be a real
    elif sexp == "Real": return RealSort()
    # case 4: check if it's a bitvector
    elif isinstance(sexp, (list, tuple)) and sexp[0] == "BitVec":
        return BitVecSort(int(sexp[1]))

# and create constants
def interpret_constant(value):
    # case 1: it's an integer
    try: return int(value)
    except: pass
    # case 2: boolean?
    if value == "true": return True
    elif value == "false": return False
    # case 3: bit-vectors
    elif value.startswith("#b"):
        bits = int(value[2:], 2)
        length = len(value) - 2
        return BitVecVal(bits, length)
    elif value.startswith("#x"):
        bits = int(value[2:], 16)
        length = (len(value) - 2) * 4
        return BitVecVal(bits, length)
    else:
        raise Exception("{} not a valid constant".format(value))

# construct a variable from a symbol and a sort -- avoids importing z3 in init
def make_variable(variable, sort):
    return Const(variable, interpret_sort(sort))

# we need to just AND somethings sometimes
def conjoin(*args):
    if len(args) == 1:
        return args[0]
    else:
        return And(args)

# because we have universal quantification
def quantify(vars, phi):
    return ForAll(vars, phi)

# and wrap a quick z3 call
def check_sat(formula):
    s = Solver()
    s.add(formula)
    return sat == s.check()
