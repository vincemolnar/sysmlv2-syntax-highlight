# SysML v2 syntax highlighting

Syntax highlighting for the textual notations of the OMG Systems Modeling
Language (SysML) v2 and the Kernel Modeling Language (KerML), for several
highlighters:

| Folder | Highlighter | The highlighter is used by, for example |
|---|---|---|
| [`pygments`](pygments) | [Pygments](https://pygments.org/) | Sphinx, Material for MkDocs, Jupyter exports, LaTeX (`minted`), Leanpub |
| [`highlightjs`](highlightjs) | [highlight.js](https://highlightjs.org/) 11 | websites, Markdown renderers |
| [`prism`](prism) | [Prism](https://prismjs.com/) | websites, Docusaurus |
| [`rouge`](rouge) | [Rouge](https://github.com/rouge-ruby/rouge) | Jekyll, GitLab |
| [`chroma`](chroma) | [Chroma](https://github.com/alecthomas/chroma) | Hugo, Gitea |
| [`notepad++`](notepad++) | Notepad++ User Defined Language | Notepad++ |

Some of these platforms only use the lexers that ship with the highlighter, so
there a language has to be added upstream before it can be used.

These highlighters are a by-product of writing
[The SysML v2 Book](https://leanpub.com/sysmlv2), whose many textual models
needed them. They are shared here in the hope that they are useful beyond the
book.

## What is highlighted

All formats classify the text the same way:

| Text | Class |
|---|---|
| Reserved keywords (`part`, `def`, `specializes`, ...), `true`, `false`, `null` | keyword |
| User-defined keywords: prefix metadata such as `#Safety` | keyword |
| Notes: `// ...` and `//* ... */` | comment |
| Strings: `"..."` | string |
| Regular comments: `/* ... */` after `doc`, `comment`, `rep`, or on their own | string |
| Numbers: `42`, `1.5e3` | number |
| Names (`Drone`, `'Max. Speed'`), symbols and operators (`:>>`, `::`, `>=`) | plain |

Two choices are worth explaining:

* Notes and regular comments look alike, but the parser ignores only notes. A
  regular comment becomes the String-valued `body` of a comment, documentation
  or textual representation element, so it is part of the model, much like the
  `"..."` after `locale` or `language`. Notes are therefore shown as comments
  and regular comments as strings.
* Symbols are plain, so that keywords stand out, as in the specifications
  (which show keywords in bold) and in the SysML v2 Pilot Implementation.

The keywords are the reserved words of the specifications: SysML 2.1, 8.2.2.1.2,
and KerML 1.1, 8.2.2.6 (see [`spec`](spec)). SysML and KerML have different
reserved words, so every format has separate SysML and KerML definitions.

## Consistency

[`samples`](samples) contains sample models and, for each, a class map that
gives the class of every character. The models only illustrate the syntax; they
are not examples of good modeling practice. The class maps are generated from the
Pygments lexers. The tests of every other format highlight the samples with the
real highlighter and compare the result with the class maps character by
character. During development, all formats were also run on the 94 files of the
SysML v2 standard library (Pilot Implementation 0.63.0) and the 178 models of
*The SysML v2 Book*, and gave the same classes as the Pygments lexers on every
character.

The Notepad++ files cannot be tested this way; they are checked against the
schema of the Notepad++ UDL collection.

## Development

```sh
# Pygments (reference): tests, and the class maps of the samples
cd pygments && pip install . pytest && pytest
python scripts/classmap.py          # after changing the lexers

# Generated files: run after changing spec/ or the Pygments lexers
python notepad++/build.py
python chroma/build.py

cd highlightjs && npm install && npm test
cd prism && npm install && npm test
cd rouge && ruby -I <path to rouge>/lib test_sysml.rb
cd chroma && go test ./...
```

## Related projects

* The [SysML v2 Pilot Implementation](https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation/tree/master/tool-support/syntax-highlighting)
  generates TextMate grammars (VS Code), JetBrains file types and a Jupyter
  mode from its Xtext grammars.
* [daltskin/VSCode_SysML_Extension](https://github.com/daltskin/VSCode_SysML_Extension):
  VS Code extension with a TextMate grammar and a language server.
* [Open-MBEE/sysml-v2-textmate](https://github.com/Open-MBEE/sysml-v2-textmate):
  TextMate grammars for SysML and KerML.
* [mycr0ft/pygments-sysml](https://github.com/mycr0ft/pygments-sysml): another
  Pygments lexer, derived from an ANTLR grammar.
* [DeciSym/sysml-mode](https://github.com/DeciSym/sysml-mode): Emacs major mode.
* The [Notepad++ UDL collection](https://github.com/notepad-plus-plus/userDefinedLanguages)
  has a SysML v2 definition (`sysmlv2_omg_byaklira.xml`).

## License

MIT, see [LICENSE](LICENSE).
