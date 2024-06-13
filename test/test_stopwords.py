from src.services.stopwords import StopWordsClear
import pytest


@pytest.fixture
def document() -> StopWordsClear:
    review_list = [
        "SUPERA EM AGILIDADE E PRATICIDADE OUTRAS PANELAS ELÉTRICAS.  COSTUMO USAR OUTRA PANELA PARA COZIMENTO DE ARROZ (JAPONESA), MAS LEVA MUITO TEMPO,  +/- 50 MINUTOS.  NESSA PANELA  É MUITO MAIS RÁPIDO, EXATAMENTE 6 MINUTOS.    EU RECOMENDO.",
        "Produto maravilhoso! Não é barulhento, fácil manuseio, tranquilo de montar e desmontar, entrega antes do prazo mesmo se tratando de época do Natal. Americanas de parabéns e o produto muito bom. Recomendo com força.",
        "Melhor do que imaginava. Superou minhas expectativas.",
    ]
    return StopWordsClear(review_list)


def test_stop_words(document: StopWordsClear):
    doc = document.preprocess_text()
    result = [
        "supera agilidade praticidade panelas elétricas costumo panela cozimento arroz japonesa leva - minutos panela rápido exatamente minutos recomendo",
        "produto maravilhoso barulhento fácil manuseio tranquilo montar desmontar entrega prazo tratando época natal americanas parabéns produto recomendo força",
        "melhor imaginava superou expectativas",
    ]
    assert doc == result
