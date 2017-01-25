from functools import wraps

# convenience exception, for pretty-printing of random parsing errors
class ParseException(Exception):
    def __init__(self, cmd, p):
        self._cmd = cmd
        self._p = p
    def __repr__(self):
        return "Can't parse {} with {}".format(self._cmd, self._p)

# keep a record of all parsers declared
PARSERS = {}

# since we're maintaining a record, we can use this to easily tag the parsers
def parser(p):
    def decorator(f):
        @wraps(f)
        def wrapped(cmd):
            try:
                return f(cmd)
            except:
                raise ParseException(cmd, p)
        PARSERS[p] = wrapped
        return wrapped
    return decorator

# and now getting the parsers is trivial
@parser("set-logic")
def parse_set_logic(cmd):
    return cmd[1]

@parser("define-sort")
def parse_sort_def(cmd):
    return cmd[1], cmd[2]

@parser("declare-var")
def parse_var_decl(cmd):
    return cmd[1], cmd[2]

@parser("declare-fun")
def parse_fun_decl(cmd):
    return cmd[1], cmd[2], cmd[3]

@parser("define-fun")
def parse_fun_def(cmd):
    return cmd[1], cmd[2], cmd[3], cmd[4]

@parser("synth-fun")
def parse_synth_fun(cmd):
    return cmd[1], cmd[2], cmd[3], cmd[4]

@parser("constraint")
def parse_constraint(cmd):
    return cmd[1]

@parser("check-synth")
def parse_check_synth(cmd):
    return True

@parser("set-options")
def parse_options(cmd):
    return cmd[1], cmd[2]
