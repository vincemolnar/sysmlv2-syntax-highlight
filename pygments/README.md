# pygments-sysml

[Pygments](https://pygments.org/) lexers for the textual notations of the OMG
Systems Modeling Language (SysML) v2 and the Kernel Modeling Language (KerML).

| Lexer | Aliases | File names | MIME type |
|---|---|---|---|
| `SysMLLexer` | `sysml`, `sysml2`, `sysmlv2` | `*.sysml` | `text/x-sysml` |
| `KerMLLexer` | `kerml` | `*.kerml` | `text/x-kerml` |

## Installation and use

```sh
pip install pygments-sysml
pygmentize -l sysml -f html -O full -o model.html model.sysml
```

The package registers the lexers through Pygments' plugin entry points, so
`get_lexer_by_name('sysml')`, `get_lexer_for_filename('model.sysml')`,
`pygmentize -l sysml`, and tools built on Pygments (Sphinx, Material for MkDocs,
Jupyter's nbconvert, LaTeX `minted`) find them once the package is installed.
`pygments_sysml/lexers.py` has no dependencies besides Pygments and can also be
used on its own: `pygmentize -x -l lexers.py:SysMLLexer model.sysml`.

## Token types

| Text | Token type |
|---|---|
| Reserved keywords (`part`, `def`, `specializes`, ...) | `Keyword` |
| `true`, `false`, `null` | `Keyword.Constant` |
| User-defined keywords: prefix metadata such as `#Safety` | `Keyword` |
| Notes: `// ...` and `//* ... */` | `Comment.Single`, `Comment.Multiline` |
| Regular comments: `/* ... */` | `String` |
| Strings: `"..."` | `String.Double`, `String.Escape` |
| Numbers: `42`, `1.5e3` | `Number.Integer`, `Number.Float` |
| Names: `Drone`, `'Max. Speed'` | `Name` |
| Symbols and operators: `:`, `:>>`, `::`, `>=`, `@`, ... | `Punctuation` |

A regular comment is a string because the parser turns it into the
String-valued `body` of a comment, documentation or textual representation; only
notes are ignored. Symbols are punctuation so that keywords stand out.

The package also contains an optional style, `sysml-pilot`, with the colours of
the Eclipse editor of the SysML v2 Pilot Implementation:
`pygmentize -l sysml -f html -O full,style=sysml-pilot model.sysml`.

## Compatibility

The lexers use only `RegexLexer` and `words()`, available since Pygments 2.0. The
tests pass with Pygments 2.5.2, 2.11.2, 2.18.0 and 2.21.0.

## License

MIT, see [LICENSE](LICENSE).
