from typing import List, Dict
from collections import defaultdict
from multiprocessing import Pool
import spacy


class IdentifyHotTopicList:
    def __init__(self, reviews: List[List[str]]) -> None:
        self.__reviews = reviews
        self.__nlp = spacy.load("pt_core_news_sm")

    def identify_hot_topics(self) -> Dict[str, any]:
        try:
            lexicon = self.build_model_lexicon()
            top_adjectives = self.get_top_adjectives(lexicon, 5)
            return top_adjectives
        except Exception as e:
            print("[IdentifyHotTopicList - identify_hot_topics] ", e)

    def build_model_lexicon(self) -> Dict[str, Dict[str, int]]:
        try:
            model_lexicon = defaultdict(
                lambda: {"counter": 0, "doc_counter": 0, "sent_counter": 0}
            )
            with Pool() as pool:
                results = pool.map(self.process_review, self.__reviews)
            for result in results:
                for word, counts in result.items():
                    model_lexicon[word]["counter"] += counts["counter"]
                    model_lexicon[word]["sent_counter"] += counts["sent_counter"]
                    model_lexicon[word]["doc_counter"] += counts["doc_counter"]
            return dict(model_lexicon)
        except Exception as e:
            print("[IdentifyHotTopicList - build_model_lexicon] ", e)

    def process_review(self, review: List[str]) -> Dict[str, Dict[str, int]]:
        try:
            counts = defaultdict(
                lambda: {"counter": 0, "doc_counter": 0, "sent_counter": 0}
            )
            for sentence in review:
                doc = self.__nlp(sentence)
                for token in doc:
                    if token.pos_ == "ADJ":
                        word = token.text.lower()
                        counts[word]["counter"] += 1
                        counts[word]["sent_counter"] += 1
                        counts[word]["doc_counter"] += 1
            return dict(counts)
        except Exception as e:
            print("[IdentifyHotTopicList - process_review] ", e)

    def get_top_adjectives(
        self, lexicon: Dict[str, Dict[str, int]], n: int
    ) -> List[Dict[str, int]]:
        try:
            sorted_adjectives = sorted(
                lexicon.items(), key=lambda item: item[1]["counter"], reverse=True
            )
            top_adjectives = [
                {"adjective": word, "count": data["counter"]}
                for word, data in sorted_adjectives[:n]
            ]
            return top_adjectives
        except Exception as e:
            print("[IdentifyHotTopicList - process_review] ", e)
