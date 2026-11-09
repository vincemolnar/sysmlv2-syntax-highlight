# -*- coding: utf-8 -*- #
# frozen_string_literal: true

# SysML v2 and KerML lexers for Rouge. Load this file after Rouge:
#
#   require 'rouge'
#   require_relative 'sysml'
#
# MIT License, see LICENSE in https://github.com/vincemolnar/sysmlv2-syntax-highlight

require 'set'

module Rouge
  module Lexers
    class SysML < RegexLexer
      # Lexical structure: KerML 1.1, 8.2.2; SysML 2.1, 8.2.2.1.2.

      title 'SysML'
      desc 'The textual notation of the OMG Systems Modeling Language v2 (https://www.omg.org/spec/SysML/)'

      tag 'sysml'
      aliases 'sysml2', 'sysmlv2'
      filenames '*.sysml'
      mimetypes 'text/x-sysml'

      # SysML 2.1, 8.2.2.1.2
      def self.keywords
        @keywords ||= Set.new %w(
          about abstract accept action actor after alias all allocate
          allocation analysis and as assert assign assume at attribute bind
          binding by calc case comment concern connect connection constant
          constraint crosses decide def default defined dependency derived do
          doc else end entry enum event exhibit exit expose false filter first
          flow for fork frame from hastype if implies import in include
          individual inout interface istype item join language library locale
          loop merge message meta metadata new nonunique not null objective
          occurrence of or ordered out package parallel part perform port
          private protected public redefines ref references render rendering
          rep require requirement return satisfy send snapshot specializes
          stakeholder standard state subject subsets succession terminate then
          timeslice to transition true until use variant variation
          verification verify via view viewpoint when while xor
        )
      end

      def self.literals
        @literals ||= Set.new %w(false null true)
      end

      name = %r/(?:[A-Za-z_][A-Za-z0-9_]*|'(?:[^'\\\n]|\\.)*')/

      state :root do
        rule %r/\s+/, Text

        # Notes are ignored by the parser: comments.
        rule %r(//\*), Comment::Multiline, :note
        rule %r(//[^\n]*), Comment::Single

        # A regular comment is the String-valued body of a comment,
        # documentation or textual representation: a string.
        rule %r(/\*), Str, :body
        rule %r/"/, Str::Double, :string

        # Prefix metadata, a user-defined keyword (#Safety part ...).
        rule %r/#(?:\$::)?#{name}(?:::#{name})*/, Keyword

        rule %r/[A-Za-z_][A-Za-z0-9_]*/ do |m|
          if self.class.literals.include?(m[0])
            token Keyword::Constant
          elsif self.class.keywords.include?(m[0])
            token Keyword
          else
            token Name
          end
        end

        rule %r/'(?:[^'\\\n]|\\.)*'/, Name

        # "1..5" is a range, not a real number.
        rule %r/[0-9]*\.[0-9]+(?:[eE][+-]?[0-9]+)?/, Num::Float
        rule %r/[0-9]+[eE][+-]?[0-9]+/, Num::Float
        rule %r/[0-9]+/, Num::Integer

        rule %r/::>|:>>|===|!==|::|:>|:=|\.\.|\.\?|->|=>|==|!=|<=|>=|\*\*|\?\?|@@|[(){}\[\];,~@#%&^|*+\-\/$.:<=>?]/, Punctuation
      end

      state :note do
        rule %r([^*]+), Comment::Multiline
        rule %r(\*/), Comment::Multiline, :pop!
        rule %r(\*), Comment::Multiline
      end

      state :body do
        rule %r([^*]+), Str
        rule %r(\*/), Str, :pop!
        rule %r(\*), Str
      end

      # Strings end at the line end, so an unclosed quote does not swallow
      # the rest of the text.
      state :string do
        rule %r/[^"\\\n]+/, Str::Double
        rule %r/\\[btnfr"'\\]/, Str::Escape
        rule %r/\\/, Str::Double
        rule %r/"/, Str::Double, :pop!
        rule %r/\n/, Text, :pop!
      end
    end

    class KerML < SysML
      title 'KerML'
      desc 'The textual notation of the OMG Kernel Modeling Language (https://www.omg.org/spec/KerML/)'

      tag 'kerml'
      filenames '*.kerml'
      mimetypes 'text/x-kerml'

      # KerML 1.1, 8.2.2.6, plus new (used by the grammar, missing from the list)
      def self.keywords
        @keywords ||= Set.new %w(
          about abstract alias all and as assoc behavior binding bool by
          chains class classifier comment composite conjugate conjugates
          conjugation connector const crosses datatype default dependency
          derived differences disjoining disjoint doc else end expr false
          feature featured featuring filter first flow for from function
          hastype if implies import in inout interaction intersects inv
          inverse inverting istype language library locale member meta
          metaclass metadata multiplicity namespace new nonunique not null of
          or ordered out package portion predicate private protected public
          redefines redefinition references rep return specialization
          specializes standard step struct subclassifier subset subsets
          subtype succession then to true type typed typing unions var xor
        )
      end
    end
  end
end
