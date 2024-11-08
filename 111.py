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
import datetime
import random
from openai import OpenAI

# Discord bot token and channel ID
DISCORD_TOKEN = 'MTMwMDkxMTc2MTU0ODkwNjUxNg.GslcYm.kUi-YZ-WvZeHch8pL6KcR7fM4JAcPjTAyZO6iA'
CHANNEL_ID = 1295757053997879332  # Replace with your channel ID (must be an integer)
global last_post_title
last_post_title = ""
# Create a separate Chrome instance for each data source


def is_similar(a, b, threshold=0.70):
    """Check if two strings are similar by a given threshold."""
    return SequenceMatcher(None, a, b).ratio() > threshold

def is_similar_sportscard(a, b, threshold=0.90):
    """Check if two strings are similar by a given threshold."""
    return SequenceMatcher(None, a, b).ratio() > threshold

async def send_to_discord(message):
    """Send a message to the Discord channel."""
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(message)
        await client.close()

    await client.start(DISCORD_TOKEN)
    

# below finds hype flips
def hype_flips():
    link_cost = []
    link_counter = 0  # Counter for links
    max_links = 5  # Max number of links to open
    price_range = ""
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw=presale&_sacat=0&_sop=10")

    try:
        # Wait for the items with the class 's-item' to load
        # items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item")))
        
        ul_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul[class=\"srp-results srp-list clearfix\"]")))
        items = ul_element.find_elements(By.CSS_SELECTOR, "li[class*=\"s-item\"]")
        positive_values = []
        found_item = False

        for item in items:
            try:
                # Extract the title of the item
                title_element = item.find_element(By.CLASS_NAME, 's-item__title')
                title_text = (title_element.text.strip()).replace("NEW LISTING", "")

                if title_text:  # If the title is not blank
                    print(f"Title found: {title_text}")

                    # Check if title contains a date (MM:DD format)
                    date_match = re.search(r'(\d{1,2})/(\d{1,2})', title_text)
                    if date_match:
                        month, day = map(int, date_match.groups())
                        current_date = datetime.datetime.now()
                        try:
                            title_date = datetime.datetime(current_date.year, month, day)
                        except:
                            title_date = datetime.datetime(current_date.year, day, month)

                        # If the date in the title is not in the future, quit the driver
                        if title_date < current_date:
                            print(f"Date in title {title_text} is in the past: {title_date.strftime('%m:%d')}")
                            continue
                        else:
                            print(f"Future date found in title: {title_date.strftime('%m:%d')}")

                        # Extract the price of the item
                        price_element = item.find_element(By.CLASS_NAME, "s-item__price")
                        price_text = price_element.text.strip()

                        # Use regex to extract the first valid price number (ignoring ranges like "$10.00 to $20.00")
                        price_value = re.findall(r'\d+\.?\d*', price_text)  # Extracts numbers
                        if price_value:
                            positive_values.append(float(price_value[0]))  # Take the first price found

                        print(f"Price: {price_value[0]}")
                        

                        found_item = True
                        break  # Exit the loop once we find the first item with a valid title

            except StaleElementReferenceException:
                print("Element went stale, skipping this one.")
            except Exception as e:
                print(f"Error while extracting price or title: {e}")

        if not found_item:
            print("No item with a valid title found.")
            return

        # Calculate the average sell price (only one value in this case)
        if positive_values:
            average_sell_price = f"${statistics.mean(positive_values):.2f}"
        else:
            average_sell_price = "Unreliable Sales Data Found"

        print(f"Average_sell_price: {average_sell_price}")

        driver.switch_to.new_window('tab')
        sanitized_title_text = urllib.parse.quote_plus(title_text)
        search_ebay_flip = "https://www.ebay.com/sch/i.html?_nkw=" + sanitized_title_text + "&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
        driver.get(search_ebay_flip)


        # Wait for the eBay page to load and fetch elements with the class 's-item s-item__pl-on-bottom'
        # comparison_items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item.s-item__dsa-on-bottom.s-item__pl-on-bottom")))
        ul_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul[class=\"srp-results srp-list clearfix\"]")))
        comparison_items = ul_element.find_elements(By.CSS_SELECTOR, "li[class*=\"s-item\"]")
        print(len(comparison_items))

        positive_values = []

        for item in comparison_items:
            try:
                # Extract the title of the current item
                flip_element = item.find_element(By.CLASS_NAME, 's-item__title')
                flip_text = flip_element.text.strip()
                print(flip_text)


                # Check if the title contains a year (e.g., any four digits)
                contains_year = re.search(r'\b\d{4}\b', flip_text)

                # Check if the title contains a '#' sign
                contains_hash = '#' in flip_text

                # Call is_similar_sportscard if the title contains a year or contains a '#'
                if contains_year or contains_hash:
                    similar_check = is_similar_sportscard(flip_text.lower(), title_text.lower())
                else:
                    similar_check = is_similar(flip_text.lower(), title_text.lower())
                print("-----------")
                print(title_text)
                print(similar_check)

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

        print(f"POSTIVE_VALUES: {positive_values}")
        # Calculate the average sell price
        if positive_values:
            average_sold_price = f"${statistics.mean(positive_values):.2f}"  # Format the average to 2 decimal places
        else:
            average_sold_price = "$Unreliable Sales Data Found"


        print(f"Average sold price: {average_sold_price}")


        driver.switch_to.new_window('tab')
        driver.get("https://www.google.com/search?q=" + sanitized_title_text)
        unwanted_links = [
            "https://www.google.com",
            "https://www.ebay.com",
            "https://www.stockx.com",
            "https://www.instagram.com",
            "https://www.reddit.com",
            "https://www.tiktok.com"
            
        ]

        # Find all anchor tags and extract their href attributes
        hrefs = [element.get_attribute('href') for element in driver.find_elements(By.TAG_NAME, 'a')]
        possible_links_unfiltered = ""

        # Print the hrefs, excluding unwanted links
        for href in hrefs:
            # Check if href is not None and does not start with unwanted links
            if href is not None and not any(href.startswith(link) for link in unwanted_links):
                possible_links_unfiltered += " " + href
                print(href)

        print(possible_links_unfiltered)
        
        
        

    # Create the prompt
    # Use the chat completion endpoint
    except Exception as e:
        print("Error occurred: ", e)
    try:
        if average_sold_price != "$Unreliable Sales Data Found":
            prompt = (
                "Sort through the links. ONLY OUTPUT LINKS THAT COULD BE THE PRODUCT LINK MATCHING THE PRODUCT: "
                + title_text +
                " IF THERE ARE MULTIPLE LINKS YOU BELIEVE ARE POSSIBLE, YOU CAN INCLUDE MULTIPLE BUT ONLY OUTPUT LINKS, NO EXTRA WORDING: "
                + possible_links_unfiltered
            )
            client = OpenAI()

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response_message = completion.choices[0].message.content  # Use .content to get the message
            print("--------------------------------------")
            print(title_text)
            print(possible_links_unfiltered)
            print(response_message)
            # Splitting the content by " \n" and storing it in a list
            links_list = response_message.split(" \n")

            print("COMPLETED LIST:")
            print(links_list)

            

            for link in links_list:
                if link_counter < max_links:
                    # Open a new tab
                    driver.switch_to.new_window('tab')

                    # Visit the link
                    driver.get(link)
                    
                    # Allow some time for the page to load
                    sleep(2)

                    # Get the page source
                    page_source = driver.page_source

                    # Refined regex to focus on prices like $8.99 or similar (avoid $100.00 if possible)
                    price_matches = re.findall(r'\$\d{1,3}(?:,\d{3})?\.\d{2}', page_source)

                    # Pick a random price from the matches (if any are found)
                    if price_matches:
                        # Convert the matches to floats
                        prices_as_floats = [float(price.replace('$', '').replace(',', '')) for price in price_matches]
                        
                        # Select a random price from the available prices
                        random_price = random.choice(prices_as_floats)
                        link_cost.append(random_price)  # Store as float
                        print(f'Random price selected: ${random_price:.2f}')
                    else:
                        print('Price not found')

                    # Close the tab
                    driver.close()
                    
                    # Switch back to the original window (main tab)     
                    driver.switch_to.window(driver.window_handles[0])
                    
                    link_counter += 1

            # Calculate the price range if there are prices in the list
            if link_cost:
                min_price = min(link_cost)
                max_price = max(link_cost)
                price_range = f"Price range: ${min_price:.2f} - ${max_price:.2f}"
                print(price_range)
            else:
                price_range = "No prices found"
                print(price_range)

            # links_list = []

            message = (
                f" # 🤖{title_text}\n"
                f"🏷Possible Vinyl Cost: {price_range}\n"
                f"💸Average Sell Price: {average_sold_price}\n"
                f"🔗Possible Buy Links: {links_list}\n"
                f"✅️Ebay Comp: {search_ebay_flip}"
            )
            # Prepare the message to send

            print("Final message:", message)

            # Send the message to Discord
            asyncio.run(send_to_discord(message))
            print("called func again------")
       

        sleep(5000)
        driver.quit()

    except Exception as e:
        print("Error occurred: ", e)
        

    except Exception as e:
        print(f"Error: {e}")
        print("called func again")
        # driver.quit()

hype_flips()




















