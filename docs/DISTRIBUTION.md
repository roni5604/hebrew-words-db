# אסטרטגיית הפצה · Distribution plan

המטרה: שכל אדם, מפתח או מודל AI שמחפש "רשימת מילים בעברית" יגיע לריפו הזה וישתמש בו תוך דקה.

## התובנה המרכזית

כמעט כל רשימת מילים עברית מקיפה אחרת חסומה ברישיון: Hspell ו-eyaler/hebrew_wordlists הם AGPL, משאבי DICTA הם לא-מסחריים, ויקימילון הוא CC BY-SA. ב-Hugging Face יש כ-700 דאטהסטים בעברית, כמעט כולם קורפוסים ומבחנים, ולא נמצאה אף רשימת מילים נקייה. **הנישה פתוחה, והמסר הוא: "רשימת המילים העברית היחידה הגדולה שאפשר להשתמש בה בכל מקום".**

## איך מודלים ואנשים מוצאים מאגרים

- **חיפוש ב-GitHub** מתאים רק לשם הריפו, לתיאור ולנושאים (topics). ה-README נסרק רק בחיפוש מפורש. לכן התיאור והנושאים הם הטקסט החשוב ביותר.
- **מודלי שפה** לומדים מדפים שנסרקים ומועתקים: GitHub, Hugging Face, PyPI, npm ורשימות awesome. נוכחות בכמה שיותר מהם היא האות החזק ביותר.
- **סוכני AI** מעתיקים כתובות URL ישירות, ולכן ה-README ו-`llms.txt` מכילים כתובות raw ו-CDN מוכנות.
- **Google Dataset Search** קורא נתוני schema.org מסוג Dataset, שנמצאים בדף ה-GitHub Pages.

## מה כבר נעשה בריפו

| רכיב | קובץ | למה |
|---|---|---|
| README חדש | `README.md` | כתובות להורדה וקוד בשורה אחת בראש, טבלת השוואה מול החלופות, מילות מפתח בעברית ובאנגלית, הוראות למודלים |
| llms.txt | `llms.txt` | תקציר קריא-מכונה לפי התקן llmstxt.org |
| ציטוט | `CITATION.cff`, `.zenodo.json` | כפתור "Cite this repository" ו-DOI אוטומטי מ-Zenodo |
| CSV | `data/words.csv` | טבלה יפה ב-Hugging Face וב-Kaggle, נטען ישר ב-pandas |
| מטא-דאטה | `data/stats.json` | שם, רישיון, קבצים — מתאר את עצמו |
| כרטיס Hugging Face | `hf/README.md` | כרטיס דאטהסט עם YAML מלא |
| חבילת Python | `packages/python` | `pip install hebrew-wordlist` |
| חבילת npm | `packages/npm` | `npm install hebrew-wordlist` |
| CI | `.github/workflows/validate.yml` | בודק בכל push שהנתונים תקינים ומעודכנים |
| סנכרון HF | `.github/workflows/sync-huggingface.yml` | מעלה ל-Hugging Face בכל עדכון |
| שחרור | `.github/workflows/release.yml` | בכל Release: מצרף קבצים, מפרסם ל-PyPI ו-npm |
| אתר | `docs/index.html` | בודק מילים, חיפוש תבניות, הורדה, JSON-LD לגוגל |
| תמונת שיתוף | `docs/social-preview.png` | 1280×640 לשיתוף ברשתות |
| טופס issue | `.github/ISSUE_TEMPLATE/missing-words.yml` | קל להציע מילים חסרות |

## צעדים שרק אתה יכול לעשות (צריכים את החשבונות שלך)

לפי סדר עדיפות:

0. ✅ **בוצע (13.10.2026):** **תיאור, אתר ונושאים** — בעמוד הריפו, גלגל השיניים ליד About:
   - **Description:** `Hebrew word list · מאגר מילים בעברית — the largest public-domain (CC0) list of Hebrew words: 67k+ incl. plurals & verb conjugations. Plain TXT/JSON/CSV, free for any use.`
   - **Website:** `https://roni5604.github.io/hebrew-words-db/`
   - **Topics (20):** `hebrew hebrew-wordlist hebrew-words hebrew-dictionary hebrew-language hebrew-nlp wordlist word-list dictionary lexicon dataset open-data public-domain cc0 nlp spellcheck word-games wordle ivrit llm`
   - **GitHub Pages:** Settings → Pages → Deploy from a branch → `main` / `/docs` → Save.
1. ✅ **בוצע:** תמונת שיתוף הועלתה (Settings → General → Social preview).
2. ✅ **בוצע:** Release `v1.0.0` פורסם, וה-workflow צירף אוטומטית txt/json/csv/zip.
3. **Zenodo** (5 דק'): היכנס ל-zenodo.org עם GitHub → Settings → GitHub → הפעל את `hebrew-words-db`. ה-Release הבא (למשל `v1.1.0` אחרי תוספת מילים) יקבל DOI אוטומטית. אחר כך הוסף את ה-DOI ל-`CITATION.cff` ול-README.
4. **Hugging Face** (5 דק'): צור טוקן write ב-huggingface.co/settings/tokens → בריפו: Settings → Secrets and variables → Actions → סוד בשם `HF_TOKEN` → Actions → "Sync to Hugging Face" → Run workflow. הדאטהסט יופיע ב-`huggingface.co/datasets/roni5604/hebrew-words`.
5. **PyPI** (10 דק'): ב-pypi.org → Your account → Publishing → Add a pending publisher: owner `roni5604`, repo `hebrew-words-db`, workflow `release.yml`, environment `pypi`, project `hebrew-wordlist`. בריפו: Settings → Environments → צור `pypi`; Variables → `PUBLISH_PYPI` = `true`. ה-Release הבא יפרסם.
6. **npm** (10 דק'): בדוק ש-`hebrew-wordlist` פנוי ב-npmjs.com (אם תפוס: שנה ל-`@roni5604/hebrew-words` ב-`packages/npm/package.json`). פרסם פעם אחת ידנית (`cd packages/npm && cp ../../data/words.json . && npm publish`), ואז הגדר Trusted Publisher בהגדרות החבילה (repo + `release.yml`) והוסף משתנה `PUBLISH_NPM` = `true`.
7. **Kaggle** (10 דק', לא חובה): kaggle.com → New Dataset → העלה את `words.csv`, רישיון CC0, קישור לריפו.

## רשימות awesome — Pull Requests

**NNLP-IL/Hebrew-Resources** (הכי חשוב, כ-295 כוכבים) — בקובץ `corpora_and_data_resources.rst`, בסעיף Lexical Resources / Dictionaries & Word Lists:

```rst
* `hebrew-words-db <https://github.com/roni5604/hebrew-words-db>`_ {`CC0 1.0`_} [`<Hugging Face> <https://huggingface.co/datasets/roni5604/hebrew-words>`_] - The largest public-domain list of Modern Hebrew words (67k+, incl. plurals, verb conjugations and adjective forms). Plain TXT/JSON/CSV, no niqqud. Unlike Hspell-derived lists (AGPL), usable in commercial and closed-source projects.
```

**iddoberger/awesome-hebrew-nlp** — בסעיף Links:

```md
- [hebrew-words-db](https://github.com/roni5604/hebrew-words-db) - The largest public-domain (CC0) Hebrew word list: 67k+ words incl. inflections, TXT/JSON/CSV.
```

## קידום בקהילות

עשה רק אחרי שהאתר, ה-Release ו-Hugging Face באוויר, כדי שלמבקרים יהיה מה לנסות.

| ערוץ | זווית |
|---|---|
| LinkedIn (עברית) | "בניתי את מאגר המילים העברי החופשי הגדול ב-GitHub — כי כל השאר AGPL". תייג אנשי NLP ישראלים. |
| מעקף (Discord/WhatsApp), Python Israel, PyData TLV | שיתוף כפרויקט קוד פתוח עם בקשה לתרומת מילים |
| r/hebrew | למי שבונה משחקי מילים ואפליקציות לימוד; לינק לבודק המילים |
| r/datasets, r/LanguageTechnology | הפער ברישיונות; קרא את כללי הקידום העצמי קודם |
| Hacker News (Show HN) | "Show HN: A CC0 Hebrew word list (because Hspell is AGPL)" עם לינק לאתר. אל תבקש הצבעות |
| פורום Hugging Face, קהילות DICTA ו-ivrit.ai | הודעה על הדאטהסט |
| NNLP-IL | מייל ל-contact@nlph.org.il |

## הרגלים שמגדילים את הריפו לאורך זמן

- **עדכונים קבועים** — כל תוספת מילים היא commit, ו-Release חודשי (`v1.1.0`, `v1.2.0`...) מפרסם אוטומטית לכל הפלטפורמות.
- **"Used by"** — בקש מכל מי שמשתמש להוסיף שורה ל-README. אחרי שהחבילות יפורסמו, GitHub יראה את זה גם אוטומטית.
- **ענה מהר ל-issues ו-PRs** — פעילות היא אות למנועי חיפוש ולמשתמשים.
- **שמור את המספר בכותרת עדכני** — התג ב-README מתעדכן לבד מ-`stats.json`; עדכן ידנית את "67,000+" בתיאור כשעוברים 70k, 80k וכו'.

## מה לא נבדק

- זמינות השם `hebrew-wordlist` ב-PyPI וב-npm (בדוק לפני הפרסום).
- כמות הכוכבים העדכנית של מתחרים, ואיך בדיוק GitHub מדרג תוצאות חיפוש.
