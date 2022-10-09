import numpy as np

from typing import List

# Note: I am actually just going to save the ActionBaselines as a dict


class SavingAndLoadingNPArrays:
    def __init__(self):
        self.arr1 = np.array([1., 2., 3., 4., 5.])
        self._list1 = [1., 2., 3., 4., 5.]
        self.file_name = "test_file.npy"

    def save_np_array(self) -> None:
        np.save(self.file_name, self.arr1)

    def load_np_array(self) -> None:
        arr2 = np.load(self.file_name)
        print(f"arr2: {arr2}")


def main():
    x = SavingAndLoadingNPArrays()
    x.save_np_array()
    x.load_np_array()


if __name__ == "__main__":
    main()
