import os
from dotenv import load_dotenv

load_dotenv()


SLEEP_LOWER = 120
SLEEP_UPPER = 240
TWO_HOURS = 7200

EMAIL = os.getenv("email")

PUSHBULLET_ACCESS_TOKEN = os.getenv("pushbullet_access_token")
PUSH_TITLE = "TGTG"

ACCESS_TOKEN = os.getenv("access_token")
REFRESH_TOKEN = os.getenv("refresh_token")
USER_ID = os.getenv("user_id")
