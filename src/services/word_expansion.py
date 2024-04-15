import json
from typing import List


class WordAbbreviationExpand:
    def __init__(self, reviews: List[str]) -> None:
        self.__reviews = reviews

    @staticmethod
    def load_expansion_dict(expansion_dict_file):
        with open(expansion_dict_file, "r", encoding="utf-8") as f:
            expansion_dict = json.load(f)
        return expansion_dict

    @staticmethod
    def expand_word(word: str, expansion_dict: dict):
        get_value = expansion_dict.get(word)
        if expansion_dict.get(word) is not None:
            return get_value
        else:
            return word

    @staticmethod
    def word_expansion(review: str):
        expansion_dict: dict = WordAbbreviationExpand.load_expansion_dict(
            "src/utils/words.json"
        )
        expanded = []
        for words in review:
            splited_review = words.split()
            expanded_words = []
            for i, word in enumerate(splited_review):
                expanded_word = WordAbbreviationExpand.expand_word(
                    word.lower(), expansion_dict
                )
                splited_review[i] = expanded_word
                expanded_words.append(expanded_word)
            expanded.append(expanded_words)
        return expanded

    def preprocess_text(self):
        reviews = [word[:] for word in self.__reviews if word]
        result = self.word_expansion(reviews)
        return result
