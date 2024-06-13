from typing import Any, Dict, List
from pandas import DataFrame
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.product_sumary import ProductSummary
from src.schemas.product_summary import ProductSummaryModel
from src.services.processamento import Processamento


class ProductPipeline:
    def __init__(self, df: DataFrame, db: AsyncSession) -> None:
        self._df = df
        self._db = db

    async def process_hot_topics(self, _class: Processamento, data: Any) -> Dict[str, List[Dict[str, Any]]]:
        try:
            return await _class.process_data_hot_topics(data)
        except Exception as e:
            print("[ProductPipeline - process_hot_topics]", e)
            return {}

    async def products_list(self, df: DataFrame) -> List[str]:
        return df["product_id"].unique().tolist()

    async def product_execute(self):
        try:
            products = await self.products_list(self._df)
            for product in products:
                product_df = self._df[self._df["product_id"] == product]
                process_class = Processamento(product_df["review_text"].tolist())
                data = process_class.process()
                await self.result_product_summary(process_class, data, product)
        except Exception as e:
            print("[ProductPipeline - product_execute]", e)

    async def result_product_summary(self, process_class: Processamento, data: Any, product: str) -> None:
        product_summary = ProductSummary()
        sentiment_clusters = await self.process_hot_topics(process_class, data)
        try:
            for review_type, adjectives_list in sentiment_clusters.items():
                for adjective_info in adjectives_list:
                    product_model = ProductSummaryModel(
                        product_id=product,
                        text=adjective_info.get("adjective"),
                        amount=adjective_info.get("count"),
                        sentiment_review=review_type,
                    )
                    await product_summary.insert(product_model, self._db)
        except Exception as e:
            print("[ProductPipeline - result_product_summary]", e)