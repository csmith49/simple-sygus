from z3 import *

CORE = {
    "="         : (lambda a, b: a == b),
    'ite'		: If,
	'and'		: And,
	'or'		: Or,
	'not'		: Not,
	'xor'		: Xor,
    '=>'		: Implies,
    '_ID'		: (lambda a: a)
}

LIA = {
    '+'			: (lambda a, b: a + b),
	'-'			: (lambda a, b: a - b),
	'*'			: (lambda a, b: a * b),
    '<='		: (lambda a, b: a <= b),
	'>='		: (lambda a, b: a >= b),
	'>'			: (lambda a, b: a > b),
	'<'			: (lambda a, b: a < b)
}

BV = {
    'bvand'		: (lambda a, b: a & b),
    'bvor'		: (lambda a, b: a | b),
    'bvxor'		: (lambda a, b: a ^ b),
    'bvadd'		: (lambda a, b: a + b),
    'bvsub'		: (lambda a, b: a - b),
    'bvmul'		: (lambda a, b: a * b),
    'bvudiv'	: UDiv,
    'bvurem'	: URem,
    'bvlshr'	: LShR,
    'bvashr'	: (lambda a, b: a >> b),
    'bvshl'		: (lambda a, b: a << b),
    'bvsdiv'	: (lambda a, b: a / b),
    'bvsrem'	: SRem,
    'bvneg'		: (lambda a: -a),
    'bvnot'		: (lambda a: ~a),
    'bvugt'		: UGT,
    'bvuge'		: UGE,
    'bvule'		: ULE,
    'bvsle'		: (lambda a, b: a <= b),
    'bvult'		: ULT,
    'bvslt'		: (lambda a, b: a < b),
    'bvredor'	: (lambda a: Not(a == BitVecVal(0, a.sort().size())))
}

# just to make sure we don't try to use the synth fun before it's defined
def uninterpreted(*args):
    raise Exception

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
