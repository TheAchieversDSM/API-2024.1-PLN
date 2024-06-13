import spacy
from src.services.hot_topics import IdentifyHotTopicList
import pytest


@pytest.fixture
def hot_topics() -> IdentifyHotTopicList:
    review_list = [
        [
            "superar agilidade praticidade panela elétrico costumo panela cozimento japonês levar minuto ne panela rápido exatamente minuto recomer",
            "produto maravilhoso barulhento fácil manuseio tranquilo montar desmontar entrega prazo tratar época natal americana parabéns produto recomer força",
            "bom imaginar superar expectativa",
            "super bonito potente demorar chegar preço otimo recomendar",
            "roxo cumprir prometer muito atenção uso bater prolongar vida útil mesmo",
            "produto feliz semana cheio amor alegrio realização",
            "produto gula medida certo fácil entalação",
            "produto ótima qualidade fácil valer pena",
            "produto prefeito super bonito atender neve",
            "ótima amar americana entregar produto otimo qualidade recomer",
            "walita Master puro modelo anterior funcionar te robusto silenciar poder pratico atual natural evolução excelente produto manutenção comprar atualizar pratico uso ace poder barulhento ficar ai dica posterior melhoria quanto trituração alimento liquidificador granulação anterior devido designer latino enfim produto ha aprimorar atingir excelência",
            "excelente produto prático rápido eficaz valer pena comprar",
            "maquina recomendar trabalho leve ajudar dia-dia bom iniciante recomender",
            "gostar achar totalmente funcional rapidamente ch ficar pronto parabéns achar frágil madrinha bacano",
            "bom produto funcionar recomendar",
            "ótima superar expectativa café sair quentinho super fácil rápido adoramos",
            "produto ótima qualidade chegar prazo",
            "produto entregar prazo gostar",
            "pão maravilhoso bolo eficiente amar",
        ]
    ]
    return IdentifyHotTopicList(
        review_list, spacy.load("pt_core_news_lg", disable=["parser", "ner"])
    )


def test_generate_hot_topics_clusters(hot_topics: IdentifyHotTopicList):
    doc = hot_topics.identify_hot_topics()
    result = [
        {"adjective": "fácil", "count": 4},
        {"adjective": "ótima", "count": 4},
        {"adjective": "bom", "count": 3},
        {"adjective": "maravilhoso", "count": 2},
        {"adjective": "americana", "count": 2},
    ]
    assert result == doc
