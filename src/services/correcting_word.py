from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import List
from src.utils import nltk_tokens


class WordCorrecting:
    def __init__(self, reviews: List[str]) -> None:
        self._reviews = reviews
        self.lexico: set = set(nltk_tokens)
        self.count = defaultdict(int)
        for word in self.lexico:
            self.count[word] += 1

    def edits0(self, word):
        return {word}

    def edits1(self, word):
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        def splits(word):
            return [(word[:i], word[i:]) for i in range(len(word) + 1)]

        pairs = splits(word)
        deletes = [a + b[1:] for (a, b) in pairs if b]
        transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
        replaces = [a + c + b[1:] for (a, b) in pairs for c in alphabet if b]
        inserts = [a + c + b for (a, b) in pairs for c in alphabet]
        return set(deletes + transposes + replaces + inserts)

    def known(self, words):
        return {w for w in words if w in self.count}

    def correct(self, word):
        candidates = (
            self.known(self.edits0(word)) or self.known(self.edits1(word)) or {word}
        )
        return max(candidates, key=self.count.get)

    def preprocess_text(self):
        corrected_reviews = []
        with ThreadPoolExecutor() as executor:
            results = executor.map(self.__correct_review, self._reviews)
            for corrected_words in results:
                corrected_reviews.append(corrected_words)
        return corrected_reviews

    def __correct_review(self, review):
        corrected_words = [self.correct(word) for word in review]
        return corrected_words
