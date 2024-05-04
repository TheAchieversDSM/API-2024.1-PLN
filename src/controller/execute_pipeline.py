from src.models import CategorySummary, Comment, Product, BaseImportLog
from src.models.product_sumary import ProductSummary
from src.schemas import (
    BaseImportModel,
    CategorySummaryModel,
    CommentModel,
    ProductModel,
)
from src.schemas.product_summary import ProductSummaryModel
from src.services.processamento import Processamento
from src.utils import ReadCsv
from io import BytesIO
from typing import Dict, List
from fastapi import UploadFile
from pandas import DataFrame
from sqlalchemy.ext.asyncio import AsyncSession
from dateutil.parser import parse

class ExecutePipeline(ReadCsv):
    def __init__(self, csv: UploadFile, db: AsyncSession) -> None:
        super().__init__()
        self.__db = db
        self.__csv = csv

    async def get_csv_file(self) -> BytesIO:
        contents = await self.__csv.read()
        return BytesIO(contents)

    async def processing(self):
        logger_id = await self.base_import_log("POST", self.__db)
        try:
            async with self.__db.begin() as exec:
                exec = exec.session
                try:
                    df = await self.dataframe()
                    await self.inserts(df.copy(), exec)
                    await self.execute_process(df.copy(), exec)
                    await exec.commit()
                except Exception as e:
                    print("[ExecutePipeline - processing]: ", e)
                    await exec.rollback()
            await self.base_import_log("PUT", self.__db, "Concluido", logger_id)
        except Exception as e:
            await self.base_import_log("PUT", self.__db, "Falha no processo", logger_id)
            print("[ExecutePipeline - processing] ", e)

    async def base_import_log(
        self, method: str, db: AsyncSession, status: str = None, id: int = None
    ):
        b = BaseImportLog()
        if method == "POST":
            b_model = BaseImportModel(
                fileName=self.__csv.filename, status="Processando"
            )
            id = await b.insert(b_model, db)
            await db.commit()
            return id
        if method == "PUT":
            try:
                if id is None:
                    raise ValueError("ID is required for PUT method.")
                await b.update(id=id, status=status, db=db)
            except Exception as e:
                print("[ExecutePipeline - base_import_log] ", e)
            finally:
                await db.commit()

    async def dataframe(self) -> DataFrame:
        try:
            csv = await self.get_csv_file()
            df = await self.read_csv(csv)
            df.dropna(inplace=True)
            return df
        except Exception as e:
            raise e

    async def categories(self, df: DataFrame) -> List[str]:
        unique_categories = set()
        for _, row in df.iterrows():
            unique_categories.add(row["site_category_lv1"])
        return list(unique_categories)

    async def products_list(self, df: DataFrame) -> List[str]:
        unique_categories = set()
        for _, row in df.iterrows():
            unique_categories.add(row["product_id"])
        return list(unique_categories)

    async def inserts(self, df: DataFrame, db: AsyncSession) -> str:
        try:
            await self.insert_products(df, db)
            await self.insert_comments(df, db)
            return "Insertion completed"
        except Exception as e:
            print("[ExecutePipeline - category_summary] Erro ao inserir dados: ", e)
            raise

    def process_most_comment(self, _class: Processamento, data):
        try:
            return _class.process_data_document_similarity(data)
        except Exception as e:
            print("[ExecutePipeline - process_most_comment] ", e)

    def process_hot_topics(self, _class: Processamento, data) -> str:
        try:
            return _class.process_data_hot_topics(data)
        except Exception as e:
            print("[ExecutePipeline - process_hot_topics] ", e)

    async def execute_process(self, df: DataFrame, db: AsyncSession):
        try:
            await self.category_execute(df.copy(), db)
            await self.product_execute(df.copy(), db)
        except Exception as e:
            print("[ExecutePipeline - execute_process]", e)

    async def category_execute(self, df: DataFrame, db: AsyncSession):
        result_hot_topics = {}
        result_most_comments = {}
        try:
            categories = await self.categories(df)
            for category in categories:
                category_df = df[df["site_category_lv1"] == category]
                process_class = Processamento(category_df["review_text"].tolist())
                data = process_class.process()
                result_most_comments[category] = self.process_most_comment(
                    process_class, data
                )
                result_hot_topics[category] = self.process_hot_topics(
                    process_class, data
                )
            await self.result_category_summary(result_hot_topics, db, "tag")
            await self.result_most_comment(result_most_comments, db, "comment")
        except Exception as e:
            print("[ExecutePipeline - category_execute]", e)

    async def product_execute(self, df: DataFrame, db: AsyncSession):
        result = {}
        try:
            products = await self.products_list(df)
            for product in products:
                product_df = df[df["product_id"] == product]
                process_class = Processamento(product_df["review_text"].tolist())
                data = process_class.process()
                result[product] = self.process_hot_topics(process_class, data)
            await self.result_product_summary(result, db)
        except Exception as e:
            print("[ExecutePipeline - product_execute]", e)

    async def result_product_summary(
        self, data: Dict[str, List[str]], db: AsyncSession
    ) -> None:
        product_summary = ProductSummary()
        try:
            for product in data:
                for values in data[product]:
                    product_model = ProductSummaryModel(
                        product_id=product,
                        text=values["adjective"],
                        amount=values["count"],
                    )
                    await product_summary.insert(product_model, db)
                # print(product)
                # print(data[product])
        except Exception as e:
            print("[ExecutePipeline - result_product_summary]", e)

    async def result_category_summary(
        self, data: Dict[str, List[str]], db: AsyncSession, type: str = ""
    ) -> None:
        category_summary = CategorySummary()
        try:
            for category in data:
                for values in data[category]:
                    category_model = CategorySummaryModel(
                        category=category,
                        text=values["adjective"],
                        amount=values["count"],
                        type=type,
                    )
                    await category_summary.insert(category_model, db)
        except Exception as e:
            print("[ExecutePipeline - result_category_summary] ", e)

    async def result_most_comment(
        self, data: Dict[str, List[Dict[str, str]]], db: AsyncSession, type: str = ""
    ) -> None:
        try:
            category_summary = CategorySummary()
            for category, clusters in data.items():
                if clusters is None:
                    continue
                for cluster_index, cluster in enumerate(clusters, 1):
                    if cluster is None:
                        continue
                    top_texts = cluster.get("Cluster Text", [])[:2]
                    for text in top_texts:
                        if text is not None:
                            category_model = CategorySummaryModel(
                                category=category,
                                text=text,
                                amount=cluster_index,
                                type=type,
                            )
                            await category_summary.insert(category_model, db)
        except Exception as e:
            print("[ExecutePipeline - result_most_comment] ", e)

    async def insert_products(self, df: DataFrame, db: AsyncSession) -> None:
        try:
            product_data = Product()
            for _, row in df.iterrows():
                product = ProductModel(
                    category=row["site_category_lv1"],
                    id=row["product_id"],
                    subcategory=row["site_category_lv2"],
                    name=row["product_name"],
                    externalId="",
                )
                await product_data.insert(product, db)
        except Exception as e:
            raise e

    async def insert_comments(self, df: DataFrame, db: AsyncSession) -> None:
        try:
            comment_data = Comment()
            for _, row in df.iterrows():
                date = parse(row["submission_date"]).strftime("%Y-%m-%d")
                comment = CommentModel(
                    productId=row["product_id"],
                    state=row["reviewer_state"],
                    date=date,
                    age=row["reviewer_birth_year"],
                    recommended=row["recommend_to_a_friend"],
                    gender=row["reviewer_gender"],
                    id=row["reviewer_id"],
                    rating=row["overall_rating"],
                    text=row["review_text"],
                    title=row["review_title"],
                )
                await comment_data.insert(comment, db)
        except Exception as e:
            print("Erro ao inserir comentários:", e)
