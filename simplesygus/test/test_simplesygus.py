import simplesygus
import pta

# testing loading -- if this breaks, something is reallly bad
p = simplesygus.load("./examples/hd01.sl")
print("Problem statement loaded.")

# testing parsing constants
print("Testing constant parsing")
constants = ["#b01101010", "#x00000001", "true", "false", "143"]
for c in constants:
    print("\tTest constant: {}".format(c))
    print("\tEvaluated constant: {}".format(simplesygus.symbols.interpret_constant(c)))

# and now testing term evaluation
print("Testing evaluation and parsing")
terms = [
    ("(bvsub #x00000001 #x00000001)"),
    ("(hd01 #x00000001)")
]
for term in terms:
    print("\tS-expression: {}".format(term))
    t = pta.Term(simplesygus.parse_sexp(term))
    print("\tParsed term: {}".format(t))
    e = p.evaluate(t)
    print("\tEvaluated: {}".format(e))

# t = pta.Term("hd01", "#x0000001")
# print("Test term: {}".format(str(t)))
# print("Evaluation: {}".format(p.evaluate(t)))
