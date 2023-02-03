from tgtg import TgtgClient
import time
import json
import requests

from constants import (
    ACCESS_TOKEN,
    COOKIE,
    REFRESH_TOKEN,
    USER_ID,
    PUSHBULLET_ACCESS_TOKEN,
    PUSHBULLET_PHONE_IDEN,
    PUSH_TITLE,
)


def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f)


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def get_client():
    return TgtgClient(
        access_token=ACCESS_TOKEN,
        refresh_token=REFRESH_TOKEN,
        user_id=USER_ID,
        cookie=COOKIE,
    )


def time_since(start_time):
    """
    Return time since start_time
    """
    return time.time() - start_time


def send_push_notification(message):
    """
    Send push notification.
    https://github.com/rbrcsk/pushbullet.py
    """

    headers = {
        "Access-Token": f"{PUSHBULLET_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "type": "note",
        "title": PUSH_TITLE,
        "body": message,
        "device_iden": PUSHBULLET_PHONE_IDEN,
    }
    requests.post(
        "https://api.pushbullet.com/v2/pushes", headers=headers, data=json.dumps(data)
    )
