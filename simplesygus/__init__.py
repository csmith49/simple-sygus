from .sexp import clean_string, parse_sexp
from .scope import Scope
from .grammar import Grammar
from pta import Substitution, Term
from . import symbols

# this describes the problem to be solved --- the entire point of this module
class Problem(object):
    def __init__(self, cmd_list=None):
        # don't ever make function defaults mutable
        if cmd_list is None:
            cmd_list = []
        # our symbol table is a scope object
        self.symbol_table = Scope() << symbols.CORE
        # we'll hold on to the 'structure' of the synth function
        self.grammar = None
        # as well as a list of constraints
        self.constraints = []
        # and optional arguments
        self.options = {}
        # finally, step through the provided commands until we're done
        for cmd in cmd_list:
            self.update(cmd)
    # method by which we process commands
    def update(self, cmd):
        # a little introspection never hurt nobody
        inst, *args = cmd
        try:
            getattr(self, "_{f}".format(f=inst.replace('-', '_')))(*args)
        except AttributeError:
            raise Exception("{} not a recognized command".format(inst))
    # methods to execute individual commands
    def _set_logic(self, logic):
        # just pull the symbols for the appropriate theory
        functions = getattr(symbols, logic)
        self.symbol_table = self.symbol_table << functions
    def _declare_var(self, variable, sort):
        # interpret the sort string as an actual sort and construct a
        # universally-quantified variable
        z3_var = symbols.make_variable(variable, sort)
        self.symbol_table = self.symbol_table << (variable, z3_var)
    def _declare_fun(self, name, input_sorts, output_sort):
        # convert the input sorts and the output sort into z3 sort objects
        z3_inputs = list(map(symbols.interpret_sort, input_sorts))
        z3_output = symbols.interpret_sort(output_sort)
        # and then pull together an uninterpreted function
        z3_unfun = Function(name, *(z3_inputs + [z3_output]))
        self.symbol_table = self.symbol_table << (name, z3_unfun)
    def _define_fun(self, name, inputs, output_sort, sexp):
        # we'll turn the term/inputs combo into a function using substitutions
        input_variables, input_sorts = zip(*inputs)
        term = Term(sexp)
        def f(*args):
            sub = Substitution(zip(input_variables, args))
            return self.evaluate(term @ sub)
        self.symbol_table = self.symbol_table << (name, f)
    def _synth_fun(self, name, inputs, output_sort, grammar_sexps):
        input_variables, input_sorts = zip(*inputs)
        self.grammar = Grammar(name, input_variables, grammar_sexps)
        # note: at this point, you can't actually execute the synth fun
        self.symbol_table = self.symbol_table << (name, symbols.uninterpreted)
    def _constraint(self, sexp):
        self.constraints.append(Term(sexp))
    def _set_options(self, options):
        for key, value in options:
            self.options[key] = value
    def _check_synth(self):
        pass
    # of course, end of the day we need a way to convert our terms into things
    def evaluate(self, term):
        def valuation(t):
            # if it's not a term, just push it through
            if not isinstance(t, Term):
                return lambda: t
            # otherwise, handle the leaf case
            if t.is_leaf():
                # look for it in the symbol table
                if t.value in self.symbol_table.keys():
                    evaluated = self.symbol_table[t.value]
                # or convert it into a constant/strip it of Term
                else:
                    try: evaluated = symbols.interpret_constant(t.value)
                    except Exception as e:
                        evaluated = t.value # just a catch-all, hope it works
                return lambda: evaluated
            # now evaluating functions
            else:
                f = self.symbol_table[t.value]
                return lambda *args: f(*args)
        # now just evaluate
        return term.cata(valuation)
    # we need to turn terms into actual functions
    def _register_synth_fun(self, term):
        sf_name = self.grammar.name
        sf_inputs = self.grammar.input_variables
        def f(*args):
            sub = Substitution(zip(sf_inputs, args))
            return self.evaluate(term @ sub)
        self.symbol_table[sf_name] = f
    # and maybe pull them out as well
    def _unregister_synth_fun(self):
        sf_name = self.grammar.name
        self.symbol_table[sf_name] = symbols.uninterpreted
    # evaluate each constraint wrt the new candidate, then join them together
    def check_constraints(self, term):
        self._register_synth_fun(term)
        constraint = symbols.conjoin(*list(map(self.evaluate, self.constraints)))
        self._unregister_synth_fun()
        return constraint

# finally, provide a mechanism by which to load problem files
def load(filename):
    with open(filename, 'r') as f:
        data = f.read()
    cmds = parse_sexp(clean_string(data))
    return Problem(cmds)
