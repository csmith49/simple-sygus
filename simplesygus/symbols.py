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

# TODO
def interpret_sort(*args):
    pass
