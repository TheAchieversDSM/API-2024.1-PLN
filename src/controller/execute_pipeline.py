from io import BytesIO
from fastapi import UploadFile
from pandas import DataFrame
from src.models.products import Product
from src.schemas.product import ProductModel
from src.utils.csv import ReadCsv
import concurrent.futures
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

    def create_summary(self, df: DataFrame):
        return "Summary created"

    def create_tags(self, df: DataFrame):
        return "Tags created"

    async def processing(self):
        df = await self.dataframe()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(self.insert_products, df)
            future2 = executor.submit(self.create_summary, df)
            future3 = executor.submit(self.create_tags, df)

            concurrent.futures.wait([future1, future2, future3])

            result1 = await future1.result()
            result2 = future2.result()
            result3 = future3.result()

            print(result1)
            print(result2)
            print(result3)
