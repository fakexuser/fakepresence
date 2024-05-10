from storage import AppStorage
from pypresence import Presence as DsPresence
from time import sleep


class Presence:
    def __init__(self, storage: AppStorage) -> None:
        self.rpc = DsPresence("1232077534976413847")
        self.storage = storage

    def create_presence_payload(self) -> dict:
        payload = {}
        data = self.storage.storage["data"]

        payload["details"] = data["details"]
        payload["state"] = data["state"]
        payload["buttons"] = []

        for button in data["buttons"]:
            button_data = data["buttons"][button]

            if button_data["show"]:
                if button_data["url"].startswith("http://") or button_data["url"].startswith("https://"):
                    payload["buttons"].append({
                        "label": button_data["label"],
                        "url": button_data["url"]
                    })

        if (len(payload["details"]) < 2):
            del payload["details"]

        if (len(payload["state"]) < 2):
            del payload["state"]

        if len(payload["buttons"]) == 0:
            del payload["buttons"]

        if data["img"] != "":
            payload["large_image"] = data["img"]

        return payload

    def loop(self) -> None:
        while True:
            try:
                while not self.storage.storage["enable"]:
                    sleep(1)
                
                try:
                    self.rpc.clear()
                except:
                    self.rpc.connect()
                
                while True:
                    if not self.storage.storage["enable"]:
                        self.rpc.clear()
                        break

                    self.rpc.update(**self.create_presence_payload())
 
                    sleep(1)

            except Exception as e: 
                print(e)
                sleep(1)