from typing import List
from fastapi import UploadFile
import pandas as pd

from ..services.stopwords import StopWordsClear
from ..utils.timer import timing
from io import StringIO
from contextlib import redirect_stdout


class Processamento:
    def __init__(self, csv: UploadFile) -> None:
        self.__csv = csv

    @timing
    def __clear_data(self) -> pd.DataFrame:
        with StringIO(self.__csv.file.read().decode("utf-8")) as csv_data:
            with redirect_stdout(None):
                df = pd.read_csv(csv_data)
        df = df.dropna(subset=["review_text"])
        return df

    @timing
    def __remove_stop_words(self, reviews: List[str]) -> List[str]:
        stopword = StopWordsClear(reviews)
        process = stopword.preprocess_text()
        return process

    def process_data(self):
        df, timer = self.__clear_data()
        reviews, timer = self.__remove_stop_words(df["review_text"])

        return reviews
