import json


class ConfigService:

    def __init__(self):
        with open('config.json', 'r') as config_file:
            self.config = json.load(config_file)
