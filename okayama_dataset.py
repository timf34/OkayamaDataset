import csv



class OkayamaDataset:
    def __init__(self, cleaned_file: bool = True):
        if cleaned_file:
            self.filepath: str = 'data/okayamaTidiedTelemetry.csv'
        else:
            self.filepath: str = "data/S2_2022_Okayama_Full_MX-5_crexlive_Stint_1.csv"
        self.csv_data = self.read_csv()

    def read_csv(self):
        with open(self.filepath, 'r') as f:
            return list(csv.reader(f))

    def print_headers(self):
        print(self.csv_data[9])


def main():
    dataset = OkayamaDataset(cleaned_file=False)
    dataset.print_headers()


if __name__ == '__main__':
    main()
