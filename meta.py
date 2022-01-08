import json
from typing import Union

from config import Config
from edict import Edict


class Meta:
    def __init__(self):
        config = Config()
        with open(config.config.paths.nameHandlers, 'r') as handlers:
            self.handlers = Edict(json.load(handlers))

    def getname(self, title: str, id: str) -> Union[str, None]:
        print(self.handlers.keys())
        if id not in self.handlers.keys():
            print("skipping")
            return None

        print(self.handlers[id].items())
        for key, value in self.handlers[id].items():
            print(key)
            print(value)
