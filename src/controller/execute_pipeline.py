from src.controller.category_pipeline import CategoryPipeline
from src.controller.product_pipeline import ProductPipeline
from src.models.base_import import BaseImportLog
from src.models.comments import Comment
from src.models.products import Product

from src.schemas.base_import import BaseImportModel
from src.schemas.commet import CommentModel
from src.schemas.product import ProductModel

from src.utils import ReadCsv
from io import BytesIO
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

    async def inserts(self, df: DataFrame, db: AsyncSession) -> str:
        try:
            await self.insert_products(df, db)
            await self.insert_comments(df, db)
            return "Insertion completed"
        except Exception as e:
            print("[ExecutePipeline - category_summary] Erro ao inserir dados: ", e)
            raise

    async def execute_process(self, df: DataFrame, db: AsyncSession):
        category_execute = CategoryPipeline(df.copy(), db)
        product_execute = ProductPipeline(df.copy(), db)
        try:
            await category_execute.category_execute()
            await product_execute.product_execute()
        except Exception as e:
            print("[ExecutePipeline - execute_process]", e)

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
