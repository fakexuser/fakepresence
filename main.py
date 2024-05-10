import sys
import os
if hasattr(sys, "_MEIPASS"): # if the script is started from an executable file
    with open(os.environ["APPDATA"] + "/fakepresence.log", "a") as f_logs:
        sys.stdout = f_logs
        sys.stderr = f_logs


import eel
from storage import AppStorage
from presence import Presence
from threading import Thread
from requests import post

storage = AppStorage()
presence = Presence(storage)


def uploadImageViaImgBB(base64image: str) -> str:
    try:
        res = post("https://api.imgbb.com/1/upload", {
            "key": "d61835a6c258a6001c1d68e727fd8771",
            "image": base64image.split(",")[1]
        })

        if not res.ok:
            return "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Cross_red_circle.svg/1024px-Cross_red_circle.svg.png"
        else:
            return res.json()["data"]["url"]
    except:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Cross_red_circle.svg/1024px-Cross_red_circle.svg.png"
    

@eel.expose
def send_event(name: str, data: any):
    if name == "ready":
        eel.send_event("init", storage.storage) 
    elif name == "updateState":
        storage.storage = data
        storage.save()
    elif name == "imageUpload":
        return uploadImageViaImgBB(data["base64"])


if __name__ == "__main__":
    Thread(target=presence.loop, daemon=True).start()
    eel.init('web')
    eel.start('main.html', size=(420, 360))