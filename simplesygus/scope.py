class ScopeError(Exception):
    # one of the only reasons we subclass dicts below is so we can throw this
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg
    def __repr__(self):
        return str(self)

class Scope(dict):
    # represents a simple dictionary mapping symbols to things
    __slots__ = ()
    # how do we add new elements? we want this thing to be immutable
    def extend(self, d):
        fresh_scope = Scope()
        fresh_scope.update(self)
        # now, make sure there's no namespace clashes here
        if set(fresh_scope.keys()).isdisjoint(d.keys()):
            fresh_scope.update(d)
            return fresh_scope
        else:
            raise ScopeError("Forbidden namespace clash")
    # this is massive over-abuse of syntax, but we're just gonna go with it
    def __rlshift__(self, other):
        # case 1: other is a tuple
        if isinstance(other, tuple):
            return self.extend(dict([other]))
        # case 2, 3: other is a dictionary, scope
        elif isinstance(other, [dict, Scope]):
            return self.extend(other)
        # eh, just throw back the original
        else:
            return self
