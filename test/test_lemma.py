from src.services.lemma import WordLemmatizer
import pytest
import spacy


@pytest.fixture
def lemma() -> WordLemmatizer:
    review_list = [
        ["adorei", "pães", "casa", "qualidade", "saudáveis"],
        ["precisa", "melhorar", "filtro", "porque", "pai", "pó", "café"],
    ]
    return WordLemmatizer(
        review_list, spacy.load("pt_core_news_lg", disable=["parser", "ner"])
    )


def test_lemma(lemma: WordLemmatizer):
    lem = lemma.preprocess_text()
    result = [
        ["adorar", "pão", "casa", "qualidade", "saudável"],
        ["precisar", "melhorar", "filtro", "porque", "pai", "pó", "café"],
    ]
    assert result == lem
