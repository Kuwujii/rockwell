import pandas as pd


class Signal:
    def __init__(self, path_to_data: str):
        self.df = pd.read_csv(path_to_data, sep=';')
        self.mean = self._calcualte_mean()
        self.std = self._calculate_std()

    def _calculate_mean(self):
        pass

    def _calculate_std(self):
        pass

    def process_data(self) -> pd.DataFrame:
        """
        Returns a dataframe with processed data (df_for_prediction)
        """
        pass

    def predict(self, df_for_prediction: pd.DataFrame, horizon: int) -> pd.DataFrame:
        pass

    def plot(self, forecast: pd.DataFrame) -> None:
        pass

    def calculate_mse(self, forecast: pd.DataFrame) -> float:
        pass
