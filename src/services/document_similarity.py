from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class DocumentSimilarity:
    def __init__(
        self, reviews: list, min_df=0.05, max_df=0.95, random_state=42, num_clusters=2
    ) -> None:
        self.reviews = reviews
        self.min_df = min_df if min_df is not None else 0.05
        self.max_df = max_df if max_df is not None else 0.95
        self.random_state = random_state if random_state is not None else 42
        self.num_clusters = num_clusters
        self.kmeans = None
        self.tfidf_matrix = None
        self.feature_names = None
        self.train_kmeans()

    def preprocess_reviews(self) -> list:
        preprocessed_reviews = list(set(self.reviews))
        return preprocessed_reviews

    def train_kmeans(self):
        preprocessed_reviews = self.preprocess_reviews()
        tfidf = TfidfVectorizer(
            min_df=self.min_df, max_df=self.max_df, norm="l2", use_idf=True
        )
        self.tfidf_matrix = tfidf.fit_transform(preprocessed_reviews)
        self.feature_names = tfidf.get_feature_names_out()
        self.kmeans = KMeans(
            n_clusters=self.num_clusters, random_state=self.random_state
        )
        self.kmeans.fit(self.tfidf_matrix)

    def generate_document_clusters(self) -> list:
        preprocessed_reviews = self.preprocess_reviews()
        cluster_labels = self.kmeans.predict(self.tfidf_matrix)
        cluster_results = []

        for i in range(self.kmeans.n_clusters):
            cluster_indices = np.where(cluster_labels == i)[0]
            cluster_text = [preprocessed_reviews[idx] for idx in cluster_indices]

            if len(cluster_indices) > 0:
                cluster_tfidf_scores = np.asarray(
                    self.tfidf_matrix[cluster_indices].mean(axis=0)
                ).flatten()
                top_keywords_indices = np.argsort(cluster_tfidf_scores)[::-1][:5]
                top_keywords = [self.feature_names[idx] for idx in top_keywords_indices]
            else:
                top_keywords = []

            cluster_results.append(
                {
                    "Cluster Label": i,
                    "Cluster Text": cluster_text,
                    "Top Keywords": top_keywords,
                }
            )

        return cluster_results
