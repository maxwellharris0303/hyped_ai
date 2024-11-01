import time
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
from gpt_api import ask
from gpt_api.cli import clear_screen
from openai import OpenAI
import os

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
        items = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item"))
        )

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
                        title_date = datetime.datetime(current_date.year, month, day)

                        # If the date in the title is not in the future, quit the driver
                        if title_date < current_date:
                            print(f"Date in title {title_text} is in the past: {title_date.strftime('%m:%d')}")
                            driver.quit()
                            return
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

        driver.switch_to.new_window('tab')
        sanitized_title_text = urllib.parse.quote_plus(title_text)
        search_ebay_flip = "https://www.ebay.com/sch/i.html?_nkw=" + sanitized_title_text + "&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
        driver.get(search_ebay_flip)

        # Wait for the eBay page to load and fetch elements with the class 's-item s-item__pl-on-bottom'
        comparison_items = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item"))
        )

        positive_values = []

        for item in comparison_items:
            try:
                # Extract the title of the current item
                flip_element = item.find_element(By.CLASS_NAME, 's-item__title')
                flip_text = flip_element.text.strip()

                # Check if the title contains a year (e.g., any four digits)
                contains_year = re.search(r'\b\d{4}\b', flip_text)

                # Check if the title contains a '#' sign
                contains_hash = '#' in flip_text

                # Call is_similar_sportscard if the title contains a year or contains a '#'
                if contains_year or contains_hash:
                    similar_check = is_similar_sportscard(flip_text, title_text)
                else:
                    similar_check = is_similar(flip_text, title_text)

                if similar_check:
                    # Find and process positive elements
                    green_elements = item.find_elements(By.CLASS_NAME, "POSITIVE")

                    # Only take every other positive element starting from the second one
                    for index, element in enumerate(green_elements):
                        if index % 2 == 0:
                            continue  # Skip the even ones
                        try:
                            # Extract value, remove $ sign and clean it
                            value = element.text.replace('$', '').strip()
                            positive_values.append(float(value))  # Convert to float for averaging
                        except StaleElementReferenceException:
                            print("Element went stale, skipping this one.")

            except Exception as e:
                print(f"Error processing item: {e}")


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
        if average_sold_price == "$Unreliable Sales Data Found":
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
                    time.sleep(2)

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
            f"🔗Possible Buy Links: {links_list}"
            f"✅️Ebay Comp: {search_ebay_flip}"
        )
        # Prepare the message to send

        print("Final message:", message)

        # Send the message to Discord
        asyncio.run(send_to_discord(message))
        print("called func again")

    except Exception as e:
        print("Error occurred: ", e)
        

    except Exception as e:
        print(f"Error: {e}")
        print("called func again")

hype_flips()




#----------------------------------------------------------------------------------------------------------------------------------------


# below is for finding vinyls specifically
def hype_vinyls():
    global last_post_title
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://www.reddit.com/r/VinylReleases/new/")
    time.sleep(5)
    try:
        # Locate the first post link on Reddit (you need to select the first or a specific post)
        post_links = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@slot, 'full-post-link')]"))
        )

        if len(post_links) > 0:
            # Click the first post link (use index 0 for the first post)
            driver.execute_script("arguments[0].click();", post_links[0])
        else:
            print("No post links found")
            return

        # Wait for the post title element to be present and get its text
        post_title_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@slot='title']"))  # Wait for the first title with the title attribute
        )
        post_title = post_title_element.text
        print("Post title:", post_title)
        try:
            # Try to locate the lightbox link first
            first_post_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@source='post_lightbox']//a[@href]"))
            )
            # If found, click the link
            first_post_link.click()
            buy_link = driver.current_url
            print("First post link href:", buy_link)

        except TimeoutException:
            # If the lightbox is not found, proceed with the alternative
            print("Lightbox not found. Trying alternative selector.")
            try:
                first_post_link = driver.find_element(By.CSS_SELECTOR, ".relative.pointer-events-auto.a.cursor-pointer.underline")
                buy_link = first_post_link.get_attribute('href')
                print("First post link href:", buy_link)
                driver.switch_to.new_window('tab')
                driver.get(buy_link)
            except NoSuchElementException:
                print("No alternative link found either.")

        # Wait for the page to load and look for any element containing a $ sign
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Wait for page load
        time.sleep(5)
        
        # Refine the XPath to search for common elements that may contain price tags like <span>, <div>, <p> etc.
        price_elements = driver.find_elements(By.XPATH, 
            "//span[contains(text(), '$')] | //p[contains(text(), '$')] | //div[contains(text(), '$')] | "
            "//li[contains(text(), '$')] | //strong[contains(text(), '$')] | "
            "//*[contains(@class, 'price')] | //*[@data-price] | "
            "//*[@aria-label and contains(., '$')] | "
            "//meta[@content[contains(., '$')]]"
        )

        # Extract the text from the price elements
        dollar_values = [re.findall(r'\$\d+\.?\d*', element.text) for element in price_elements if element.text.strip() != '']
        dollar_values = [float(value.replace('$', '')) for sublist in dollar_values for value in sublist]  # Flatten list and convert to float

        if dollar_values:
            if len(set(dollar_values)) == 1:
                dollar_value_cost = f"${dollar_values[0]:.2f}"
            else:
                min_value = min(dollar_values)
                max_value = max(dollar_values)
                dollar_value_cost = f"${min_value:.2f} - ${max_value:.2f}"  # Show range if multiple prices
        else:
            dollar_value_cost = "$Unable to scan for price"


        print("Dollar values:", dollar_values)

        # Proceed to eBay for further search based on post title
        driver.switch_to.new_window('tab')
        search_ebay_vinyl = "https://www.ebay.com/sch/i.html?_nkw=" + post_title.replace(' ', '+') + "&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
        driver.get(search_ebay_vinyl)

        # Wait for the eBay page to load and fetch elements with the class 's-item s-item__pl-on-bottom'
        items = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item"))
        )

        positive_values = []

        for item in items:
            try:
                # Extract the title of the current item
                title_element = item.find_element(By.CLASS_NAME, 's-item__title')
                title_text = title_element.text.strip()

                # Check similarity with post_title
                if is_similar(title_text, post_title):
                    # Find and process positive elements
                    positive_elements = item.find_elements(By.CLASS_NAME, "POSITIVE")

                    # Only take every other positive element starting from the second one
                    for index, element in enumerate(positive_elements):
                        if index % 2 == 0:
                            continue  # Skip the even ones
                        try:
                            # Extract value, remove $ sign and clean it
                            value = element.text.replace('$', '').strip()
                            positive_values.append(float(value))  # Convert to float for averaging
                        except StaleElementReferenceException:
                            print("Element went stale, skipping this one.")
                            
            except Exception as e:
                print(f"Error processing item: {e}")

        # Calculate the average sell price
        if positive_values:
            average_sell_price = f"${statistics.mean(positive_values):.2f}"  # Format the average to 2 decimal places
        else:
            average_sell_price = "$Unreliable Sales Data Found"

        # Prepare the message to send
        # Prepare the message to send
        first_two_words = ' '.join(post_title.split()[:2])
        print("First two words of the post title:", first_two_words)

        # Open Spotify and search for the first two words
        driver.switch_to.new_window('tab')
        driver.get("https://open.spotify.com")
        time.sleep(5)  # Let Spotify load completely

        # Locate the search bar on Spotify
        search_bar = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='search-input']"))
        )
        search_bar.send_keys(first_two_words)  # Type the first two words into the search bar
        search_bar.send_keys(u'\ue007')  # Press Enter to initiate the search

        time.sleep(5)  # Wait for the search results to load

        # Get the current URL after search
        current_url = driver.current_url
        print("Current Spotify URL:", current_url)

        # Parse the URL and edit the path to append '/artists' at the end
        parsed_url = urlparse(current_url)
        new_path = parsed_url.path.rstrip('/') + "/artists"  # Ensure there's no trailing slash and append '/artists'
        updated_url = urlunparse(parsed_url._replace(path=new_path))
        
        print("Updated URL with /artists:", updated_url)

        # Navigate to the updated URL
        driver.get(updated_url)

        time.sleep(5)  # Wait for the artists page to load

        # Locate the first card-image element and find the href that starts with /art
        card_image = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-encore-id="card"]'))
        )

        # Find the link inside the card image whose href starts with '/art'
        link = card_image.find_element(By.XPATH, ".//a[starts-with(@href, '/art')]")

        # Click the link
        driver.execute_script("arguments[0].click();", link)
        print("Clicked on the href inside the card-image that starts with '/art'.")
        
        message = (
            f" # 💿{post_title}\n"
            f"🏷Possible Vinyl Cost: {dollar_value_cost}\n"
            f"💸Average Sell Price: {average_sell_price}\n"
            f"🔗Buy Link: {buy_link}\n"
            f"✅️Ebay Comp: {search_ebay_vinyl}"
        )

        print("Final message:", message)

        # Send the message to Discord
        try:
            # Wait for the element that contains the monthly listeners text
            monthly_listeners_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'monthly listeners')]"))
            )

            # Extract the text
            monthly_listeners_text = monthly_listeners_element.text
            print("Monthly listeners text:", monthly_listeners_text)

            # Use regex to find the number before "monthly listeners"
            match = re.search(r'(\d[\d,]*)\s+monthly listeners', monthly_listeners_text)
            if match:
                listeners_count = match.group(1).replace(',', '')  # Remove commas for easier processing
                print(f"Monthly listeners: {listeners_count}")
                monthly_listeners = listeners_count
            else:
                print("No monthly listeners found")
                return None
        except Exception as e:
            print(f"Error while retrieving monthly listeners: {e}")
            return None
        print(last_post_title)
        if int(monthly_listeners) >= 300000 and last_post_title != post_title:
            asyncio.run(send_to_discord(message))
        last_post_title = post_title
        driver.quit()
        hype_vinyls()
        print("called func again")

    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        hype_vinyls()
        print("called func again")



















