/*
 * SysML v2 and KerML grammars for Prism (Prism.languages.sysml and
 * Prism.languages.kerml). Load this file after Prism.
 *
 * MIT License, see LICENSE in https://github.com/vincemolnar/sysmlv2-syntax-highlight
 */
(function (Prism) {
  'use strict';

  // KerML 1.1, 8.2.2.6, plus 'new' (used by the grammar, missing from the list)
  var KERML_KEYWORDS = [
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
    'unions', 'var', 'xor'
  ];

  // SysML 2.1, 8.2.2.1.2
  var SYSML_KEYWORDS = [
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
    'while', 'xor'
  ];

  var NAME = "(?:[A-Za-z_][A-Za-z0-9_]*|'(?:[^'\\\\\\r\\n]|\\\\.)*')";

  function grammar(keywords) {
    return {
      // Notes are ignored by the parser: comments. A regular comment is the
      // String-valued body of a comment, documentation or textual
      // representation: a string. Whichever starts first wins.
      'comment': [
        { pattern: /\/\/\*[\s\S]*?(?:\*\/|$)/, greedy: true },
        { pattern: /\/\/.*/, greedy: true }
      ],
      'string': [
        { pattern: /\/\*[\s\S]*?(?:\*\/|$)/, greedy: true },
        { pattern: /"(?:[^"\\\r\n]|\\.)*"?/, greedy: true }
      ],
      // Unrestricted names are names: no keywords inside.
      'unrestricted-name': { pattern: /'(?:[^'\\\r\n]|\\.)*'/, greedy: true },
      'keyword': [
        // Prefix metadata, a user-defined keyword (#Safety part ...).
        RegExp('#(?:\\$::)?' + NAME + '(?:::' + NAME + ')*'),
        RegExp('\\b(?:' + keywords.join('|') + ')\\b')
      ],
      'number': /(?<![A-Za-z0-9_])[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?|(?<!\.)\.[0-9]+(?:[eE][+-]?[0-9]+)?/,
      'punctuation': /::>|:>>|===|!==|::|:>|:=|\.\.|\.\?|->|=>|==|!=|<=|>=|\*\*|\?\?|@@|[(){}\[\];,~@#%&^|*+\-\/$.:<=>?!]/
    };
  }

  Prism.languages.sysml = grammar(SYSML_KEYWORDS);
  Prism.languages.kerml = grammar(KERML_KEYWORDS);
}(Prism));
