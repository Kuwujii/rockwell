import pandas as pd
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, path_to_data: str):
        self.df = pd.read_csv(path_to_data, sep=';')

        self.df["Value"] = pd.to_numeric(self.df["Value"].str.replace(',', '.'))
        self.df["Date"] = pd.to_datetime(self.df["Date"], dayfirst = True).dt.date.apply(lambda x: x.strftime("%Y.%m.%d"))

        self.mean = self._calculate_mean()
        self.std = self._calculate_std()

    def _calculate_mean(self):
        return self.df["Value"].mean()

    def _calculate_std(self):
        return self.df["Value"].std()

    def process_data(self) -> pd.DataFrame:
        df_for_prediction = self.df
        
        df_for_prediction["Date"] = df_for_prediction["Date"].str[:-3]
        return df_for_prediction.groupby(["Code", "Date"]).agg({"Value" : "sum"})

    def predict(self, df_for_prediction: pd.DataFrame, horizon: int) -> pd.DataFrame:
        if(horizon > 0):
            df_prediction = df_for_prediction
            margin = df_prediction.index.get_level_values("Date").nunique()
            first_month = int(df_prediction.index.get_level_values("Date").min()[5:])
            first_year = int(df_prediction.index.get_level_values("Date").min()[:-3])

            for code in df_prediction.index.get_level_values("Code").unique():
                start_month = first_month
                start_year = first_year
                for i in range(0, horizon):
                    moving_avg = 0

                    month = start_month
                    year = start_year
                    date_str = str(year)+"."+(str(month) if (month > 9) else "0"+str(month))

                    for j in range(0, margin):
                        if (code, date_str) in df_prediction.index:
                            moving_avg += df_prediction.loc[code, date_str]["Value"]
                        else:
                            df_prediction.at[(code, date_str), "Value"] = 0

                        month += 1
                        if month == 13:
                            month = 1
                            year += 1

                        date_str = str(year)+"."+(str(month) if (month > 9) else "0"+str(month))
                    
                    moving_avg /= margin
                    df_prediction.at[(code, date_str), "Value"] = moving_avg

                    start_month += 1
                    if start_month == 13:
                        start_month = 1
                        start_year += 1
            df_prediction = df_prediction.sort_index()
            return df_prediction
        return None

    def plot(self, forecast: pd.DataFrame) -> None:
        for date in forecast.index.get_level_values("Date").unique():
            forecast.at[(-1, date), "Value"] = forecast.xs(date, level = 1)["Value"].mean()

        ax = forecast.xs(-1).plot(color = 'r')
        forecast.xs(-1).loc[forecast.xs(-1).index <= self.df["Date"].max()].plot(color = 'g', ax = ax) 

        plt.show()

    def calculate_mse(self, forecast: pd.DataFrame) -> float:
        pass

if __name__ == "__main__":
    pd.options.display.float_format = '{:.2f}'.format

    signal = Signal("data.csv")

    df_for_prediction = signal.process_data()
    df_prediction = signal.predict(df_for_prediction, 10)

    print(signal.df)
    print(df_for_prediction)
    print(df_prediction)
    print(signal.mean)
    print(signal.std)
    signal.plot(df_prediction)
    