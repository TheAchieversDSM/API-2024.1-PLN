from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np


class DocumentSimilarity:
    def __init__(self, reviews: list) -> None:
        self.__reviews = reviews

    def gerar_cluster_documentos(self, num_clusters: int = 5) -> list:
        preprocessed_reviews = self.__reviews

        tfidf = TfidfVectorizer(min_df=0.0, max_df=1.0, norm="l2", use_idf=True)
        tfidf_matrix = tfidf.fit_transform(preprocessed_reviews)
        feature_names = tfidf.get_feature_names_out()

        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)

        cluster_results = []
        for i in range(num_clusters):
            cluster_indices = np.where(cluster_labels == i)[0]
            cluster_text = " ".join([preprocessed_reviews[idx] for idx in cluster_indices])
            cluster_tfidf_scores = np.asarray(tfidf_matrix[cluster_indices].mean(axis=0)).flatten()
            top_keywords_indices = np.argsort(cluster_tfidf_scores)[::-1][:5]
            top_keywords = [feature_names[idx] for idx in top_keywords_indices]
            cluster_results.append({
                "Cluster Label": i,
                "Cluster Name": cluster_text,
                "Top Keywords": ", ".join(top_keywords)
            })

        return cluster_results
