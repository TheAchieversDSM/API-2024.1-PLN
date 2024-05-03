import numpy as np
import json
import re
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
import joblib
from nltk.tokenize import word_tokenize


class ClassificadorRevisao:
    def __init__(self, arquivo_revisoes):
        self.arquivo_revisoes = arquivo_revisoes
        self.revisoes_classificadas = []
        self.review_nao_classificado = {
            "corpus": "",
            "review_type": "",
            "feature_vector": [],
        }
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

    def construir_vetor_caracteristicas(self, tokens, lexico_base):
        try:
            vetor_caracteristicas = np.zeros(len(lexico_base))
            for pos, palavra_lexico in enumerate(lexico_base):
                vetor_caracteristicas[pos] = tokens.count(palavra_lexico)
            return vetor_caracteristicas
        except Exception as e:
            print("[ClassificadorRevisao - construir_vetor_caracteristicas] ", e)

    def treinar_classificador(self):
        lexico_base = set()
        try:
            for revisao in self.revisoes_classificadas:
                lexico_base.update(set(re.findall(r"\b\w+\b", revisao["corpus"])))
            lexico_base = sorted(lexico_base)

            X = [
                self.construir_vetor_caracteristicas(word_tokenize(rev["corpus"]), lexico_base)
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
        lexico_base = set()
        try:
            for revisao in self.revisoes_classificadas:
                lexico_base.update(set(re.findall(r"\b\w+\b", revisao["corpus"])))
            lexico_base = sorted(lexico_base)

            for tokens in revisoes_nao_classificadas:
                feature_vector = self.construir_vetor_caracteristicas(tokens, lexico_base)
                review_type = self.classificador.predict([feature_vector])[0]
                revisao_classificada = {
                    "corpus": " ".join(tokens),
                    "review_type": review_type,
                }
                resultados.append(revisao_classificada)
            return resultados
        except Exception as e:
            print("[ClassificadorRevisao - classificar_revisoes_nao_classificadas] ", e)

    def salvar_modelo(self):
        joblib.dump(self.classificador, "modelo_treinado.pkl")

    def carregar_modelo(self):
        self.classificador = joblib.load("modelo_treinado.pkl")
