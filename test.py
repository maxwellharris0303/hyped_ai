import re
from datetime import datetime

def should_post_item(item):
    """
    Determine whether an item should be posted based on its release date and stock status.
    """
    # Extract information from the item
    release_date = item.get("release_date")  # Expected format: "YYYY-MM-DD"
    stock_status = item.get("stock_status", "").lower()
    pre_order_status = item.get("pre_order", False)
    
    # Current date
    today = datetime.now().date()

    # Check if the item is out of stock
    if re.search(r"(out of stock|sold out|unavailable)", stock_status):
        return False

    # Check if the release date is in the future
    if release_date:
        release_date_obj = datetime.strptime(release_date, "%Y-%m-%d").date()
        if release_date_obj > today:
            return True

    # Check if the item is in stock or available for pre-order
    if "in stock" in stock_status or pre_order_status:
        return True

    return False

# Example items
items = [
    {"name": "Barbie A", "release_date": "2024-11-21", "stock_status": "in stock", "pre_order": False},
    {"name": "Barbie B", "release_date": "2024-11-15", "stock_status": "out of stock", "pre_order": False},
    {"name": "Barbie C", "release_date": "2024-11-17", "stock_status": "pre-order available", "pre_order": True},
]

# Filter items
for item in items:
    if should_post_item(item):
        print(f"Post: {item['name']}")
    else:
        print(f"Do not post: {item['name']}")
