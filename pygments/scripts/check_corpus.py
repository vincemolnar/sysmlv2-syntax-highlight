"""Lex SysML and KerML files and report problems and token statistics.

Usage: python check_corpus.py FILE... (or @LIST, a file with one path per line)

For every file: the tokens must reproduce the text exactly, and no token may
be an Error. The statistics list the token types and, per type, the most
frequent values, for reading.
"""

import collections
import sys

from pygments.token import Error

from pygments_sysml.lexers import KerMLLexer, SysMLLexer


def paths(args):
    for arg in args:
        if arg.startswith('@'):
            with open(arg[1:], encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        yield line.strip()
        else:
            yield arg


def main(args):
    counts = collections.Counter()
    values = collections.defaultdict(collections.Counter)
    files = problems = 0
    for path in paths(args):
        lexer_class = KerMLLexer if path.endswith('.kerml') else SysMLLexer
        lexer = lexer_class(stripnl=False)
        with open(path, encoding='utf-8-sig') as f:
            text = f.read()
        files += 1
        result = list(lexer.get_tokens(text))
        text = text.replace('\r\n', '\n')
        if ''.join(v for _, v in result) != text + (
                '' if text.endswith('\n') else '\n'):
            print('ROUND TRIP FAILS:', path)
            problems += 1
        opened = sum(1 for t, v in result if v in ('/*', '//*'))
        closed = sum(1 for t, v in result if v == '*/')
        if opened != closed:
            print('UNCLOSED COMMENT OR NOTE: %s (%d opened, %d closed)'
                  % (path, opened, closed))
        line = 1
        for ttype, value in result:
            if ttype in Error:
                print('ERROR TOKEN %s:%d: %r' % (path, line, value))
                problems += 1
            line += value.count('\n')
            counts[(lexer.name, str(ttype))] += 1
            if value.strip():
                values[(lexer.name, str(ttype))][value[:40]] += 1
    print('%d files, %d problems' % (files, problems))
    for key in sorted(counts):
        top = ', '.join('%s (%d)' % (v.replace('\n', '\\n'), n)
                        for v, n in values[key].most_common(12))
        print('%-5s %-28s %7d  %s' % (key[0], key[1], counts[key], top))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
