'use strict';
// Data: https://github.com/roni5604/hebrew-words-db (CC0-1.0). Code: MIT.
const words = require('./words.json');
let set = null;
const wordSet = () => set || (set = new Set(words));

module.exports = words;
module.exports.words = words;
module.exports.wordSet = wordSet;
module.exports.isWord = (w) => wordSet().has(String(w).trim());
module.exports.ofLength = (n) => words.filter((w) => w.length === n);
module.exports.startingWith = (p) => words.filter((w) => w.startsWith(p));
module.exports.randomWord = () => words[Math.floor(Math.random() * words.length)];
