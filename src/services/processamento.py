from typing import List
import pandas as pd
import spacy

from src.services.correcting_word import WordCorrecting
from src.services.document_similarity import DocumentSimilarity
from src.services.hot_topics import IdentifyHotTopicList
from src.services.reviews_classifier import ClassificadorRevisao

from .lemma import WordLemmatizer
from .word_expansion import WordAbbreviationExpand
from .stopwords import StopWordsClear
from src.utils.timer_func import timing


class Processamento:
    def __init__(self, csv: pd.DataFrame) -> None:
        self.__csv = csv
        self.__nlp = spacy.load("pt_core_news_sm", disable=["parser", "ner"])

    def process(self) -> List[List[str]]:
        reviews, _ = self.__remove_stop_words(self.__csv)
        expanded, _ = self.__expanded_abreviatio(reviews)
        corrects, _ = self.__correcting_words(expanded)
        lemmatizer, _ = self.__lemmatize_words(corrects)
        classifier, _ = self.__reviews_classifier(lemmatizer)
        return classifier

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
        word_lemmatizer = WordLemmatizer(reviews, self.__nlp)
        process = word_lemmatizer.preprocess_text()
        return process

    @timing
    def __ranking_words(self, reviews: List[str]):
        list_type = {"positiva": [], "negativa": [], "neutra": []}
        self.__process_reviews(reviews, list_type)
        self.__generate_identify_for_list_type(list_type)
        return list_type

    @timing
    def __document_similarity(self, reviews: List[dict]):
        list_type = {"positiva": [], "negativa": [], "neutra": []}
        self.__process_reviews(reviews, list_type)
        self.__generate_clusters_for_list_type(list_type)
        return list_type

    @timing
    def __reviews_classifier(self, reviews: List[str]):
        reviews_classifer = ClassificadorRevisao("src/utils/reviews.json")
        process = reviews_classifer.classificar_revisoes_nao_classificadas(reviews)
        return process

    def __process_reviews(self, reviews: List[dict], list_type: dict):
        for review in reviews:
            review_type = review.get("review_type")
            corpus = review.get("corpus")
            if review_type in list_type:
                list_type[review_type].append(corpus)

    def __generate_clusters_for_list_type(self, list_type: dict):
        for review_type, corpus_list in list_type.items():
            if len(corpus_list) >= 2:
                document_similarity = DocumentSimilarity(corpus_list)
                clusters = document_similarity.generate_document_clusters()
                list_type[review_type] = clusters

    def __generate_identify_for_list_type(self, list_type: dict):
        for review_type, corpus_list in list_type.items():
            if len(corpus_list) >= 1:
                ranking_words = IdentifyHotTopicList([corpus_list], self.__nlp)
                clusters = ranking_words.identify_hot_topics()
                list_type[review_type] = clusters

    async def process_data_hot_topics(self, data):
        ranking, _ = self.__ranking_words(data)
        return ranking

    async def process_data_document_similarity(self, data):
        similarity, _ = self.__document_similarity(data)
        return similarity
