# Keywords

The reserved keywords of the two notations, one per line, as listed in the
specifications:

* `sysml-keywords.txt`: SysML 2.1 Beta 2 (Release 2026-07), 8.2.2.1.2
* `kerml-keywords.txt`: KerML 1.1 Beta 2 (Release 2026-07), 8.2.2.6, plus
  `new`, which the KerML grammar uses (`ConstructorExpression`) but the list
  omits

The tests of every format check their keyword lists against these files, and
`notepad++/build.py` generates the Notepad++ files from them.

The rest of the lexical structure (notes, regular comments, names, numbers,
strings and symbols) follows KerML 1.1, 8.2.2, which SysML shares.
