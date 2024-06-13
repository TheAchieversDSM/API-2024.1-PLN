from src.services.correcting_word import WordCorrecting
import pytest


@pytest.fixture
def wc() -> WordCorrecting:
    review_list = [
        ["adorez", "batatx"],
    ]
    return WordCorrecting(review_list)


def test_wc(wc: WordCorrecting):
    wc_result = wc.preprocess_text()
    result = [["adorei", "batata"]]
    assert result == wc_result

def test_count_initialization(wc: WordCorrecting):
    assert wc.count['adorei'] == 1
    assert wc.count['batata'] == 1