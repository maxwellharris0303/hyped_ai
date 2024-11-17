result = {
    "https://example.com/1": {
        "price_list": [10.99, 12.99],
        "release_dates": ["2023-01-01", "2023-02-01"]
    },
    "https://example.com/2": {
        "price_list": [9.99, 11.99],
        "release_dates": ["2023-03-01", "2023-04-01"]
    }
}

# Iterate through the dictionary
for link, data in result.items():
    print(f"Link: {link}")
    
    # Access the nested dictionary
    price_list = data["price_list"]
    release_dates = data["release_dates"]

    # Print price list
    print("  Price List:")
    for price in price_list:
        print(f"    - {price}")

    # Print release dates
    print("  Release Dates:")
    for date in release_dates:
        print(f"    - {date}")

    print()  # Add a blank line for better readability
