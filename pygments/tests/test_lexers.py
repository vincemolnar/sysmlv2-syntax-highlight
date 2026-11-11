"""Tests for the SysML and KerML lexers and the Pilot style."""

import os
import sys

import pytest
from pygments.token import (Comment, Error, Keyword, Name, Number,
                            Punctuation, String, Text, Whitespace)

from pygments_sysml.lexers import (KERML_KEYWORDS, SYSML_KEYWORDS,
                                   KerMLLexer, SysMLLexer)
from pygments_sysml.styles import SysMLPilotStyle

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
SAMPLES = os.path.join(ROOT, 'samples')
SPEC = os.path.join(ROOT, 'spec')


def tokens(lexer, text, merge=True):
    """The tokens without whitespace, merging adjacent tokens of one type."""
    result = []
    adjacent = False
    for ttype, value in lexer.get_tokens(text):
        if ttype in Whitespace or (ttype is Text and not value.strip()):
            adjacent = False
            continue
        if merge and adjacent and result[-1][0] is ttype:
            result[-1] = (ttype, result[-1][1] + value)
        else:
            result.append((ttype, value))
        adjacent = True
    return result


@pytest.fixture(params=[SysMLLexer, KerMLLexer], ids=['sysml', 'kerml'])
def lexer(request):
    return request.param()


def spec_keywords(name):
    with open(os.path.join(SPEC, name), encoding='utf-8') as f:
        return [line.strip() for line in f
                if line.strip() and not line.startswith('#')]


def test_keyword_lists_match_the_specifications():
    assert list(SYSML_KEYWORDS) == spec_keywords('sysml-keywords.txt')
    assert list(KERML_KEYWORDS) == spec_keywords('kerml-keywords.txt')


def test_class_maps_are_up_to_date():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
    import classmap
    assert classmap.main(check=True) == 0


def test_each_notation_has_its_own_keywords():
    assert tokens(SysMLLexer(), 'part feature') == [
        (Keyword, 'part'), (Name, 'feature')]
    assert tokens(KerMLLexer(), 'part feature') == [
        (Name, 'part'), (Keyword, 'feature')]
    assert tokens(KerMLLexer(), 'new typed') == [
        (Keyword, 'new'), (Keyword, 'typed')]


def test_keywords_are_whole_words(lexer):
    assert tokens(lexer, "partition all_parts 'in'") == [
        (Name, 'partition'), (Name, 'all_parts'), (Name, "'in'")]


def test_literal_keywords(lexer):
    assert tokens(lexer, 'true false null') == [
        (Keyword.Constant, 'true'), (Keyword.Constant, 'false'),
        (Keyword.Constant, 'null')]


def test_prefix_metadata_is_a_keyword(lexer):
    assert tokens(lexer, "#Safety #A::'b c'::D") == [
        (Keyword, '#Safety'), (Keyword, "#A::'b c'::D")]


def test_hash_without_name_is_the_index_operator(lexer):
    assert tokens(lexer, 'seq#(1)') == [
        (Name, 'seq'), (Punctuation, '#('), (Number.Integer, '1'),
        (Punctuation, ')')]


def test_at_sign_is_punctuation(lexer):
    # Metadata usage (@Safety) and classification (x @ T) look alike.
    assert tokens(lexer, '@Safety; x @@ T') == [
        (Punctuation, '@'), (Name, 'Safety'), (Punctuation, ';'),
        (Name, 'x'), (Punctuation, '@@'), (Name, 'T')]


def test_notes_are_comments(lexer):
    assert tokens(lexer, 'a // note\n//* multi\nline */ b') == [
        (Name, 'a'), (Comment.Single, '// note'),
        (Comment.Multiline, '//* multi\nline */'), (Name, 'b')]


def test_regular_comments_are_strings(lexer):
    # The body of a comment, documentation or textual representation.
    assert tokens(lexer, "doc /* It's\n * text */ comment c /* x */") == [
        (Keyword, 'doc'), (String, "/* It's\n * text */"),
        (Keyword, 'comment'), (Name, 'c'), (String, '/* x */')]
    assert tokens(lexer, 'rep r language "alf" /* x = "y"; */') == [
        (Keyword, 'rep'), (Name, 'r'), (Keyword, 'language'),
        (String.Double, '"alf"'), (String, '/* x = "y"; */')]


def test_strings_and_escapes(lexer):
    assert tokens(lexer, r'"a\"b\\c\n" "d"') == [
        (String.Double, '"a'), (String.Escape, r'\"'),
        (String.Double, 'b'), (String.Escape, r'\\'),
        (String.Double, 'c'), (String.Escape, r'\n'),
        (String.Double, '"'), (String.Double, '"d"')]


def test_unclosed_string_ends_at_the_line_end(lexer):
    assert tokens(lexer, '"open\npart') [-1][1] == 'part'


def test_unrestricted_names(lexer):
    assert tokens(lexer, r"'Mass (kg)' 'it\'s'") == [
        (Name, "'Mass (kg)'"), (Name, r"'it\'s'")]


def test_numbers_and_ranges(lexer):
    assert tokens(lexer, '[0..*] [1..5] 3 .5 1.5 1.5e3 2E-3') == [
        (Punctuation, '['), (Number.Integer, '0'), (Punctuation, '..*]'),
        (Punctuation, '['), (Number.Integer, '1'), (Punctuation, '..'),
        (Number.Integer, '5'),
        (Punctuation, ']'), (Number.Integer, '3'),
        (Number.Float, '.5'), (Number.Float, '1.5'), (Number.Float, '1.5e3'),
        (Number.Float, '2E-3')]


@pytest.mark.parametrize('symbol', [
    '::>', ':>>', '===', '!==', '::', ':>', ':=', '..', '.?', '->', '=>',
    '==', '!=', '<=', '>=', '**', '??', '@@', '~', '$', ':', '<', '>', '=',
    '?', '%', '&', '^', '|', '*', '+', '-', '/'])
def test_symbols_are_single_tokens(lexer, symbol):
    assert list(lexer.get_tokens('a ' + symbol + ' b'))[2] == (
        Punctuation, symbol)


def test_longest_symbol_wins(lexer):
    # The example of KerML 8.2.2.7.
    assert [v for _, v in tokens(lexer, 'a:::b', merge=False)] == [
        'a', '::', ':', 'b']


@pytest.mark.parametrize('name', sorted(
    n for n in os.listdir(SAMPLES) if n.endswith(('.sysml', '.kerml'))))
def test_samples_lex_without_errors(name):
    lexer = KerMLLexer() if name.endswith('.kerml') else SysMLLexer()
    with open(os.path.join(SAMPLES, name), encoding='utf-8') as f:
        text = f.read()
    result = list(lexer.get_tokens(text))
    assert ''.join(v for _, v in result) == text
    assert [v for t, v in result if t is Error] == []


def test_pilot_style():
    style = SysMLPilotStyle.style_for_token
    assert style(Keyword)['bold'] and style(Keyword)['color'] == '7f0055'
    assert style(Keyword.Constant)['color'] == '7f0055'
    assert style(Comment.Single)['color'] == '3f7f5f'
    assert style(String.Double)['color'] == '2a00ff'
    assert style(String.Escape)['color'] == '2a00ff'
    # Regular comments (String) are plain in the Pilot.
    for plain in (String, Text, Name, Number.Float, Punctuation, Error):
        assert style(plain)['color'] is None and not style(plain)['bold']
