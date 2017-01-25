from .sexp import clean_string, parse_sexp
from .scope import Scope
from .sorts import interpret_sort
from . import symbols

# this describes the problem to be solved --- the entire point of this module
class Problem(object):
    def __init__(self, cmd_list=None):
        # don't ever make function defaults mutable
        if cmd_list is None:
            cmd_list = []
        # our s_table is a map from ids to Scopes
        self.symbol_table = {"init": Scope()}
        self.global_id = "init"
        # finally, step through the provided commands until we're done
        for cmd in cmd_list:
            self.update(cmd)
    # helpers for moving global around
    def globa_scope(self):
        return self.symbol_table[self.global_id]
    def update_global(self, fresh_scope):
        fresh_id = "{old}->ugs".format(old=self.global_id)
        fresh_global = self.global_scope() << fresh_scope
        self.symbol_table[fresh_id] = fresh_global
        self.global_id = fresh_id
    # method by which we process commands
    def update(self, cmd):
        # a little introspection never hurt nobody
        inst, *args = cmd
        try:
            getattr(self, "_{f}".format(f=inst.replace('-', '_')))(*args)
        except AttributeError:
            raise Exception()
    # methods to execute individual commands
    def _set_logic(self, logic):
        functions = getattr(symbols, logic)
        self.update_global(functions)
    def _declare_var(self, variable, sort):
        z3_var = Const(variable, symbols.interpret_sort(sort))
        self.update_global( (variable, z3_var) )
    def _declare_fun(self, name, input_sorts, output_sort):
        pass

# finally, provide a mechanism by which to load problem files
def load(filename):
    with open(filename, 'r') as f:
        data = f.read()
    cmds = parse_sexp(clean_string(data))
    return Problem(cmds)
