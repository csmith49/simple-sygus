A simple interface to the SyGuS benchmark file format, for Python 3 and z3.

Limitations:
* No support for let-bindings
* Only one call to `check-synth`
* Currently, only supports the theories `LIA` and `BV`
* Allowed sorts are integers, booleans, and bit-vectors
