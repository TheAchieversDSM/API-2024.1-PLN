from src.services.reviews_classifier import ClassificadorRevisao
import pytest


@pytest.fixture
def document() -> ClassificadorRevisao:
    return ClassificadorRevisao("src/utils/reviews.json")


def test_reviews_classifier(document: ClassificadorRevisao):
    review_list = [
        [
            "Meu produto não foi entregue e a Americanas está descontando na fatura do meu cartão."
        ],
        [
            "Excelente produto, por fora em material acrílico super resistente e por dentro em adamantio, faz milagre com qualquer bebida. Sugiro aproveitarem a promoção antes que acabe."
        ],
    ]
    lem = document.classificar_revisoes_nao_classificadas(review_list)
    result = [
        {
            "corpus": "Meu produto não foi entregue e a Americanas está descontando na fatura do meu cartão.",
            "review_type": "negativa",
        },
        {
            "corpus": "Excelente produto, por fora em material acrílico super resistente e por dentro em adamantio, faz milagre com qualquer bebida. Sugiro aproveitarem a promoção antes que acabe.",
            "review_type": "positiva",
        },
    ]
    print(lem)
    assert result == lem
