import csv
import pandas as pd
import matplotlib as mpl


class OkayamaDataset:
    def __init__(self, cleaned_file: bool = True):
        if cleaned_file:
            self.filepath: str = 'data/okayamaTidiedTelemetry.csv'
        else:
            self.filepath: str = "data/S2_2022_Okayama_Full_MX-5_crexlive_Stint_1.csv"
        self.csv_data = self.read_csv()

    def read_csv(self):
        with open(self.filepath, 'r') as f:
            print("type of csv reader: ", type(csv.reader(f)))
            return list(csv.reader(f))

    def get_headers(self):
        return self.csv_data[9]

    def get_data(self):
        return self.csv_data[10:]



def main():
    dataset = OkayamaDataset(cleaned_file=True)
    print(dataset.get_headers())
    # print(dataset.get_data())


if __name__ == '__main__':
    main()
