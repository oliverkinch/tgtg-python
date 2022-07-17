import smtplib
from tgtg import TgtgClient
from dotenv import load_dotenv
import os
import re
from pushbullet import PushBullet
import time
import json



load_dotenv()


def print_credentials(email="tgtghaps@gmail.com"):
    """
    Send approval email -> accept this and get credentials
    (assess_token, refresh_token, user_id), which can be saved in .env
    """
    client = TgtgClient(email=email)
    credentials = client.get_credentials()
    print(credentials)


def favorite_items_to_json():
    """
    Print names and ids of favorite items
    """
    favorite_items = {}
    client = get_client()
    items = client.get_items(page_size=100, favorites_only=True)
    for item in items:
        item_name = item["display_name"]
        item_id = item["item"]["item_id"]
        favorite_items[item_id] = item_name

    save_json(favorite_items, "favorite_items.json")


def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)


def load_json(path):
    """
    Load json file
    """
    with open(path, 'r') as f:
        return json.load(f)


def send_mail_notification(subject="", text=""):
    """
    Send notification email
    """
    message = f"Subject: {subject}\n\n{text}"
    message = re.sub(r"[æøåÆØÅ]", "", message)  # Remoev æøå

    content = message

    my_mail = "tgtghaps@gmail.com"

    mail = smtplib.SMTP("smtp.gmail.com", 587)
    mail.ehlo()
    mail.starttls()
    mail.login(
        my_mail, "hrtluovbkaymovsg"
    )  # https://stackoverflow.com/a/72529505/18472321
    mail.sendmail(my_mail, my_mail, content)
    mail.close()

    print("Sent")


def get_client():
    """
    Read credentials from .env and return TgtgClient
    """
    access_token = os.getenv("access_token")
    refresh_token = os.getenv("refresh_token")
    user_id = os.getenv("user_id")

    return TgtgClient(
        access_token=access_token, refresh_token=refresh_token, user_id=user_id
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
    apikey = os.getenv("APIKEY-pushbullet")
    pb = PushBullet(apikey)
    pb.push_note("TGTG", message)


if __name__ == "__main__":
    items = favorite_items_to_json()
    # send_notification_mail(subject='Hello', text='World')
    # get_client()
    # print_credentials(email="tgtghaps@gmail.com")
    pass
