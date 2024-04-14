from typing import List
from spellchecker import SpellChecker


class WordCorrecting:
    def __init__(self, reviews: List[str]) -> None:
        self._spellchecker = SpellChecker(language="pt")
        self._reviews = reviews

    def preprocess_text(self):
        correcao_palavra_list = []

        def correcao_palavra(word):
            correction_word = self._spellchecker.correction(word)
            return correction_word if correction_word is not None else word

        for words in self._reviews:
            correcao_lista = [correcao_palavra(word) for word in words]
            correcao_palavra_list.append(correcao_lista)

        return correcao_palavra_list
