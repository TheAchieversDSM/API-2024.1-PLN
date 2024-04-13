import logging
from typing import List
from stanza import Pipeline

logging.getLogger("stanza").setLevel(logging.ERROR)


class WordLemmatizer:
    def __init__(self, reviews: List[str]) -> None:
        self.__reviews = reviews
        self.npl = Pipeline("pt", processors="tokenize,lemma", use_lemmatizer=True)

    @staticmethod
    def lemmatize_words(review, npl: Pipeline):
        text = " ".join(review)
        doc = npl(text)
        lemmas = []
        for sent in doc.sentences:
            for word in sent.words:
                lemmas.append(word.lemma)
        return lemmas

    def preprocess_text(self) -> List[List[str]]:
        processed_texts = []
        for review in self.__reviews:
            processed_review = self.lemmatize_words(review, self.npl)
            processed_texts.append(processed_review)
        return processed_texts
