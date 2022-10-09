from mqtt_sender import MQTTSender
from utils import open_json_as_dict


class ActionBaselines:
    def __init__(self):
        self.path_to_action_baselines = "data/okayama_action_baselines.json"
        self.action_baselines = open_json_as_dict(self.path_to_action_baselines)
        self.mqtt_client = MQTTSender()
