'use strict';

const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const hljs = require('highlight.js/lib/core');
const languages = require('./sysml.js');

hljs.registerLanguage('sysml', languages.sysml);
hljs.registerLanguage('kerml', languages.kerml);

const ROOT = path.join(__dirname, '..');
const SAMPLES = path.join(ROOT, 'samples');

const CLASSES = { keyword: 'k', literal: 'k', comment: 'c', string: 's', number: 'n' };
const ENTITIES = { lt: '<', gt: '>', amp: '&', quot: '"', '#x27': "'" };

function specKeywords(file) {
  return fs.readFileSync(path.join(ROOT, 'spec', file), 'utf8')
    .split('\n').map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#'));
}

// The class map of highlighted HTML (see pygments/scripts/classmap.py).
function classmap(html) {
  const scopes = [];
  let out = '';
  const re = /<span class="hljs-([\w-]+)">|<\/span>|&(lt|gt|amp|quot|#x27);|[^<&]/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[1] !== undefined) {
      scopes.push(m[1]);
    } else if (m[0] === '</span>') {
      scopes.pop();
    } else {
      const ch = m[2] !== undefined ? ENTITIES[m[2]] : m[0];
      const scope = scopes.length ? scopes[scopes.length - 1] : '';
      out += /\s/.test(ch) ? ch : (CLASSES[scope] || '.');
    }
  }
  return out;
}

test('keyword lists match spec/', () => {
  assert.deepStrictEqual(languages.SYSML_KEYWORDS, specKeywords('sysml-keywords.txt'));
  assert.deepStrictEqual(languages.KERML_KEYWORDS, specKeywords('kerml-keywords.txt'));
});

for (const name of fs.readdirSync(SAMPLES)) {
  const language = path.extname(name).slice(1);
  if (language !== 'sysml' && language !== 'kerml') continue;
  test(`${name} matches its class map`, () => {
    const text = fs.readFileSync(path.join(SAMPLES, name), 'utf8');
    const expected = fs.readFileSync(path.join(SAMPLES, name + '.classes'), 'utf8');
    const html = hljs.highlight(text, { language }).value;
    const actual = classmap(html);
    const a = actual.split('\n');
    const e = expected.split('\n');
    for (let i = 0; i < Math.max(a.length, e.length); i++) {
      assert.strictEqual(a[i], e[i], `line ${i + 1}: ${text.split('\n')[i]}`);
    }
  });
}
