import time
import random
import argparse
from datetime import datetime
from constants import SLEEP_LOWER, SLEEP_UPPER, ONE_HOUR

from utils import send_push_notification, get_client, send_mail_notification, time_since


class Service:
    def __init__(self, push_notification=True, mail_notification=False):
        self.push_notification = push_notification
        self.mail_notification = mail_notification

        self.client = get_client()
        self.start_time = time.time()
        # list of tuples with (name, id)
        self.items_of_interest = [
            ("Gorillas", 477157),
            # ("Coop365 - Kbh S Njalsgade (Frugt & Grønt)", 284731),
            # ("SuperBrugsen - Christianshavns Torv, København K (Frugt & Grønt)", 3321),
            # ("Irma  - Torvegade, København K (Dagligvarer)", 2849),
        ]

    def check_items(self):
        for _, item_id in self.items_of_interest:
            item = self.client.get_item(item_id=item_id)
            if item["items_available"]:
                self._send_notification(item)
            self._sleep()

    def run(self):
        while True:
            self.get_time()
            self.check_items()
            if time_since(self.start_time) > ONE_HOUR:
                self.restart_client()
                self.start_time = time.time()

    def restart_client(self):
        self.client = get_client()

    def _send_notification(self, item):
        if self.push_notification:
            send_push_notification(message=item["display_name"])
        if self.mail_notification:
            send_mail_notification(subject=item["display_name"])

    @staticmethod
    def _sleep():
        sleep_duration = random.randint(SLEEP_LOWER, SLEEP_UPPER)
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
