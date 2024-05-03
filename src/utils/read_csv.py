from abc import ABC, abstractmethod
from io import BytesIO, StringIO
import pandas as pd
from src.utils.dataset_type import dataset_types


class ReadCsv(ABC):
    @abstractmethod
    async def get_csv_file(self) -> BytesIO:
        pass

    async def read_csv(self, csv_file: BytesIO) -> pd.DataFrame:
        with csv_file as file:
            csv_data = file.read().decode("utf-8")
            df = pd.read_csv(StringIO(csv_data), dtype=dataset_types, sep=",")
        df = df.dropna(subset=["review_text"])
        return df
