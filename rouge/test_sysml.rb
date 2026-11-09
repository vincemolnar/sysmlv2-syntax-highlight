# frozen_string_literal: true

# Run with: ruby test_sysml.rb (Rouge must be on the load path)

require 'minitest/autorun'
require 'rouge'
require_relative 'sysml'

ROOT = File.expand_path('..', __dir__)
SAMPLES = File.join(ROOT, 'samples')

CLASSES = {
  'Keyword' => 'k', 'Comment' => 'c', 'Literal.String' => 's',
  'Literal.Number' => 'n'
}.freeze

def spec_keywords(file)
  File.readlines(File.join(ROOT, 'spec', file), chomp: true)
      .map(&:strip).reject { |line| line.empty? || line.start_with?('#') }
end

# The class map of a token stream (see pygments/scripts/classmap.py).
def classmap(lexer, text)
  lexer.lex(text).map do |token, value|
    prefix = CLASSES.keys.find { |p| token.qualname.start_with?(p) }
    letter = prefix ? CLASSES[prefix] : '.'
    value.gsub(/[^[:space:]]/, letter)
  end.join
end

class TestSysML < Minitest::Test
  def test_keyword_lists_match_spec
    assert_equal spec_keywords('sysml-keywords.txt'),
                 Rouge::Lexers::SysML.keywords.to_a.sort
    assert_equal spec_keywords('kerml-keywords.txt'),
                 Rouge::Lexers::KerML.keywords.to_a.sort
  end

  def test_lexers_are_registered
    assert_equal Rouge::Lexers::SysML, Rouge::Lexer.find('sysmlv2')
    assert_equal Rouge::Lexers::KerML, Rouge::Lexer.find('kerml')
  end

  Dir.children(SAMPLES).sort.each do |name|
    lexer_class = { '.sysml' => Rouge::Lexers::SysML,
                    '.kerml' => Rouge::Lexers::KerML }[File.extname(name)]
    next unless lexer_class

    define_method("test_#{name.tr('.', '_')}_matches_its_class_map") do
      text = File.read(File.join(SAMPLES, name), encoding: 'utf-8')
      expected = File.read(File.join(SAMPLES, "#{name}.classes"), encoding: 'utf-8')
      actual = classmap(lexer_class.new, text)
      expected.lines.zip(actual.lines).each_with_index do |(e, a), i|
        assert_equal e, a, "line #{i + 1}: #{text.lines[i]}"
      end
      assert_equal expected, actual
    end
  end
end
