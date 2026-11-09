"""Generate the Chroma lexers (sysml.xml, kerml.xml) from the Pygments lexers.

Usage: python build.py [--check]

The Pygments lexers use only plain regular expressions, words(), token types,
and pushing or popping states, so the translation is direct. With --check,
nothing is written; the exit status is 1 if a file is out of date.
"""

import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'pygments'))

from pygments.lexer import RegexLexer, words  # noqa: E402
from pygments.token import _TokenType  # noqa: E402

from pygments_sysml.lexers import KerMLLexer, SysMLLexer  # noqa: E402

LEXERS = [('sysml.xml', SysMLLexer), ('kerml.xml', KerMLLexer)]


def pattern(regex):
    if isinstance(regex, words):
        return '%s(%s)%s' % (regex.prefix,
                             '|'.join(re.escape(w) for w in regex.words),
                             regex.suffix)
    if isinstance(regex, str):
        return regex
    raise ValueError('unsupported regex %r' % (regex,))


def token(ttype):
    if not isinstance(ttype, _TokenType):
        raise ValueError('unsupported action %r' % (ttype,))
    # Token.Literal.String.Double -> LiteralStringDouble
    return '<token type="%s"/>' % ''.join(ttype[:])


def state_change(new_state):
    if new_state == '#pop':
        return '<pop depth="1"/>'
    if isinstance(new_state, str) and not new_state.startswith('#'):
        return '<push state="%s"/>' % new_state
    raise ValueError('unsupported state change %r' % (new_state,))


def xml(lexer_class):
    assert issubclass(lexer_class, RegexLexer)
    lines = ['<lexer>', '  <config>',
             '    <name>%s</name>' % lexer_class.name]
    lines += ['    <alias>%s</alias>' % a for a in lexer_class.aliases]
    lines += ['    <filename>%s</filename>' % f for f in lexer_class.filenames]
    lines += ['    <mime_type>%s</mime_type>' % m for m in lexer_class.mimetypes]
    lines += ['  </config>', '  <rules>']
    for state, rules in lexer_class.tokens.items():
        lines.append('    <state name="%s">' % state)
        for rule in rules:
            body = token(rule[1])
            if len(rule) > 2:
                body += state_change(rule[2])
            lines.append('      <rule pattern="%s">%s</rule>'
                         % (html.escape(pattern(rule[0])), body))
        lines.append('    </state>')
    lines += ['  </rules>', '</lexer>', '']
    return '\n'.join(lines)


def main(check):
    stale = []
    for filename, lexer_class in LEXERS:
        path = os.path.join(HERE, filename)
        content = xml(lexer_class)
        if check:
            try:
                with open(path, encoding='utf-8') as f:
                    current = f.read()
            except FileNotFoundError:
                current = None
            if current != content:
                stale.append(filename)
        else:
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
    if stale:
        print('Out of date: ' + ', '.join(stale))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main('--check' in sys.argv[1:]))
