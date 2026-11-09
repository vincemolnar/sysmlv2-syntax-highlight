# Prism

SysML v2 and KerML grammars for [Prism](https://prismjs.com/). Load
`prism-sysml.js` after Prism; it defines `Prism.languages.sysml` and
`Prism.languages.kerml`:

```html
<script src="prism.js"></script>
<script src="prism-sysml.js"></script>

<pre><code class="language-sysml">part def Drone;</code></pre>
```

In Node, set `global.Prism` before requiring the file:

```js
const Prism = require('prismjs');
global.Prism = Prism;
require('./prism-sysml.js');
const html = Prism.highlight(text, Prism.languages.sysml, 'sysml');
```

The grammars use the token names `keyword`, `comment`, `string`, `number` and
`punctuation`, which all Prism themes style, `prefix-metadata` (with the alias
`keyword`) for user-defined keywords such as `#Safety`, and `unrestricted-name`
for names in single quotes, which themes leave plain.

Tests: `npm install && npm test`.
