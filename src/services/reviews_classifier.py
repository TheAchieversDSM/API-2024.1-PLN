from src.config.settings import settings
import numpy as np
import json
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
import joblib
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class ClassificadorRevisao:
    def __init__(self, arquivo_revisoes):
        self.arquivo_revisoes = arquivo_revisoes
        self.revisoes_classificadas = []
        self.review_nao_classificado = {
            "corpus": "",
            "review_type": "",
            "feature_vector": [],
        }
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.carregar_revisoes()
        try:
            self.carregar_modelo()
        except FileNotFoundError:
            self.treinar_classificador()
            self.salvar_modelo()

    def carregar_revisoes(self):
        try:
            with open(self.arquivo_revisoes, "r", encoding="utf-8") as arquivo:
                self.revisoes_classificadas = json.load(arquivo)
        except FileNotFoundError as f:
            print("[ClassificadorRevisao - carregar_revisoes]", f)

    def construir_vetor_caracteristicas(self, tokens):
        try:
            scores = self.sentiment_analyzer.polarity_scores(" ".join(tokens))
            return np.array([scores['neg'], scores['neu'], scores['pos'], scores['compound']])
        except Exception as e:
            print("[ClassificadorRevisao - construir_vetor_caracteristicas] ", e)

    def treinar_classificador(self):
        try:
            X = [
                self.construir_vetor_caracteristicas(
                    word_tokenize(rev["corpus"].lower())
                )
                for rev in self.revisoes_classificadas
            ]
            y = [rev["review_type"] for rev in self.revisoes_classificadas]

            param_grid = [
                {
                    "alpha": [1e-5, 1e-4, 1e-3],
                    "hidden_layer_sizes": [(5,), (10,), (5, 3), (10, 5)],
                }
            ]
            classificador = MLPClassifier(solver="lbfgs", random_state=42)
            self.classificador = GridSearchCV(
                classificador, param_grid, cv=3, scoring="accuracy"
            )
            self.classificador.fit(X, y)
        except Exception as e:
            print("[ClassificadorRevisao - treinar_classificador] ", e)

    def classificar_revisoes_nao_classificadas(self, revisoes_nao_classificadas):
        resultados = []
        try:
            for revisao in revisoes_nao_classificadas:
                print(revisao   )
                tokens = word_tokenize(revisao[0].lower())
                feature_vector = self.construir_vetor_caracteristicas(tokens)
                review_type = self.classificador.predict([feature_vector])[0]
                revisao_classificada = {
                    "corpus": revisao[0],
                    "review_type": review_type,
                }
                resultados.append(revisao_classificada)
            return resultados
        except Exception as e:
            print("[ClassificadorRevisao - classificar_revisoes_nao_classificadas] ", e)
            return resultados


    def salvar_modelo(self):
        joblib.dump(self.classificador, settings.PKL_MODELO_TREINO)

    def carregar_modelo(self):
        self.classificador = joblib.load(settings.PKL_MODELO_TREINO)
