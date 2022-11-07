from utils import get_client, save_json


def favorite_items_to_json():
    """
    Write favorite items to JSON file
    """
    favorite_items = {}
    client = get_client()
    items = client.get_items(page_size=100, favorites_only=True)
    for item in items:
        item_name = item["display_name"]
        item_id = item["item"]["item_id"]
        favorite_items[item_id] = item_name

    save_json(favorite_items, "favorite_items.json")


if __name__ == "__main__":
    favorite_items_to_json()
