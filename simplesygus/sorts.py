from pta import Term
from enum import Enum

Sorts = Enum("Sorts", "INT BOOL BV NA")

def parse_sort(sexp):
    if isinstance(sexp, (list, tuple)) and sexp[0] == "BitVec":
        return Sorts.BV
    elif sexp == "Int":
        return Sorts.INT
    elif sexp == "Bool":
        return Sorts.BOOL
    else:
        raise Exception("not a valid sort: {}".format(sexp))
