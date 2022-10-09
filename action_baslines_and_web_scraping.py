from typing import List

from mqtt_sender import MQTTSender
from utils import open_json_as_dict


class ActionBaselines:
    def __init__(self):
        self.path_to_action_baselines = "data/okayama_action_baselines.json"
        self.action_baselines = open_json_as_dict(self.path_to_action_baselines)
        self.actions: List[str] = ["Brake", "Throttle", "Speed", "RPM", "Gear"]

        self.mqtt_client = MQTTSender()

    def iterate_through_action_baseline(self) -> None:
        """
        Iterates through each sector, printing all information from all keys
        """
        # for sector in self.action_baselines:
        #     print(f"Sector: {sector}")
        #     for i in zip(self.action_baselines[sector][self.actions[0]], self.action_baselines[sector][self.actions[1]], self.action_baselines[sector][self.actions[2]], self.action_baselines[sector][self.actions[3]], self.action_baselines[sector][self.actions[4]]):
        #         print(i)

        # Now lets do the same as above, but cleaner (again, github copilot is amazing! I need to learn more on pointers in Python)
        for sector in self.action_baselines:
            print(f"Sector: {sector}")
            for i in zip(*[self.action_baselines[sector][action] for action in self.actions]):
                print(i)


def main():
    action_baselines = ActionBaselines()
    action_baselines.iterate_through_action_baseline()


if __name__ == "__main__":
    main()

