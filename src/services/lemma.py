from concurrent.futures import ThreadPoolExecutor
from typing import List
import spacy


class WordLemmatizer:
    def __init__(self, reviews: List[str]) -> None:
        self.__reviews = reviews
        self.nlp = spacy.load("pt_core_news_lg", disable=["parser", "ner"])

    def preprocess_text(self) -> List[List[str]]:
        with ThreadPoolExecutor() as executor:
            result = executor.map(self.__lematize_review, self.__reviews)
        return list(result)

    def lemmatize_words(self, text: str) -> List[str]:
        doc = self.nlp(text)
        lemmatized_tokens = [token.lemma_ for token in doc]
        return lemmatized_tokens

    def __lematize_review(self, review):
        processed_review = self.lemmatize_words(" ".join(review))
        return processed_review
