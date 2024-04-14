from collections import Counter, defaultdict
from typing import List


class IdentifyHotTopicList:
    def __init__(self, review: List[str]) -> None:
        self.__review = review

    def identify_hot_topics(self) -> List[str]:
        word_to_id = defaultdict(lambda: len(word_to_id))
        corpus_bow = []
        for text in self.__review:
            bow = [word_to_id[word] for word in text.split()]
            corpus_bow.extend(bow)
        id_to_word = {v: k for k, v in word_to_id.items()}
        word_freq = Counter(corpus_bow)
        ranking = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

        result = []
        for i, (word_id, freq) in enumerate(ranking[:10], start=1):
            word = id_to_word[word_id]
            result.append({word: freq})

        return result
