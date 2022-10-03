import pandas
import pandas as pd
import matplotlib.pyplot as plt

from typing import Union, List


class OkayamaDataset:
    def __init__(self, cleaned_file: bool = True):
        if cleaned_file:
            self.filepath: str = 'data/okayamaTidiedTelemetry.csv'
        else:
            self.filepath: str = "data/S2_2022_Okayama_Full_MX-5_crexlive_Stint_1.csv"
        self.csv_data = self.read_csv()

    def read_csv(self):
        return pd.read_csv(self.filepath, header=9)

    def get_headers(self):
        return self.csv_data.columns

    def get_rows_where_value_changes(self, column: Union[str, int]) -> List[int]:
        """
        Returns a list of the indices where the value of the column changes
        :param column: The column to check for changes
        :return: The row where the value changes
        """
        if isinstance(column, str):
            column = self.get_headers().get_loc(column)

        # This does 3 operations: 1. selects the column, 2. removes NaN values, 3. Calcs the difference between the current and previous row values (with our dataset, this will equal 1.0 when the lap goes up by 1)
        x = self.csv_data.iloc[:, column].dropna().diff()

        # This gets the indices of the values not equal to 0.0
        return x.ne(0.0)[x.ne(0.0)].index  # Source: https://stackoverflow.com/questions/52173161/getting-a-list-of-indices-where-pandas-boolean-series-is-true

    def get_dataset_two_rows(self, start_index: int, finish_index: int) -> pd.DataFrame:
        return self.csv_data.iloc[start_index:finish_index]

    def get_lists_for_plot(self):
        df = self.get_dataset_two_rows(2, 6548)

        # Note: this is really bad code but I just want to get something working for now... I don't know why I found this so hard today
        brake_list = self.convert_series_to_list(df['Brake'])
        throttle_list = self.convert_series_to_list(df['Throttle'])
        speed_list = self.convert_series_to_list(df['Speed'])

        # What even should the x-axis be? I'm just going to use the index for now
        x = [i for i in range(len(brake_list))]

        return brake_list, throttle_list, speed_list, x

    def plot_lists(self, brake_list, throttle_list, speed_list, x) -> None:
        """
        Plots the lists
        :param brake_list:
        :param throttle_list:
        :param speed_list:
        :param x:
        :return:
        """
        fig, ax = plt.subplots()
        ax.plot(x, brake_list, label='Brake')
        ax.plot(x, throttle_list, label='Throttle')
        ax.plot(x, speed_list, label='Speed')
        ax.legend()
        plt.show()

    def get_sector_information(self, df: pandas.DataFrame):
        # sourcery skip: merge-dict-assign
        """
            Sector lengths are 1km, 1km, 1km, and 700 metres.

            The car travels 3,653 metres so we will let the last sector be 653 metres long for now.

            So we need to split our dataframe into 4 dataframes along the LapDist column at 1000, 2000, 3000, and 3653
        """
        # Initialize our dict
        sectors = {}
        # Slice the dataset up until LapDist = 1000. Note that we need to convert the LapDist column to a float first
        sectors['S1'] = df[df['LapDist'].astype({"LapDist" : "float"}) < 1000]
        sectors['S2'] = df[(df['LapDist'].astype({"LapDist" : "float"}) >= 1000) & (df['LapDist'].astype({"LapDist" : "float"}) < 2000)]
        sectors['S3'] = df[(df['LapDist'].astype({"LapDist" : "float"}) >= 2000) & (df['LapDist'].astype({"LapDist" : "float"}) < 3000)]
        sectors['S4'] = df[(df['LapDist'].astype({"LapDist" : "float"}) >= 3000) & (df['LapDist'].astype({"LapDist" : "float"}) < 3653)]

        return sectors







    @staticmethod
    def convert_series_to_list(series: pd.Series) -> List:
        return series.tolist()


def main():
    dataset = OkayamaDataset(cleaned_file=True)
    # print(dataset.get_headers())
    # print(dataset.get_data())
    # print(dataset.get_rows_where_value_changes('Lap No.'))
    df = dataset.get_dataset_two_rows(2, 6548)
    # dataset.plot_lists(*dataset.get_lists_for_plot())
    dataset.get_sector_information(df)


if __name__ == '__main__':
    main()
