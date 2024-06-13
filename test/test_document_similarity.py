from src.services.document_similarity import DocumentSimilarity
import pytest


@pytest.fixture
def document() -> DocumentSimilarity:
    min_df: float = 0.05
    max_df: float = 0.95
    random_state: int = 42
    num_clusters: int = 2
    review_list = [
        "modelo bonito ser vir defeito vazar agir",
        "conhecer chaleira comprar cadence pois querer preto aparecer face promoção conhecer marca utilizei fiquei satisfeita esperar durabilidade longo",
        "pedir avaliação recebi produto informar extraviar estoque estranho produto disponível Side dinheiro devolver comprovar honestidade loja americano",
        "vazar de o café ma escurecer pé qualidade tomar café de o né",
        "quando chegar velocidade grande soltar óleo recebi produto r",
        "recebi produto devido feriado ma produto chegar mão",
        "dever trar pra copo sol colocar fraco",
    ]
    return DocumentSimilarity(review_list, min_df, max_df, random_state, num_clusters)


def test_generate_document_clusters(document: DocumentSimilarity):
    doc = document.generate_document_clusters()
    assert all(doc["Cluster Text"] for doc in doc)
    assert all("Cluster Label" in doc for doc in doc)
    assert all(doc["Top Keywords"] for doc in doc)
