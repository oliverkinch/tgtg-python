from utils import get_client


def check_for_new_items():
    """
    Check for new items in radius of 3 km around Gizgården.
    """
    client = get_client()
    items = client.get_items(
        favorites_only=False,
        latitude=55.665501,
        longitude=12.594691,
        radius=3,
        page_size=200,
    )
    for item in items:
        item_id = item["item"]["item_id"]
        new_item = item["new_item"]
        favorite = item["favorite"]
        if new_item and not favorite and item_id:
            display_name = item["display_name"]
            print(display_name)


if __name__ == "__main__":
    check_for_new_items()
