from z3 import IntSort, BoolSort, BitVecSort

# classes for holding some basic info
class Const(object):
    def __init__(self, sort, val):
        self.sort = sort
        self.val = val

class Symb(object):
    def __init__(self, val):
        self.val = val

class Func(object):
    def __init__(self, val):
        self.val = val

# try to parse leaves into everything possible
def parse_leaf(sexp):
    try:
        return Const(IntSort(), int(sexp))
    except: pass

    if sexp == "true":
        return Const(BoolSort(), True)
    elif sexp == "false":
        return Const(BoolSort(), False)

    if sexp.startswith("#b"):
        bits = int(sexp[2:], 2)
        length = len(sexp) - 2
        return Const(BitVecSort(length), bits)
    elif sexp.startswith("#x"):
        bits = int(sexp[2:], 16)
        length = (len(sexp) - 2) * 4
        return Const(BitVecSort(length), bits)

    return Symb(sexp)

def parse_app(sexp):
    pass

def parse_sexp(sexp):
    pass
