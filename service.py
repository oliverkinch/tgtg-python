import time
import random
import argparse
from datetime import datetime
from constants import (
    SHORT_SLEEP_LOWER,
    SHORT_SLEEP_UPPER,
    LONG_SLEEP_LOWER,
    LONG_SLEEP_UPPER,
)

from utils import send_push_notification, get_client, send_mail_notification


class Service:
    def __init__(self, push_notification=True, mail_notification=False):
        self.push_notification = push_notification
        self.mail_notification = mail_notification

        self.client = get_client()

        # list of tuples with (name, id)
        self.items_of_interest = [
            ("Gorillas", 477157),
            # ("Coop365 - Kbh S Njalsgade (Frugt & Grønt)", 284731),
            # ("SuperBrugsen - Christianshavns Torv, København K (Frugt & Grønt)", 3321),
            # ("Irma  - Torvegade, København K (Dagligvarer)", 2849),
        ]
        self.observed = set()

    def check_items(self):
        for _, item_id in self.items_of_interest:
            if item_id not in self.observed:
                self.observed.add(item_id)

                item = self.client.get_item(item_id=item_id)
                if item["items_available"]:
                    if self.push_notification:
                        send_push_notification(message=item["display_name"])
                    if self.mail_notification:
                        send_mail_notification(subject=item["display_name"])
                self.short_sleep()

    def run(self):
        while True:
            self.get_time()
            self.check_items()
            self.long_sleep()

    @staticmethod
    def short_sleep():
        sleep_duration = random.randint(SHORT_SLEEP_LOWER, SHORT_SLEEP_UPPER)
        time.sleep(sleep_duration)

    @staticmethod
    def long_sleep():
        sleep_duration = random.randint(LONG_SLEEP_LOWER, LONG_SLEEP_UPPER)
        time.sleep(sleep_duration)

    @staticmethod
    def get_time():
        time_now = datetime.now().strftime("%H:%M:%S")
        print(f"Service running: {time_now}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--push-notification", type=int, default=1)
    parser.add_argument("-m", "--mail-notification", type=int, default=0)
    args = parser.parse_args()

    service = Service()
    service.run()
