# Samples

Sample models that use every lexical construct of SysML v2 and KerML, and their
class maps. A class map (`<sample>.classes`) has the same lines as its sample;
whitespace is kept and every other character is replaced by its class:

| Letter | Class |
|---|---|
| `k` | keyword: reserved keywords, `true`/`false`/`null`, prefix metadata (`#Name`) |
| `c` | comment: notes (`// ...`, `//* ... */`) |
| `s` | string: string literals and regular comments (`/* ... */`) |
| `n` | number |
| `.` | anything else: names, symbols |

The class maps are generated from the Pygments lexers
(`python pygments/scripts/classmap.py`), and the tests of the other formats
compare their output with them.
