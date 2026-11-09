"""Write or check the class maps of the samples (samples/*.classes).

A class map has the same lines as its sample. Whitespace is copied, and every
other character is replaced by the class of the token it belongs to:

    k  keyword: reserved keywords, true/false/null, prefix metadata (#Name)
    c  comment: notes (// ... and //* ... */)
    s  string: string literals and regular comments (/* ... */)
    n  number
    .  anything else (names, symbols)

The maps are generated from the Pygments lexers, which serve as the reference
for the other formats in this repository.

Usage: python classmap.py [--check]
"""

import os
import sys

from pygments.token import Comment, Keyword, Number, String

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from pygments_sysml.lexers import KerMLLexer, SysMLLexer  # noqa: E402

SAMPLES = os.path.join(os.path.dirname(__file__), '..', '..', 'samples')


def token_class(ttype):
    for parent, letter in ((Keyword, 'k'), (Comment, 'c'), (String, 's'),
                           (Number, 'n')):
        if ttype in parent:
            return letter
    return '.'


def classmap(text, lexer):
    out = []
    for ttype, value in lexer.get_tokens(text):
        letter = token_class(ttype)
        out.append(''.join(ch if ch.isspace() else letter for ch in value))
    return ''.join(out)


def samples():
    for name in sorted(os.listdir(SAMPLES)):
        if name.endswith('.sysml'):
            yield name, SysMLLexer
        elif name.endswith('.kerml'):
            yield name, KerMLLexer


def main(check):
    stale = []
    for name, lexer_class in samples():
        path = os.path.join(SAMPLES, name)
        with open(path, encoding='utf-8') as f:
            text = f.read()
        expected = classmap(text, lexer_class(stripnl=False, ensurenl=False))
        target = path + '.classes'
        if check:
            try:
                with open(target, encoding='utf-8') as f:
                    current = f.read()
            except FileNotFoundError:
                current = None
            if current != expected:
                stale.append(name)
        else:
            with open(target, 'w', encoding='utf-8', newline='\n') as f:
                f.write(expected)
    if stale:
        print('Out of date: ' + ', '.join(stale))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main('--check' in sys.argv[1:]))
