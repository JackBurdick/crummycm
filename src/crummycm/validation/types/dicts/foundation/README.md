## Dict Types
If we imagine a truth table for known(1)/unknown(0) for Key/Values of dicts, the
following table describes the types of dicts possible

Key : value
1   :     1 - `KnownDict`
1   :     0 - `NamedDict`
0   :     1 - `UnnamedDict`
0   :     0 - `Unknown`