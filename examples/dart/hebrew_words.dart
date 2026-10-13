// Flutter / Dart: bundle the Hebrew word list as an asset.
//
// 1. Download words.json into assets/:
//    curl -sLo assets/he_words.json https://raw.githubusercontent.com/roni5604/hebrew-words-db/main/data/words.json
// 2. pubspec.yaml:
//    flutter:
//      assets:
//        - assets/he_words.json
// 3. Load once at startup (in an isolate so the UI never stutters):

import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

class HebrewWords {
  HebrewWords._(this.words) : _set = words.toSet();

  final List<String> words;
  final Set<String> _set;

  static const _finals = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'};
  static const _prefixes = 'והבכלמש';

  static Future<HebrewWords> load() async {
    final raw = await rootBundle.loadString('assets/he_words.json');
    final list = await compute(_decode, raw);
    return HebrewWords._(list);
  }

  static List<String> _decode(String raw) =>
      (jsonDecode(raw) as List).cast<String>();

  /// ם -> מ etc. Use for game tiles / matching, not for display.
  static String foldFinals(String w) =>
      w.split('').map((c) => _finals[c] ?? c).join();

  /// Known word? Peels up to three clitic prefixes (ו ה ב כ ל מ ש).
  bool isWord(String token) {
    var t = token.trim();
    if (_set.contains(t)) return true;
    for (var i = 0; i < 3 && t.length > 2 && _prefixes.contains(t[0]); i++) {
      t = t.substring(1);
      if (_set.contains(t)) return true;
    }
    return false;
  }

  List<String> ofLength(int n) => words.where((w) => w.length == n).toList();
}

// Usage:
//   final hebrew = await HebrewWords.load();
//   hebrew.isWord('שלום');      // true
//   hebrew.ofLength(5);         // Wordle answers
