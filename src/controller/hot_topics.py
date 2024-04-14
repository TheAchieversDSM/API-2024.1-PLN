from typing import List, Union
from fastapi import UploadFile
from io import BytesIO

from src.services.processamento import Processamento
from ..utils.csv import ReadCsv


class GetHotTopicsByCategory(ReadCsv):
    def __init__(self, category, csv: UploadFile, limit: Union[str, int]) -> None:
        super().__init__()
        self.__category = category
        self.__csv = csv
        self.__limit = limit

    def _resolve_limit(self, limit: Union[str, int]) -> int:
        if isinstance(limit, str) and limit.lower() == "max":
            return None
        else:
            return int(limit)

    def _resolver_category(self, category: str) -> List[str]:
        return category.split(",")

    def get_csv_file(self):
        return BytesIO(self.__csv.file.read())

    def init_hot_topic(self):
        df = self.read_csv()
        limit = self._resolve_limit(self.__limit)
        categories = self._resolver_category(self.__category)
        if limit is not None:
            df = df.head(limit)
        filters = df[df["site_category_lv1"].isin(categories)]
        return filters

    def process_data(self, df):
        process = Processamento(df["review_text"]).process_data_hot_topics()
        return process

    def process_by_categories(self):
        df = self.init_hot_topic()
        categories = self._resolver_category(self.__category)
        results = {}
        for category in categories:
            category_df = df[df["site_category_lv1"] == category]
            results[category] = self.process_data(category_df)
        return results
