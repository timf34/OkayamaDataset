import matplotlib.pyplot as plt
import numpy as np
import pandas
import pandas as pd

from copy import deepcopy
from typing import Union, List, Dict, Tuple

from utils import save_dict_as_json

# Note: this is all very hardcodey, but it works for what we need tbh. I need to get more comfortable with pandas

class OkayamaDataset:
    """
        This class was primarily working with the dataset, to extract action baslines.
        I will save these action baslines locally, and create another class for merging with the Web Scraping data
    """

    def __init__(self, cleaned_file: bool = True):
        if cleaned_file:
            self.filepath: str = 'data/okayamaTidiedTelemetry.csv'
        else:
            self.filepath: str = "data/S2_2022_Okayama_Full_MX-5_crexlive_Stint_1.csv"
        self.csv_data = self.read_and_clean_csv()

        self.timing_interval: float = 0.25
        self.json_output_path: str = "data/okayama_action_baselines.json"

    def read_and_clean_csv(self) -> pd.DataFrame:
        """
            This func reads, then cleans (removes first two rows, then converts relatvie columns to floats or ints)
            it up
        """
        df = pd.read_csv(self.filepath, header=9)

        # Drop the first 2 rows (these contain weird values)
        df = df.drop(df.index[:2])

        # I am getting SettingWithCopyWarning below, but I don't know how to fix it (.loc was supposed to)

        # Convert the LapDist, Brakem, RPM, Speed and Throttle values to floats from strings, using df.at
        df.loc[:, 'LapDist'] = df.LapDist.astype(float)
        df.loc[:, 'Brake'] = df.Brake.astype(float)
        df.loc[:, 'RPM'] = df.RPM.astype(float)
        df.loc[:, 'Speed'] = df.Speed.astype(float)
        df.loc[:, 'Throttle'] = df.Throttle.astype(float)

        # Convert SessionTick, Lap No. to int
        df.loc[:, 'SessionTick'] = df.SessionTick.astype(int)
        df.loc[:, 'Lap No.'] = df['Lap No.'].astype(int)

        return df

    def get_headers(self):
        return self.csv_data.columns

    def print_five_rows(self):
        # Print rows 50 to 55
        print(self.csv_data.iloc[50:55])

    def add_full_lap_timing_columns(self):
        # Note: I am only going to work with Lap 1 for now, so this function will just work with that assumption

        # Add a Lap1 column that's the same as SessionTick, but subtracts 39951 from each value up to row 6948
        self.csv_data['Lap1TickTiming'] = self.csv_data.loc[:6948, 'SessionTick'] - 39951
        # Now add another column that converts Lap1TickTiming to seconds
        self.csv_data['Lap1SecondTiming'] = self.csv_data.loc[:6948, 'Lap1TickTiming'] / 60

    def get_rows_where_value_changes(self, column: Union[str, int]) -> List[int]:
        """
        Returns a list of the indices where the value of the column changes (mostly a helper function)
        :param column: The column to check for changes
        :return: The row where the value changes
        """
        if isinstance(column, str):
            column = self.get_headers().get_loc(column)

        # This does 3 operations: 1. selects the column, 2. removes NaN values, 3. Calcs the difference between the current and previous row values (with our dataset, this will equal 1.0 when the lap goes up by 1)
        x = self.csv_data.iloc[:, column].dropna().diff()

        # This gets the indices of the values not equal to 0.0
        return x.ne(0.0)[x.ne(0.0)].index  # Source: https://stackoverflow.com/questions/52173161/getting-a-list-of-indices-where-pandas-boolean-series-is-tru

    def get_dataset_two_rows(self, start_index: int, finish_index: int) -> pd.DataFrame:
        return self.csv_data.iloc[start_index:finish_index]

    def get_lists_for_plot(self):
        df = self.get_dataset_two_rows(0, 6546)

        # Note: this is really bad code but I just want to get something working for now... I don't know why I found this so hard today
        brake_list = self.convert_series_to_list(df['Brake'])
        throttle_list = self.convert_series_to_list(df['Throttle'])
        speed_list = self.convert_series_to_list(df['Speed'])

        # What even should the x-axis be? I'm just going to use the index for now
        x = list(range(len(brake_list)))

        return brake_list, throttle_list, speed_list, x

    def plot_x_y(self, x: List, y: List, y_axis_name: str, sector_number: str) -> None:
        """
            Plot x and y, ensuring that the spacing of y-axis values isn't too crowded for large numbers
        """
        # Get the max value of y
        max_y = max(float(i) for i in y)
        # Get the min value of y
        min_y = min(float(i) for i in y)
        # Get the difference between the max and min
        diff = max_y - min_y
        # Get the number of ticks we want
        num_ticks = 2
        # Get the spacing between ticks
        tick_spacing = diff / num_ticks

        # And now the same for the x axis
        max_x = max(float(i) for i in x)
        min_x = min(float(i) for i in x)
        diff_x = max_x - min_x
        num_ticks_x = 2
        tick_spacing_x = diff_x / num_ticks_x

        # Make the plot
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(xlabel='Sector Time (s)', ylabel=f'{y_axis_name}', title=f'{sector_number} {y_axis_name} vs Sector Time')
        ax.grid()
        ax.xaxis.set_major_locator(plt.MultipleLocator(tick_spacing_x))
        ax.yaxis.set_major_locator(plt.MultipleLocator(tick_spacing))
        plt.show()

    @staticmethod
    def add_sector_timing_columns(df_dict: Dict[str, pandas.DataFrame]) -> None:
        """
            This function accepts the dict with the dataframes for each sector from below.
            It then adds a timing column for each of those df's in seconds and in ticks (60FPS) to the same
            df.
        """
        # Note: this seems hard to do in a general way, so I'm actually going to hard code a lot of it.

        # Sector 1
        df_dict['S1']['S1TickTiming'] = deepcopy(df_dict['S1'].loc[:, "SessionTick"] - 39949)  # 39951 is the SessionTick value for the start of 1st sector
        df_dict['S1']['S1SecondTiming'] = deepcopy(df_dict['S1']['S1TickTiming'] / 60)

        df_dict['S2']['S2TickTiming'] = deepcopy(df_dict['S2'].loc[:, "SessionTick"] - 41726)  # 41726 is the SessionTick value for the start of the 2nd sector (not the 2nd lap!)
        df_dict['S2']['S2SecondTiming'] = deepcopy(df_dict['S2']['S2TickTiming'] / 60)

        df_dict['S3']['S3TickTiming'] = deepcopy(df_dict['S3'].loc[:, "SessionTick"] - 43277)  # 43277 is the SessionTick value for the start of the 3rd sector
        df_dict['S3']['S3SecondTiming'] = deepcopy(df_dict['S3']['S3TickTiming'] / 60)

        df_dict['S4']['S4TickTiming'] = deepcopy(df_dict['S4'].loc[:, "SessionTick"] - 45455)  # 45455 is the SessionTick value for the start of the 4th sector
        df_dict['S4']['S4SecondTiming'] = deepcopy(df_dict['S4']['S4TickTiming'] / 60)


    def get_sector_information(self, df: pandas.DataFrame):
        # sourcery skip: merge-dict-assign
        """
            Sector lengths are 1km, 1km, 1km, and 700 metres.

            The car travels 3,653 metres so we will let the last sector be 653 metres long for now.

            So we need to split our dataframe into 4 dataframes along the LapDist column at 1000, 2000, 3000, and 3653
        """
        # Initialize our dict
        sectors = {}

        # Slice the dataset up until LapDist = 1000.
        sectors['S1'] = df[df['LapDist'] < 1000]
        sectors['S2'] = df[(df['LapDist'] >= 1000) & (df['LapDist'] < 2000)]
        sectors['S3'] = df[(df['LapDist'] >= 2000) & (df['LapDist'] < 3000)]
        sectors['S4'] = df[(df['LapDist'] >= 3000) & (df['LapDist'] < 3653)]
        self.add_sector_timing_columns(sectors)  # Add timing columns to each sector df

        return sectors

    @staticmethod
    def create_a_larger_extrapolated_x_y_axis(x: List[float], y: List[float]) -> Tuple[List[float], List[float]]:
        """
            This function takes in a list of x and y values and returns a new list of x and y values that is 10x longer
            than the original list. The new list is created by interpolating the original list.
        """
        # Add 2 to the last value of x (this is arbitrary, just testing if it works)
        temp_x = x.copy()  # Have to use a copy of x... otherwise it would change the original x
        temp_x[-1] += 2  # This works for adding or subtracting!
        # Create a new list of x values that is the same size as the original vector.
        new_x = np.linspace(temp_x[0], temp_x[-1], num=len(x))
        # Convert np array to list and print
        new_x = new_x.tolist()
        # Create a new list of y values that is 10x longer than the original list
        new_y = np.interp(new_x, new_x, y)

        return new_x, new_y

    def make_our_plots(self, print_list: bool = False):
        sectors = self.get_sector_information(self.get_dataset_two_rows(0, 6546))  # Note that these must be 0 and 6546... otherwise we'll get some overflow.

        list_of_data_to_plot = ["Brake", "Throttle", "Speed", "RPM", "Gear"]
        for sector in sectors:
            print(f"Making plots for sector {sector}")
            for y_axis_name in list_of_data_to_plot:

                # Get the y-axis data
                y: List = sectors[sector][y_axis_name].tolist()
                # Get the x-axis data
                # x = sectors[sector]['LapDist'].tolist()  # If we want to use lap distance as the x-axis
                x: List = sectors[sector][f"{sector}SecondTiming"].tolist()

                # Change interval of x-axis
                x = self.convert_interval_of_list(x)

                # Change the num_elements of y to be the same as x
                y = self.change_num_elements(y, len(x))

                new_x, new_y = self.create_a_larger_extrapolated_x_y_axis(x, y)

                if print_list:
                    print(f"Here is the raw list: \n {y}")

                # Make the plot
                self.plot_x_y(x=x, y=y, y_axis_name=y_axis_name, sector_number=sector)
                self.plot_x_y(x=new_x, y=new_y, y_axis_name=y_axis_name, sector_number=sector)

    @staticmethod
    def convert_series_to_list(series: pd.Series) -> List:
        return series.tolist()

    @staticmethod
    def save_numpy_arrays(array: np. array, filename: str):
        np.save(filename, array)

    def convert_interval_of_list(self, _list: List[float]) -> List[float]:
        first_value = _list[0]
        last_value = _list[-1]

        # Round the last value to the nearest float which ends with .0, 0.25, 0.5, or 0.75
        # Note: this is so that the last value is always a multiple of 0.25
        last_value = round(last_value / self.timing_interval) * self.timing_interval

        new_list = np.arange(first_value, last_value + self.timing_interval, self.timing_interval)
        # Convert np array to list and return
        return new_list.tolist()

    @staticmethod
    def change_num_elements(_list: List[float], num_elements: int) -> List[float]:
        # Use np.interp to create a new list that has num_elements elements
        new_list = np.interp(np.linspace(0, len(_list) - 1, num_elements), np.arange(len(_list)), _list)
        return new_list.tolist()

    def convert_time_axis_interval(self, print_info: bool = False) -> None:
        """
            This function converts the time axis interval to 0.25, and then changes the other lists accordingly.

            It then saves this to a json file as a dict.
        """
        sectors = self.get_sector_information(self.get_dataset_two_rows(0, 6546))
        list_of_data_to_plot = ["Brake", "Throttle", "Speed", "RPM", "Gear"]

        # Initializing our dict
        temp_dict = {"S1": {}, "S2": {}, "S3": {}, "S4": {}}
        for sector in sectors:
            for key in list_of_data_to_plot:
                temp_dict[sector][key] = []

        for sector in sectors:

            for count, y_axis_name in enumerate(list_of_data_to_plot):
                # Get the x and y axes data
                x: List = sectors[sector][f"{sector}SecondTiming"].tolist()
                y: List = sectors[sector][y_axis_name].tolist()

                # Make new lists
                new_x = self.convert_interval_of_list(x)
                new_y = self.change_num_elements(y, len(new_x))

                # Save the x-axis to our dict just once per sector
                if count == 0:
                    temp_dict[sector][f"{sector}SecondTiming"] = new_x

                # Add the new y values to the new dict
                temp_dict[sector][y_axis_name] = new_y


                if print_info:
                    print(f"This is sector {sector}")

                    print(f"Here is the raw y axis list: \n {y}")
                    print(f"Here is the raw x axis list: \n {x}")
                    print(f"Here is the length of x and y: {len(x)} - {len(y)}")

                    print(f"Here is the new x axis list: \n {new_x}")
                    print(f"Here is the new y axis list: \n {new_y}")
                    print(f"Here is the length of new_x and new_y: {len(new_x)} - {len(new_y)}")

        save_dict_as_json(output_path=self.json_output_path, _dict=temp_dict)




def main():
    dataset = OkayamaDataset(cleaned_file=True)
    # dataset.add_full_lap_timing_columns()
    # print(dataset.get_headers())
    # dataset.print_five_rows()
    # print(dataset.get_data())
    print(dataset.get_rows_where_value_changes('Lap No.'))
    #  df = dataset.get_dataset_two_rows(2, 6548)
    # dataset.get_sector_information(df)
    # dataset.make_our_plots(print_list=False)
    dataset.convert_time_axis_interval()


if __name__ == '__main__':
    main()
