from typing import List
from src.utils import stop_words
import re


class StopWordsClear:
    def __init__(self, reviews: List[str]) -> None:
        self.stopwords = stop_words
        self.reviews = reviews

    @staticmethod
    def remove_duplicate_characters(text: str) -> str:
        character_repeat =  re.compile(r'(\w*)(\w)\2(\w*)')
        match_substitution = r"\1"

        def replace_repeated_chars(old_word):
            new_word = character_repeat.sub(match_substitution, old_word)
            while new_word != old_word:
                old_word = new_word
                new_word = character_repeat.sub(match_substitution, old_word)
            return new_word

        return " ".join(replace_repeated_chars(word) if word.isalpha() else word for word in text.split())

    @staticmethod
    def remove_stopwords(tokens: List[str], stopwords: set[str]) -> str:
        filtered_tokens = []
        for token in tokens:
            corrected_token = StopWordsClear.remove_duplicate_characters(token)
            if corrected_token.lower() not in stopwords:
                filtered_tokens.append(corrected_token)
        return " ".join(filtered_tokens)

    @staticmethod
    def clean_text(text: str) -> str:
        cleaned_text = re.sub(r'\d+', ' ', text)
        cleaned_text = re.sub(r'\b(?:R|\$|€|£|¥)\b', ' ', cleaned_text)
        cleaned_text = re.sub(r'[^\w\s\-áéíóúâêîôûàèìòùãõç]+|\([^)]*\)|\[[^\]]*\]|\{[^}]*\}', ' ', cleaned_text)
        return cleaned_text.lower()

    def preprocess_text(self) -> List[str]:
        preprocessed_texts = []
        for text in self.reviews:
            if text is not None:
                cleaned_text = StopWordsClear.clean_text(text)
                tokens = cleaned_text.split()
                text_without_stopwords = StopWordsClear.remove_stopwords(
                    tokens, self.stopwords
                )
                preprocessed_texts.append(text_without_stopwords)
        return preprocessed_texts