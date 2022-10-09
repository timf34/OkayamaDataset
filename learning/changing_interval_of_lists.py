import numpy as np

from typing import List


class ConvertInterval:
    def __init__(self):
        self.test_list = [0., 1., 2., 3., 4., 4.5, 5.07]
        self.interval: float = 0.25

    def change_interval_of_list(self, _list: List[float]) -> None:
        first_value = _list[0]
        last_value = _list[-1]

        # Round the last value to the nearest float which ends with .0, 0.25, 0.5, or 0.75
        # Note: this is so that the last value is always a multiple of 0.25
        last_value = round(last_value * 4) / 4
        print(f"last_value: {last_value}")

        # Create a new list from the first_value to the last_value, with a step size of 0.25.
        # Also ensure that the final value is included
        new_list = np.arange(first_value, last_value + self.interval, self.interval)
        print(f"new_list: {new_list}")


def main():
    x = ConvertInterval()
    x.change_interval_of_list(x.test_list)


if __name__ == "__main__":
    main()
