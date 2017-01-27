from pta import Term

class Rule(object):
    def __init__(self, non_terminals, output, term):
        self.output = output
        self._input_positions = term.filter(lambda t: t.value in non_terminals)
        self.inputs = list(map(lambda p: (term | p).value, self._input_positions))
        self.term = term
    def evaluate(self, *args):
        output = self.term
        for arg, pos in zip(args, self._input_positions):
            output = output._replace(pos, arg)
        return output
    def __str__(self):
        return "{hd} -> {bdy}".format(hd=str(self.output), bdy=str(self.term))
    def __repr__(self):
        return str(self)

class Grammar(object):
    def __init__(self, name, input_variables, sexps):
        # we first need to find the non-terms
        self.name = name
        self.input_variables = input_variables
        self.non_terminals, _, _ = zip(*sexps)
        self.rules = []
        for output, _, productions in sexps:
            for prod in productions:
                self.rules.append(Rule(self.non_terminals, output, Term(prod)))
    def create_function(self, term):
        def f(*args):
            sub = Substitution(zip(self.input_variables, args))
            return term @ sub
        return f
    def __str__(self):
        return str(self.rules)
    def __repr__(self):
        return str(self)
    # TODO: add some utilities for expanding terms in the grammar
