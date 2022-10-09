import json
import numpy as np
import os


from typing import Dict, List


def save_dict_as_json(output_path: str, _dict: Dict) -> None:
    # Ensure file_path exists, if not create it
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    with open(output_path, "w") as f:
        json.dump(_dict, f, indent=4)


def open_json_as_dict(input_path: str) -> Dict:
    # Ensure file exists
    if not os.path.exists(input_path):
        raise Exception(f"File does not exist: {input_path}")

    with open(input_path, "r") as f:
        return json.load(f)


def convert_interval_of_list(_list: List[float], timing_interval: float) -> List[float]:
    first_value = 0  # As we are just using this for timing, we can start at 0
    last_value = _list[-1]

    # Round the last value to the nearest float which ends with .0, 0.25, 0.5, or 0.75
    # Note: this is so that the last value is always a multiple of 0.25
    last_value = round(last_value / timing_interval) * timing_interval

    new_list = np.arange(first_value, last_value + timing_interval, timing_interval)
    # Convert np array to list and return
    return new_list.tolist()


def change_num_elements(_list: List[float], num_elements: int) -> List[float]:
    # Use np.interp to create a new list that has num_elements elements
    new_list = np.interp(np.linspace(0, len(_list) - 1, num_elements), np.arange(len(_list)), _list)
    return new_list.tolist()
