package chroma_test

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
	"unicode"

	"github.com/alecthomas/chroma/v2"
)

// classmap returns the class map of a text (see pygments/scripts/classmap.py).
func classmap(t *testing.T, lexer chroma.Lexer, text string) string {
	it, err := lexer.Tokenise(nil, text)
	if err != nil {
		t.Fatal(err)
	}
	var b strings.Builder
	for _, token := range it.Tokens() {
		letter := '.'
		switch {
		case token.Type.InCategory(chroma.Keyword):
			letter = 'k'
		case token.Type.InCategory(chroma.Comment):
			letter = 'c'
		case token.Type.InSubCategory(chroma.LiteralString):
			letter = 's'
		case token.Type.InSubCategory(chroma.LiteralNumber):
			letter = 'n'
		}
		for _, r := range token.Value {
			if unicode.IsSpace(r) {
				b.WriteRune(r)
			} else {
				b.WriteRune(letter)
			}
		}
	}
	return b.String()
}

func TestSamples(t *testing.T) {
	samples := filepath.Join("..", "samples")
	entries, err := os.ReadDir(samples)
	if err != nil {
		t.Fatal(err)
	}
	for _, entry := range entries {
		ext := filepath.Ext(entry.Name())
		if ext != ".sysml" && ext != ".kerml" {
			continue
		}
		t.Run(entry.Name(), func(t *testing.T) {
			lexer, err := chroma.NewXMLLexer(os.DirFS("."), ext[1:]+".xml")
			if err != nil {
				t.Fatal(err)
			}
			text, err := os.ReadFile(filepath.Join(samples, entry.Name()))
			if err != nil {
				t.Fatal(err)
			}
			expected, err := os.ReadFile(filepath.Join(samples, entry.Name()+".classes"))
			if err != nil {
				t.Fatal(err)
			}
			actual := strings.Split(classmap(t, lexer, string(text)), "\n")
			lines := strings.Split(string(text), "\n")
			for i, want := range strings.Split(string(expected), "\n") {
				if i >= len(actual) || actual[i] != want {
					t.Fatalf("line %d: %s", i+1, lines[i])
				}
			}
		})
	}
}
