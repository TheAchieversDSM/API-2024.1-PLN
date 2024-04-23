from io import BytesIO
from fastapi import UploadFile
from pandas import DataFrame
from src.models.products import Product
from src.models.base_import import BaseImportLog
from src.schemas.product import ProductModel
from src.schemas.base_import import BaseImportModel
from src.utils.csv import ReadCsv
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession


class ExecutePipeline(ReadCsv):
    def __init__(self, csv: UploadFile, db: AsyncSession) -> None:
        super().__init__()
        self.__db = db
        self.__csv = csv

    async def get_csv_file(self) -> BytesIO:
        contents = await self.__csv.read()
        return BytesIO(contents)

    async def dataframe(self) -> DataFrame:
        csv = await self.get_csv_file()
        df = await self.read_csv(csv)
        return df

    async def categories(self, df):
        unique_categories = set()
        for index, row in df.iterrows():
            unique_categories.add(row["site_category_lv1"])
        return list(unique_categories)

    async def insert_products(self, df: DataFrame):
        product_data = Product()
        for index, row in df.iterrows():
            product = ProductModel(
                category=row["site_category_lv1"],
                id=row["product_id"],
                subcategory=row["site_category_lv2"],
                name=row["product_name"],
                externalId="",
            )
            await product_data.insert(product, self.__db)
        return "Insertion completed"

    async def create_summary(self, df: DataFrame):
        return "Summary created"

    async def create_tags(self, df: DataFrame):
        return "Tags created"

    async def base_import_log(self, method: str, msg: str = None, id: int = None):
        b = BaseImportLog()
        if method == "POST":
            b_model = BaseImportModel(fileName=self.__csv.filename, status="Processando")
            id = await b.insert(b_model, self.__db)
            return id
        elif method == "PUT":
            await b.update(id=id, msg=msg, db=self.__db)

            
    async def processing(self):
        logger_id = await self.base_import_log("POST")
        df = await self.dataframe()

        task1 = asyncio.create_task(self.insert_products(df.copy()))
        task2 = asyncio.create_task(self.create_summary(df.copy()))
        task3 = asyncio.create_task(self.create_tags(df.copy()))

        results = await asyncio.gather(task1, task2, task3)

        print(results[0])
        print(results[1])
        print(results[2])
        await self.base_import_log("PUT", "Concluido", logger_id)

