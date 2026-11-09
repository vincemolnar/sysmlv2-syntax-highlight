# highlight.js

SysML v2 and KerML grammars for [highlight.js](https://highlightjs.org/) 11.

In a web page, load `sysml.js` after highlight.js; it registers the languages
`sysml` and `kerml`:

```html
<script src="highlight.min.js"></script>
<script src="sysml.js"></script>
<script>hljs.highlightAll();</script>

<pre><code class="language-sysml">part def Drone;</code></pre>
```

In Node or a bundler, register them yourself:

```js
const hljs = require('highlight.js/lib/core');
const { sysml, kerml } = require('./sysml.js');
hljs.registerLanguage('sysml', sysml);
hljs.registerLanguage('kerml', kerml);
```

Automatic language detection is disabled for both languages: many of their
keywords (`if`, `import`, `def`, ...) are common in other languages, and
detection would otherwise pick SysML for code in those languages. Mark SysML code
blocks with `language-sysml` or `language-kerml`.

Tests: `npm install && npm test`.
