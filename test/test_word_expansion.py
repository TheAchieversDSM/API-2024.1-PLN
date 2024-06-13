from src.services.word_expansion import WordAbbreviationExpand
import pytest


@pytest.fixture
def document() -> WordAbbreviationExpand:
    review_list = ["obs obg blz mto mta mt mts"]
    return WordAbbreviationExpand(review_list)


def test_word_expansion(document: WordAbbreviationExpand):
    doc = document.preprocess_text()
    result = [["observacao", "obrigado", "beleza", "muito", "muita", "muito", "muitos"]]
    assert doc == result
