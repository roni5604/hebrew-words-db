declare const words: readonly string[] & {
  words: readonly string[];
  wordSet(): ReadonlySet<string>;
  isWord(word: string): boolean;
  ofLength(n: number): string[];
  startingWith(prefix: string): string[];
  randomWord(): string;
};
export = words;
