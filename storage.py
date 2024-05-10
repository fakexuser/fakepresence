import os
import json


default_storage = {
    "enable": False,
    "buttonView": False,
    "buttonState": 1,
    "data": {
        "img": "",
        "details": "",
        "state": "",
        "buttons": {
            1: { "label": "", "url": "", "show": False },
            2: { "label": "", "url": "", "show": False }
        }
    }
}


class AppStorage:
    def __init__(self) -> None:
        self.path = os.environ["APPDATA"] + "/FakePresence/storage.json"
        self.storage = {} 

        if not os.path.exists(os.environ["APPDATA"] + "/FakePresence"):
            os.mkdir(os.environ["APPDATA"] + "/FakePresence")

        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(default_storage, file, indent=4)

        with open(self.path, "r", encoding="utf-8") as file:
            self.storage = json.load(file)

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.storage, file, indent=4)