from typing import Any, Dict, List, Tuple, Union
from pandas import DataFrame
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.category_summary import CategorySummary
from src.schemas.category_summary import CategorySummaryModel
from src.services.processamento import Processamento

CategoryData = Dict[str, List[Dict[str, Union[str, int]]]]
SentimentClusters = Dict[str, List[Dict[str, Any]]]
TextClusters = List[Dict[str, Any]]
ClusterProcessingParams = Tuple[str, str, TextClusters, str, CategorySummary]


class CategoryPipeline:
    def __init__(self, df: DataFrame, db: AsyncSession) -> None:
        self._df = df
        self._db = db

    async def process_most_comment(
        self, process_class: Processamento, data: Any
    ) -> SentimentClusters:
        try:
            return await process_class.process_data_document_similarity(data)
        except Exception as e:
            print("[CategoryPipeline - process_most_comment] ", e)

    async def process_hot_topics(self, process_class: Processamento, data: Any) -> str:
        try:
            return await process_class.process_data_hot_topics(data)
        except Exception as e:
            print("[CategoryPipeline - process_hot_topics] ", e)

    async def categories(self, df: DataFrame) -> List[str]:
        return df["site_category_lv1"].unique().tolist()

    async def category_execute(self):
        try:
            categories = await self.categories(self._df)
            for category in categories:
                category_df = self._df[self._df["site_category_lv1"] == category]
                process_class = Processamento(category_df["review_text"].tolist())
                data = process_class.process()
                await self.result_most_comment(process_class, data, category, "comment")
                await self.result_category_summary(process_class, data, category, "tag")
        except Exception as e:
            print("[CategoryPipeline - category_execute]", e)

    async def result_category_summary(
        self, process_class: Processamento, data: Any, category: str, type: str = ""
    ) -> None:
        try:
            category_summary = CategorySummary()
            sentiment_clusters = await self.process_hot_topics(process_class, data)
            for sentiment, clusters in sentiment_clusters.items():
                for results in clusters:
                    amount = results.get("count")
                    text = results.get("adjective")
                    category_model = CategorySummaryModel(
                        category=category,
                        amount=amount,
                        text=text,
                        type=type,
                        sentiment_review=sentiment,
                    )
                    await category_summary.insert(category_model, self._db)
        except Exception as e:
            print("[ExecutePipeline - result_category_summary] ", e)

    async def result_most_comment(
        self, process_class: Processamento, data: Any, category: str, type: str = ""
    ) -> None:
        try:
            category_summary = CategorySummary()
            sentiment_clusters = await self.process_most_comment(process_class, data)
            for sentiment, clusters in sentiment_clusters.items():
                await self.process_clusters(
                    (category, sentiment, clusters, type, category_summary)
                )
        except Exception as e:
            print("[CategoryPipeline - result_most_comment]", e)

    async def process_clusters(self, params: ClusterProcessingParams) -> None:
        category, sentiment, clusters, type, category_summary = params
        for cluster_info in clusters:
            if isinstance(cluster_info, dict):
                top_texts = cluster_info.get("Cluster Text", [])[:3]
                cluster_label = cluster_info.get("Cluster Label", 0)
                for text in top_texts:
                    await self.process_cluster_texts(
                        (
                            category,
                            text,
                            cluster_label,
                            sentiment,
                            type,
                            category_summary,
                        )
                    )

    async def process_cluster_texts(
        self, params: Tuple[str, str, int, str, str, CategorySummary]
    ) -> None:
        category, top_text, cluster_label, sentiment, type, category_summary = params
        category_model = CategorySummaryModel(
            category=category,
            text=top_text,
            amount=cluster_label,
            type=type,
            sentiment_review=sentiment,
        )
        await category_summary.insert(category_model, self._db)
