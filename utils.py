from tgtg import TgtgClient
import os
from pushbullet import PushBullet
import time
import json
from constants import ACCESS_TOKEN, REFRESH_TOKEN, USER_ID, PUSHBULLET_APIKEY, PUSH_NOTE


def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f)


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def get_client():
    return TgtgClient(
        access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN, user_id=USER_ID
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
    apikey = os.getenv(PUSHBULLET_APIKEY)
    pb = PushBullet(apikey)
    pb.push_note(PUSH_NOTE, message)
