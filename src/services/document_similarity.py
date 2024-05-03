from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

class DocumentSimilarity:
    def __init__(self, reviews: list, min_df=0.05, max_df=0.95) -> None:
        self.__reviews = reviews
        self.min_df = min_df
        self.max_df = max_df

    def preprocess_reviews(self) -> list:
        preprocessed_reviews = list(set(self.__reviews))
        return preprocessed_reviews

    def generate_document_clusters(self) -> dict:
        preprocessed_reviews = self.preprocess_reviews()

        tfidf = TfidfVectorizer(min_df=self.min_df, max_df=self.max_df, norm="l2", use_idf=True)
        tfidf_matrix = tfidf.fit_transform(preprocessed_reviews)

        num_samples = len(preprocessed_reviews)
        num_clusters = max(1, int(num_samples ** 0.5))

        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)

        feature_names = tfidf.get_feature_names_out()
        cluster_results = []
        for i in range(num_clusters):
            cluster_indices = np.where(cluster_labels == i)[0]
            cluster_text = [preprocessed_reviews[idx] for idx in cluster_indices]

            if len(cluster_indices) > 0:
                cluster_tfidf_scores = np.asarray(tfidf_matrix[cluster_indices].mean(axis=0)).flatten()
                top_keywords_indices = np.argsort(cluster_tfidf_scores)[::-1][:5]
                top_keywords = [feature_names[idx] for idx in top_keywords_indices]
            else:
                top_keywords = []

            if cluster_text:
                cluster_results.append({
                    "Cluster Label": i,
                    "Cluster Text": cluster_text,
                    "Top Keywords": ", ".join(top_keywords)
                })

        return cluster_results

