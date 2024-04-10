from fastapi import UploadFile
import pandas as pd
from ..utils.timer import timing  # Assuming this imports correctly
from io import StringIO
from contextlib import redirect_stdout


class Processamento:
    def __init__(self, csv: UploadFile) -> None:
        self.__csv = csv

    @timing
    def __clear_data(self) -> pd.DataFrame:
        with StringIO(self.__csv.file.read().decode("utf-8")) as csv_data:
            with redirect_stdout(None):
                df = pd.read_csv(csv_data)
        df = df.dropna(subset=["review_text"])
        return df

    def process_data(self):
        df, timer = self.__clear_data()
        return timer