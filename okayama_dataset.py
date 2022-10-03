import pandas as pd
import matplotlib as mpl

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



def main():
    dataset = OkayamaDataset(cleaned_file=True)
    # print(dataset.get_headers())
    # print(dataset.get_data())
    dataset.get_rows_where_value_changes('Lap No.')


if __name__ == '__main__':
    main()
