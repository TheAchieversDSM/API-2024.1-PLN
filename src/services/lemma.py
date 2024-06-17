from typing import List


class WordLemmatizer:
    def __init__(self, reviews: List[str], nlp) -> None:
        self.__reviews = reviews
        self.nlp = nlp

    def preprocess_text(self) -> List[List[str]]:
        return [self.__lematize_review(review) for review in self.__reviews]

    def lemmatize_words(self, text: str) -> List[str]:
        doc = self.nlp(text)
        return [token.lemma_ for token in doc]

    def __lematize_review(self, review: str) -> List[str]:
        return self.lemmatize_words(" ".join(review))
