from typing import List
import pandas as pd

from src.services.correcting_word import WordCorrecting
from src.services.document_similarity import DocumentSimilarity
from src.services.hot_topics import IdentifyHotTopicList

from .lemma import WordLemmatizer
from .word_expansion import WordAbbreviationExpand
from .stopwords import StopWordsClear
from ..utils.timer import timing


class Processamento:
    def __init__(self, csv: pd.DataFrame) -> None:
        self.__csv = csv

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

    @timing
    def __ranking_words(self, reviews: List[str]):
        ranking_words = IdentifyHotTopicList(reviews)
        process = ranking_words.identify_hot_topics()
        return process

    @timing
    def __document_similarity(self, reviews: List[str]):
        document_similarity = DocumentSimilarity(reviews)
        process = document_similarity.gerar_cluster_documentos()
        return process

    def process_data_hot_topics(self):
        reviews, _ = self.__remove_stop_words(self.__csv)
        expanded, _ = self.__expanded_abreviatio(reviews)
        corrects, _ = self.__correcting_words(expanded)
        lemmatizer, _ = self.__lemmatize_words(corrects)
        ranking, _ = self.__ranking_words(lemmatizer)
        return ranking

    def process_data_document_similarity(self):
        reviews, _ = self.__remove_stop_words(self.__csv)
        expanded, _ = self.__expanded_abreviatio(reviews)
        corrects, _ = self.__correcting_words(expanded)
        lemmatizer, _ = self.__lemmatize_words(corrects)
        similarity, _ = self.__document_similarity(lemmatizer)
        return similarity
