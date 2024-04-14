from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from io import StringIO
import pandas as pd
from ..utils.dataset_type import dataset_types


class ReadCsv(ABC):
    @abstractmethod
    def get_csv_file(self):
        pass

    def read_csv(self) -> pd.DataFrame:
        csv_file = self.get_csv_file()
        with StringIO(csv_file.read().decode("utf-8")) as csv_data:
            with redirect_stdout(None):
                df = pd.read_csv(csv_data, dtype=dataset_types)
        df = df.dropna(subset=["review_text"])
        return df
