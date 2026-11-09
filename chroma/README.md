# Chroma

SysML v2 and KerML lexers for [Chroma](https://github.com/alecthomas/chroma)
v2, in its XML lexer format (the format of the lexers embedded in Chroma).

```go
lexer, err := chroma.NewXMLLexer(os.DirFS("."), "sysml.xml")
```

To make them available by name, register them with `lexers.Register(lexer)`.

`sysml.xml` and `kerml.xml` are generated from the Pygments lexers by
`build.py`; edit those, not the XML. The rules are the same as those generated
by Chroma's own `_tools/pygments2chroma_xml.py`; only the layout differs.

Tests: `go test ./...`.
