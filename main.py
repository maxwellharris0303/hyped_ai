from time import sleep
import undetected_chromedriver as uc
from difflib import SequenceMatcher
from urllib.parse import urlparse, urlunparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import discord  # Add discord library for bot functionality
import re
import asyncio
import statistics
import urllib.parse
import asyncio
from datetime import datetime
import random
from openai import OpenAI
import discord_notifier
import google_search

def is_similar(a, b, threshold=0.70):
    """Check if two strings are similar by a given threshold."""
    return SequenceMatcher(None, a, b).ratio() > threshold

def is_similar_sportscard(a, b, threshold=0.90):
    """Check if two strings are similar by a given threshold."""
    return SequenceMatcher(None, a, b).ratio() > threshold

def clean_title(title):
    # Remove "presale" or similar terms (case-insensitive)
    title = re.sub(r'\b(confirmed presale|presale confirmed|confirmed pre-sale|pre-sale confirmed|presale|pre-order|preorder|pre-sale|order)\b', '', title, flags=re.IGNORECASE)
    # Remove emojis (any character that isn't a basic letter, number, punctuation, or whitespace)
    title = re.sub(r'[^\w\s,.\'-]', '', title)
    # Remove extra spaces from the string
    title = re.sub(r'\s+', ' ', title).strip()
    return title
    

# below finds hype flips
options = uc.ChromeOptions()
driver = uc.Chrome(version_main=130)
driver.maximize_window()
driver.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw=presale&_sacat=0&_sop=10")

# Wait for the items with the class 's-item' to load
# items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item")))
ul_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul[class=\"srp-results srp-list clearfix\"]")))
items = ul_element.find_elements(By.CSS_SELECTOR, "li[class*=\"s-item\"]")
# print(len(items))
# items = items[:10]

title_list = []
price_list = []
image_list = []
for item in items:
    # Extract the title of the item
    title_element = item.find_element(By.CLASS_NAME, 's-item__title')
    title_text = (title_element.text.strip()).replace("NEW LISTING", "")

    if title_text:  # If the title is not blank
        

        # Extract the price of the item
        price_element = item.find_element(By.CLASS_NAME, "s-item__price")
        price_text = price_element.text.strip()

        # Use regex to extract the first valid price number (ignoring ranges like "$10.00 to $20.00")
        price_value = re.findall(r'\d+\.?\d*', price_text)  # Extracts numbers
        if len(price_value) > 0:
            # print(f"Title found: {title_text}")
            # print(f"Price: {price_value[0]}")
            title_list.append(title_text)
            price_list.append(price_value[0])
            image_element = item.find_element(By.TAG_NAME, "img")
            image_list.append(image_element.get_attribute('src'))

# for title in title_list:
#     if "presale" not in title.lower():
#         print(title)
# sleep(5000)
# print(title_list)
# print(price_list)
# print(image_list)
main_window = driver.current_window_handle

for title, image, price in zip(title_list, image_list, price_list):
    driver.switch_to.new_window('tab')
    sanitized_title_text = urllib.parse.quote_plus(title)
    search_ebay_flip = "https://www.ebay.com/sch/i.html?_nkw=" + sanitized_title_text + "&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
    driver.get(search_ebay_flip)
    sleep(5)
    # Wait for the eBay page to load and fetch elements with the class 's-item s-item__pl-on-bottom'
    # comparison_items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item.s-item__dsa-on-bottom.s-item__pl-on-bottom")))
    ul_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul[class=\"srp-results srp-list clearfix\"]")))
    comparison_items = ul_element.find_elements(By.CSS_SELECTOR, "li[class*=\"s-item\"]")
    # print(len(comparison_items))
    
    # sleep(3)
    

    if len(comparison_items) > 10:
        comparison_items = comparison_items[:10]
        # break


    positive_values = []

    for item in comparison_items:
        try:
            # Extract the title of the current item
            flip_element = item.find_element(By.CLASS_NAME, 's-item__title')
            flip_text = flip_element.text.strip()
            # print(flip_text)


            # Check if the title contains a year (e.g., any four digits)
            contains_year = re.search(r'\b\d{4}\b', flip_text)

            # Check if the title contains a '#' sign
            contains_hash = '#' in flip_text

            # Call is_similar_sportscard if the title contains a year or contains a '#'
            if contains_year or contains_hash:
                similar_check = is_similar_sportscard(flip_text.lower(), title.lower())
            else:
                similar_check = is_similar(flip_text.lower(), title.lower())
            # print("-----------")
            # print(title)
            # print(similar_check)

            if similar_check:
                # Find and process positive elements
                green_elements = item.find_elements(By.CLASS_NAME, "POSITIVE")

                # Only take every other positive element starting from the second one
                for index, element in enumerate(green_elements):
                    if index % 2 == 0:
                        continue  # Skip the even ones
                    try:
                        # Extract value, remove $ sign and clean it
                        value = element.text.replace('$', '').replace('EUR', '').strip()
                        positive_values.append(float(value))  # Convert to float for averaging
                    except StaleElementReferenceException:
                        print("Element went stale, skipping this one.")

        except Exception as e:
            print(f"Error processing item: {e}")

    # print(f"POSTIVE_VALUES: {positive_values}")
    # Calculate the average sell price
    if positive_values:
        average_sold_price = f"${statistics.mean(positive_values):.2f}"  # Format the average to 2 decimal places
    else:
        average_sold_price = "$Unreliable Sales Data Found"


    # print(f"Average sold price: {average_sold_price}")
    if average_sold_price != "$Unreliable Sales Data Found":
        result = google_search.search(title)
        if len(result) !=0:
            # Loop through the dictionary and print each URL with its prices
            possible_prices = []
            possible_buy_links = []
            release_dates = []

            for data in result:
                link = data["link"]
                prices = data["price_list"]
                dates = data["release_dates"]

                possible_buy_links.append(link)

                print(f"Link: {link}")
                # Print price list
                print("  Price List:")
                for price in prices:
                    print(f"    - {price}")
                    possible_prices.append(float(re.sub(r'[\$,USDusd\s]', '', price)))

                # Print release dates
                print("  Release Dates:")
                for date in dates:
                    print(f"    - {date}")
                    release_dates.append(date)

                print()  # Add a blank line for better readability

            # Convert strings to datetime objects
            date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in release_dates]
            # Get today's date
            today = datetime.today()
            # Filter for future dates
            future_dates = [date for date in date_objects if date > today]
            # Find the nearest date
            nearest_date = ""
            if len(future_dates) != 0:
                min_date = min(future_dates, key=lambda x: abs((x - today).days))
                nearest_date = min_date.strftime("%B %d, %Y")
                print("Nearest date:", nearest_date)


            if len(possible_prices) != 0:
                price_range = f"Price range: ${min(possible_prices):.2f} - ${max(possible_prices):.2f}"
                print(price_range)
                discord_notifier.notify_to_discord_channel(clean_title(title), image, average_sold_price, possible_buy_links, price_range, nearest_date, search_ebay_flip)
    driver.close()
    driver.switch_to.window(main_window)
