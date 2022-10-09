import json
import os

from typing import Dict


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
