// Hebrew word list helpers for Node 18+ and modern browsers (ES module, no deps).
//
//   import { loadWords, isWord, fixLayout, autocomplete } from "./hebrew-words.mjs";
//   const words = await loadWords();
//   isWord("ומהבית");              // true  (clitic prefixes peeled)
//   fixLayout("akuo nv akunl");    // "שלום מה שלומך"
//   autocomplete("מחש", 5);        // ["מחשב", "מחשבה", ...]
//
// Data: https://github.com/roni5604/hebrew-words-db (CC0-1.0). Code: MIT.

const URL = "https://cdn.jsdelivr.net/gh/roni5604/hebrew-words-db@main/data/words.json";

let WORDS = [];
let SET = new Set();

export async function loadWords(url = URL) {
  if (WORDS.length) return WORDS;
  WORDS = await fetch(url).then((r) => r.json());
  SET = new Set(WORDS);
  return WORDS;
}

const MARKS = /[֑-ׇ'"׳״‎‏]/g;
export const clean = (s) => s.replace(MARKS, "").trim();

const FINALS = { "ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ" };
export const foldFinals = (w) => w.replace(/[ךםןףץ]/g, (c) => FINALS[c]);

const PREFIXES = "והבכלמש";

/** Known word? Peels up to three clitic prefixes (ו ה ב כ ל מ ש). */
export function isWord(token) {
  let t = clean(token);
  if (SET.has(t)) return true;
  for (let i = 0; i < 3 && t.length > 2 && PREFIXES.includes(t[0]); i++) {
    t = t.slice(1);
    if (SET.has(t)) return true;
  }
  return false;
}

/** Prefix autocomplete with binary search over the sorted list. */
export function autocomplete(prefix, limit = 10) {
  const p = clean(prefix);
  let lo = 0, hi = WORDS.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (WORDS[mid] < p) lo = mid + 1; else hi = mid;
  }
  const out = [];
  for (let i = lo; i < WORDS.length && WORDS[i].startsWith(p) && out.length < limit; i++) out.push(WORDS[i]);
  return out;
}

// Standard Israeli keyboard layout (SI-1452).
const EN = "qwertyuiopasdfghjkl;'zxcvbnm,./";
const HE = "/'קראטוןםפשדגכעיחלךף,זסבהנמצתץ.";
const EN2HE = Object.fromEntries([...EN].map((c, i) => [c, HE[i]]));

/** "akuo" -> "שלום" when the result is mostly real Hebrew words, else null. */
export function fixLayout(text, threshold = 0.6) {
  const converted = [...text.toLowerCase()].map((c) => EN2HE[c] ?? c).join("");
  const tokens = converted.split(/\s+/).map((t) => t.replace(/[.,/']/g, "")).filter(Boolean);
  if (!tokens.length) return null;
  const hits = tokens.filter(isWord).length;
  return hits / tokens.length >= threshold ? converted : null;
}

/** Five-letter words for a Hebrew Wordle (compare with foldFinals). */
export const wordleWords = () => WORDS.filter((w) => w.length === 5);

// Demo when run directly: node hebrew-words.mjs
if (typeof process !== "undefined" && import.meta.url === `file://${process.argv[1]}`) {
  await loadWords();
  console.log(WORDS.length, "words");
  console.log(isWord("ומהבית"), fixLayout("akuo nv akunl"), autocomplete("מחש", 5));
}
