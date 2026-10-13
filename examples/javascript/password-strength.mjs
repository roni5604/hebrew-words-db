// Teach zxcvbn-ts about Hebrew so "שלום1234" and "akuo1234" are scored as weak.
//
//   npm i @zxcvbn-ts/core @zxcvbn-ts/language-common
//   node password-strength.mjs
//
// Hebrew users often type Hebrew words on an English layout (שלום -> "akuo"),
// so we add BOTH forms as dictionaries.

import { zxcvbn, zxcvbnOptions } from "@zxcvbn-ts/core";
import * as common from "@zxcvbn-ts/language-common";

const words = await fetch(
  "https://cdn.jsdelivr.net/gh/roni5604/hebrew-words-db@main/data/words.json"
).then((r) => r.json());

const HE = "/'קראטוןםפשדגכעיחלךף,זסבהנמצתץ.";
const EN = "qwertyuiopasdfghjkl;'zxcvbnm,./";
const toEnglishKeys = (w) => [...w].map((c) => EN[HE.indexOf(c)] ?? c).join("");

zxcvbnOptions.setOptions({
  graphs: common.adjacencyGraphs,
  dictionary: {
    ...common.dictionary,
    hebrew: words,
    hebrewOnEnglishKeyboard: words.map(toEnglishKeys),
  },
});

for (const pw of ["שלום1234", "akuo1234", "כיסא-ענן-מגדל-שוקולד"]) {
  const r = zxcvbn(pw);
  console.log(pw, "score:", r.score, "/ 4");
}
