from tgtg import TgtgClient

from constants import EMAIL


def print_credentials(email):
    """
    Send approval email -> accept this and get credentials
    (assess_token, refresh_token, user_id), which must be saved in .env
    """
    client = TgtgClient(email=email)
    credentials = client.get_credentials()
    print(credentials)


if __name__ == "__main__":
    print_credentials(email=EMAIL)
