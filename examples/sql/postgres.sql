-- Load the Hebrew word list into PostgreSQL and get fast "did you mean"
-- suggestions with trigram similarity.
--
--   curl -sLo words.txt https://raw.githubusercontent.com/roni5604/hebrew-words-db/main/data/words.txt
--   psql -f postgres.sql

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS hebrew_words (
    word   text PRIMARY KEY,
    length int GENERATED ALWAYS AS (char_length(word)) STORED
);

\copy hebrew_words(word) FROM 'words.txt'

CREATE INDEX IF NOT EXISTS hebrew_words_trgm ON hebrew_words USING gin (word gin_trgm_ops);

-- Is it a word?
SELECT EXISTS (SELECT 1 FROM hebrew_words WHERE word = 'שלום') AS is_word;

-- "Did you mean" for a misspelled query (e.g. a site search box)
SELECT word, similarity(word, 'מחשבון') AS score
FROM hebrew_words
WHERE word % 'מחשבון'
ORDER BY score DESC
LIMIT 5;

-- Autocomplete (the primary key index serves prefix ranges)
SELECT word FROM hebrew_words WHERE word >= 'מחש' AND word < 'מחש' || chr(1114111) ORDER BY word LIMIT 10;

-- Five-letter words for a Hebrew Wordle
SELECT word FROM hebrew_words WHERE length = 5 ORDER BY random() LIMIT 1;
