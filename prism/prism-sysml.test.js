'use strict';

const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const Prism = require('prismjs');
global.Prism = Prism;
require('./prism-sysml.js');

const ROOT = path.join(__dirname, '..');
const SAMPLES = path.join(ROOT, 'samples');

const CLASSES = { keyword: 'k', comment: 'c', string: 's', number: 'n' };

function specKeywords(file) {
  return fs.readFileSync(path.join(ROOT, 'spec', file), 'utf8')
    .split('\n').map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#'));
}

function grammarKeywords(language) {
  const source = Prism.languages[language].keyword[1].source;
  return source.replace(/^\\b\(\?:/, '').replace(/\)\\b$/, '').split('|');
}

// The class map of a token stream (see pygments/scripts/classmap.py).
function classmap(tokens, type) {
  let out = '';
  for (const token of tokens) {
    if (typeof token === 'string') {
      for (const ch of token) {
        out += /\s/.test(ch) ? ch : (CLASSES[type] || '.');
      }
    } else {
      const content = Array.isArray(token.content) ? token.content : [token.content];
      out += classmap(content, token.type);
    }
  }
  return out;
}

test('keyword lists match spec/', () => {
  assert.deepStrictEqual(grammarKeywords('sysml'), specKeywords('sysml-keywords.txt'));
  assert.deepStrictEqual(grammarKeywords('kerml'), specKeywords('kerml-keywords.txt'));
});

for (const name of fs.readdirSync(SAMPLES)) {
  const language = path.extname(name).slice(1);
  if (language !== 'sysml' && language !== 'kerml') continue;
  test(`${name} matches its class map`, () => {
    const text = fs.readFileSync(path.join(SAMPLES, name), 'utf8');
    const expected = fs.readFileSync(path.join(SAMPLES, name + '.classes'), 'utf8');
    const actual = classmap(Prism.tokenize(text, Prism.languages[language]));
    const a = actual.split('\n');
    const e = expected.split('\n');
    for (let i = 0; i < Math.max(a.length, e.length); i++) {
      assert.strictEqual(a[i], e[i], `line ${i + 1}: ${text.split('\n')[i]}`);
    }
  });
}
