from typing import List
from fastapi import UploadFile
import pandas as pd

from src.services.correcting_word import WordCorrecting

from ..services.lemma import WordLemmatizer
from ..services.word_expansion import WordAbbreviationExpand
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

    @timing
    def __expanded_abreviatio(self, reviews: List[str]):
        word_abbreviation = WordAbbreviationExpand(reviews)
        process = word_abbreviation.preprocess_text()
        return process

    @timing
    def __correcting_words(self, reviews: List[str]):
        correcting_words = WordCorrecting(reviews)
        process = correcting_words.preprocess_text()
        return process

    @timing
    def __lemmatize_words(self, reviews: List[str]):
        word_lemmatizer = WordLemmatizer(reviews)
        process = word_lemmatizer.preprocess_text()
        return process

    def process_data(self):
        df, timer = self.__clear_data()
        reviews, timer = self.__remove_stop_words(df["review_text"][:10])
        expanded, timer = self.__expanded_abreviatio(reviews)
        corrects, timer = self.__correcting_words(expanded)
        lemmatizer, timer = self.__lemmatize_words(corrects)
        return lemmatizer
