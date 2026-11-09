# Rouge

SysML v2 and KerML lexers for [Rouge](https://github.com/rouge-ruby/rouge)
(tags `sysml` and `kerml`). Load `sysml.rb` after Rouge:

```ruby
require 'rouge'
require_relative 'sysml'

html = Rouge::Formatters::HTML.new.format(Rouge::Lexers::SysML.new.lex(text))
```

In a Jekyll site that builds its own plugins, put `sysml.rb` into `_plugins/`;
code blocks marked `sysml` or `kerml` are then highlighted. (GitHub Pages builds
without custom plugins only use the lexers that ship with Rouge.)

Tests: `ruby -I <path to rouge>/lib test_sysml.rb` (needs Rouge 4 or later).
