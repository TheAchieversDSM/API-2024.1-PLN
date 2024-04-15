from typing import List, Union

from src.schemas.request import Review
from src.services.processamento import Processamento


class GetHotTopicsByCategory:
    def __init__(self, category, data: List[Review], limit: Union[str, int]) -> None:
        self.__category = category
        self.__data = data
        self.__limit = self._resolve_limit(limit)

    def _resolve_limit(self, limit: Union[str, int]) -> int:
        if isinstance(limit, str) and limit.lower() == "max":
            return None
        else:
            return int(limit)

    def _resolver_category(self, category: str) -> List[str]:
        return category.split(",")

    def init_hot_topic(self):
        categories = self._resolver_category(self.__category)
        reviews = []
        for review in self.__data:
            if review.site_category_lv1 in categories:
                reviews.append(review)
                if self.__limit is not None and len(reviews) >= self.__limit:
                    break
        return reviews

    def process_data(self, df):
        process = Processamento(df).process_data_hot_topics()
        return process

    def process_by_categories(self):
        reviews = self.init_hot_topic()
        categories = self._resolver_category(self.__category)
        results = {}
        for category in categories:
            category_reviews = [
                review.review_text
                for review in reviews
                if review.site_category_lv1 == category
            ]
            results[category] = self.process_data(category_reviews)
        return results
