# hebrew-wordlist

The largest public-domain (CC0) list of Hebrew words — 131,000+ words including plurals, verb conjugations and adjective forms. Zero dependencies. Data from [github.com/roni5604/hebrew-words-db](https://github.com/roni5604/hebrew-words-db).

```bash
npm install hebrew-wordlist
```

```js
const hebrew = require('hebrew-wordlist');

hebrew.length;              // 131000+
hebrew.isWord('שלום');      // true
hebrew.ofLength(5);         // five-letter words (Hebrew Wordle)
hebrew.startingWith('מח');  // prefix search
hebrew.randomWord();
```

No install needed in the browser:

```js
const words = await fetch('https://cdn.jsdelivr.net/gh/roni5604/hebrew-words-db@main/data/words.json').then(r => r.json());
```

Word data: CC0-1.0 (public domain). Code: MIT.
