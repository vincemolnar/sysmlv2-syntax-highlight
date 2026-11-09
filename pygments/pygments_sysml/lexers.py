"""
    pygments_sysml.lexers
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for the textual notations of SysML v2 and KerML.

    The lexical structure follows KerML 1.1 subclause 8.2.2 (shared by SysML,
    see SysML 2.1 subclause 8.2.2.1.2). The classification of the tokens
    follows the Eclipse editor of the SysML v2 Pilot Implementation, except
    for regular comments:

    * reserved keywords and user-defined keywords (``#Name``, prefix
      metadata) are keywords;
    * notes (``// ...`` and ``//* ... */``) are comments;
    * regular comments (``/* ... */``) are strings: they are not ignored, but
      parsed into the String-valued ``body`` of a comment, documentation or
      textual representation, like the ``locale`` and ``language`` strings
      next to them (the Pilot shows them as plain text);
    * strings are strings, numbers are numbers, names are names;
    * all symbols, operators included, are punctuation.

    Compatible with Pygments 2.0 and later (tested with 2.5 to 2.21).

    :license: MIT, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, words
from pygments.token import (Comment, Keyword, Name, Number, Punctuation,
                            String, Whitespace)

__all__ = ['SysMLLexer', 'KerMLLexer']


#: Reserved keywords of KerML (KerML 1.1, 8.2.2.6), plus ``new``, which the
#: KerML grammar uses (ConstructorExpression) but the list omits.
KERML_KEYWORDS = (
    'about', 'abstract', 'alias', 'all', 'and', 'as', 'assoc', 'behavior',
    'binding', 'bool', 'by', 'chains', 'class', 'classifier', 'comment',
    'composite', 'conjugate', 'conjugates', 'conjugation', 'connector',
    'const', 'crosses', 'datatype', 'default', 'dependency', 'derived',
    'differences', 'disjoining', 'disjoint', 'doc', 'else', 'end', 'expr',
    'false', 'feature', 'featured', 'featuring', 'filter', 'first', 'flow',
    'for', 'from', 'function', 'hastype', 'if', 'implies', 'import', 'in',
    'inout', 'interaction', 'intersects', 'inv', 'inverse', 'inverting',
    'istype', 'language', 'library', 'locale', 'member', 'meta', 'metaclass',
    'metadata', 'multiplicity', 'namespace', 'new', 'nonunique', 'not',
    'null', 'of', 'or', 'ordered', 'out', 'package', 'portion', 'predicate',
    'private', 'protected', 'public', 'redefines', 'redefinition',
    'references', 'rep', 'return', 'specialization', 'specializes',
    'standard', 'step', 'struct', 'subclassifier', 'subset', 'subsets',
    'subtype', 'succession', 'then', 'to', 'true', 'type', 'typed', 'typing',
    'unions', 'var', 'xor',
)

#: Reserved keywords of SysML (SysML 2.1, 8.2.2.1.2; ``new`` was added by
#: SYSML21-11).
SYSML_KEYWORDS = (
    'about', 'abstract', 'accept', 'action', 'actor', 'after', 'alias', 'all',
    'allocate', 'allocation', 'analysis', 'and', 'as', 'assert', 'assign',
    'assume', 'at', 'attribute', 'bind', 'binding', 'by', 'calc', 'case',
    'comment', 'concern', 'connect', 'connection', 'constant', 'constraint',
    'crosses', 'decide', 'def', 'default', 'defined', 'dependency', 'derived',
    'do', 'doc', 'else', 'end', 'entry', 'enum', 'event', 'exhibit', 'exit',
    'expose', 'false', 'filter', 'first', 'flow', 'for', 'fork', 'frame',
    'from', 'hastype', 'if', 'implies', 'import', 'in', 'include',
    'individual', 'inout', 'interface', 'istype', 'item', 'join', 'language',
    'library', 'locale', 'loop', 'merge', 'message', 'meta', 'metadata',
    'new', 'nonunique', 'not', 'null', 'objective', 'occurrence', 'of', 'or',
    'ordered', 'out', 'package', 'parallel', 'part', 'perform', 'port',
    'private', 'protected', 'public', 'redefines', 'ref', 'references',
    'render', 'rendering', 'rep', 'require', 'requirement', 'return',
    'satisfy', 'send', 'snapshot', 'specializes', 'stakeholder', 'standard',
    'state', 'subject', 'subsets', 'succession', 'terminate', 'then',
    'timeslice', 'to', 'transition', 'true', 'until', 'use', 'variant',
    'variation', 'verification', 'verify', 'via', 'view', 'viewpoint', 'when',
    'while', 'xor',
)

#: Keywords that are literal values, emitted as Keyword.Constant.
LITERAL_KEYWORDS = ('false', 'null', 'true')

#: Symbols of KerML 8.2.2.7, plus ``@@`` (meta-classification), longest first.
SYMBOLS = (
    '::>', ':>>', '===', '!==',
    '::', ':>', ':=', '..', '.?', '->', '=>', '==', '!=', '<=', '>=', '**',
    '??', '@@',
    '(', ')', '{', '}', '[', ']', ';', ',', '~', '@', '#', '%', '&', '^', '|',
    '*', '+', '-', '/', '$', '.', ':', '<', '=', '>', '?',
)

BASIC_NAME = r'[A-Za-z_][A-Za-z0-9_]*'
UNRESTRICTED_NAME = r"'(?:[^'\\\n]|\\.)*'"
NAME = r'(?:%s|%s)' % (BASIC_NAME, UNRESTRICTED_NAME)
QUALIFIED_NAME = r'(?:\$::)?%s(?:::%s)*' % (NAME, NAME)


def _tokens(keywords):
    """The token definitions, shared by both notations except for the keywords."""
    other_keywords = tuple(k for k in keywords if k not in LITERAL_KEYWORDS)
    return {
        'root': [
            (r'\s+', Whitespace),
            # Notes are ignored by the parser: comments in the usual sense.
            (r'//\*', Comment.Multiline, 'multiline-note'),
            (r'//[^\n]*', Comment.Single),
            # A regular comment is the String-valued body of a comment,
            # documentation or textual representation: a string.
            (r'/\*', String, 'regular-comment'),
            (r'"', String.Double, 'string'),
            # Prefix metadata, a user-defined keyword (#Safety part ...).
            # A '#' that is not followed by a name is the index operator.
            (r'#' + QUALIFIED_NAME, Keyword),
            (words(LITERAL_KEYWORDS, prefix=r'\b', suffix=r'\b'),
             Keyword.Constant),
            (words(other_keywords, prefix=r'\b', suffix=r'\b'), Keyword),
            (BASIC_NAME, Name),
            (UNRESTRICTED_NAME, Name),
            # A real literal is DECIMAL_VALUE? '.' (DECIMAL_VALUE |
            # EXPONENTIAL_VALUE) | EXPONENTIAL_VALUE; "1..5" stays a range.
            (r'[0-9]*\.[0-9]+(?:[eE][+-]?[0-9]+)?', Number.Float),
            (r'[0-9]+[eE][+-]?[0-9]+', Number.Float),
            (r'[0-9]+', Number.Integer),
            (words(SYMBOLS), Punctuation),
        ],
        'multiline-note': [
            (r'[^*]+', Comment.Multiline),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'\*', Comment.Multiline),
        ],
        'regular-comment': [
            (r'[^*]+', String),
            (r'\*/', String, '#pop'),
            (r'\*', String),
        ],
        # Escapes as in the Pilot Implementation (KerML Table 4 plus \r).
        # Strings end at the line end (the spec allows printable characters
        # only), so an unclosed quote does not swallow the rest of the text.
        'string': [
            (r'[^"\\\n]+', String.Double),
            (r'\\[btnfr"\'\\]', String.Escape),
            (r'\\', String.Double),
            (r'"', String.Double, '#pop'),
            (r'\n', Whitespace, '#pop'),
        ],
    }


class SysMLLexer(RegexLexer):
    """
    Lexer for the textual notation of the OMG Systems Modeling Language
    (SysML) v2.
    """

    name = 'SysML'
    url = 'https://www.omg.org/spec/SysML/'
    aliases = ['sysml', 'sysml2', 'sysmlv2']
    filenames = ['*.sysml']
    mimetypes = ['text/x-sysml']

    tokens = _tokens(SYSML_KEYWORDS)

    _definition = re.compile(
        r'\b(?:part|item|action|attribute|port|state|requirement|constraint|'
        r'calc|connection|interface|allocation|occurrence|enum|metadata|'
        r'concern|case|analysis|verification|view|viewpoint|rendering|flow)'
        r'\s+def\s+[A-Za-z_\'<{]')

    def analyse_text(text):
        # "part def Name" and its siblings occur in no other language.
        if SysMLLexer._definition.search(text):
            return 0.5
        return 0.0


class KerMLLexer(RegexLexer):
    """
    Lexer for the textual notation of the OMG Kernel Modeling Language
    (KerML).
    """

    name = 'KerML'
    url = 'https://www.omg.org/spec/KerML/'
    aliases = ['kerml']
    filenames = ['*.kerml']
    mimetypes = ['text/x-kerml']

    tokens = _tokens(KERML_KEYWORDS)
