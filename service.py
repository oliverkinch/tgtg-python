import time
import random
import argparse
from datetime import datetime
from constants import SLEEP_LOWER, SLEEP_UPPER, TWO_HOURS

from utils import (
    send_push_notification,
    get_client,
    time_since,
    load_json,
)


class Service:
    def __init__(self, items_to_track, push_notification=True, mail_notification=False):
        self.push_notification = push_notification
        self.mail_notification = mail_notification

        self.client = get_client()
        self.start_time = time.time()
        self.items_to_track = items_to_track
        self.print_items_that_service_tracks()

    def run(self):
        while True:
            self.get_time()
            self.check_items()
            if time_since(self.start_time) > TWO_HOURS:
                self.restart_client()
                self.start_time = time.time()

    def check_items(self):
        for item_id in self.items_to_track:
            item = self.client.get_item(item_id=item_id)
            if item["items_available"]:
                print(f"\n\t{item['display_name']} is available\n")
                self.send_notification(item)
            self._sleep()

    def restart_client(self):
        self.client = get_client()

    def send_notification(self, item):
        if self.push_notification:
            send_push_notification(message=item["display_name"])

    def print_items_that_service_tracks(self):
        favorite_items = load_json("favorite_items.json")
        print("Service tracking:")
        for item_id in self.items_to_track:
            print(f"\t{favorite_items[str(item_id)]}")

    @staticmethod
    def _sleep():
        sleep_duration = random.randint(SLEEP_LOWER, SLEEP_UPPER)
        time.sleep(sleep_duration)

    @staticmethod
    def get_time():
        time_now = datetime.now().strftime("%H:%M:%S")
        print(f"{time_now}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--push-notification", type=int, default=1)
    parser.add_argument("-m", "--mail-notification", type=int, default=0)
    parser.add_argument(
        "-l",
        "--list",
        nargs="+",
        help="list of items ids (separated by a space)",
        type=int,
        default=[477157],
    )
    args = parser.parse_args()

    push_notification = args.push_notification
    mail_notification = args.mail_notification
    items_to_track = args.list
    service = Service(items_to_track, push_notification, mail_notification)
    service.run()
