import time

from copy import deepcopy
from typing import List, Union, Generator

from mqtt_sender import MQTTSender
from utils import open_json_as_dict


class ActionBaselines:
    def __init__(self):
        self.path_to_action_baselines = "data/okayama_action_baselines.json"
        self.action_baselines = open_json_as_dict(self.path_to_action_baselines)
        self.actions: List[str] = ["Brake", "Throttle", "Speed", "RPM", "Gear"]

        self.mqtt_client = MQTTSender()

    def iterate_through_action_baseline(self, sector_number: Union[int, str]) -> Generator:
        """
        Iterates through a given sector, printing all information from all keys
        """
        # for sector in self.action_baselines:
        #     print(f"Sector: {sector}")
        #     for i in zip(self.action_baselines[sector][self.actions[0]], self.action_baselines[sector][self.actions[1]], self.action_baselines[sector][self.actions[2]], self.action_baselines[sector][self.actions[3]], self.action_baselines[sector][self.actions[4]]):
        #         print(i)

        # Now lets do the same as above, but cleaner (again, github copilot is amazing! I need to learn more on pointers in Python)

        # Check if sector_number is an int
        if isinstance(sector_number, int):
            sector_number = f"S{sector_number}"

        # Ensure that sector_number is a valid sector (i.e. ["S1", "S2", "S3", "S4"])
        if sector_number not in self.action_baselines:
            raise KeyError(f"Invalid sector number: {sector_number}. Must be one of: {list(self.action_baselines.keys())}")

        temp_actions = deepcopy(self.actions)
        temp_actions.append(f"{sector_number}SecondTiming")

        # Yields the data from the action baselines...
        yield from zip(*[self.action_baselines[sector_number][action] for action in self.actions])

    def create_dataset_structure(self, sector_number: Union[int, str]) -> None:
        """
        Creates a dataset structure for the given sector number
        """
        # Check if sector_number is an int
        if isinstance(sector_number, int):
            sector_number = f"S{sector_number}"

        # Ensure that sector_number is a valid sector (i.e. ["S1", "S2", "S3", "S4"])
        if sector_number not in self.action_baselines:
            raise KeyError(f"Invalid sector number: {sector_number}. Must be one of: {list(self.action_baselines.keys())}")

    def send_to_mqtt(self):
        for i in self.iterate_through_action_baseline(1):
            self.mqtt_client.publish_to_topic(i)
            time.sleep(0.25)


def main():
    action_baselines = ActionBaselines()
    # action_baselines.iterate_through_action_baseline()
    action_baselines.send_to_mqtt()


if __name__ == "__main__":
    main()

