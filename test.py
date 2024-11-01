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

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()
driver.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw=presale&_sacat=0&_sop=10")

items = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item"))
        )
for item in items:
    title_element = item.find_element(By.CLASS_NAME, 's-item__title')
    title_text = (title_element.text.strip()).replace("NEW LISTING", "")
    date_match = re.search(r'(\d{1,2})/(\d{1,2})', title_text)
    if date_match != None:
        month, day = map(int, date_match.groups())
        try:
            current_date = datetime.datetime.now()
            title_date = datetime.datetime(current_date.year, month, day)
        except:
            pass
        # print(f"Future date found in title: {title_date.strftime('%m:%d')}")

        price_element = item.find_element(By.CLASS_NAME, "s-item__price")
        price_text = price_element.text.strip()
            

        # Use regex to extract the first valid price number (ignoring ranges like "$10.00 to $20.00")
        price_value = re.findall(r'\d+\.?\d*', price_text)  # Extracts numbers
        # if price_value:
        #     positive_values.append(float(price_value[0]))  # Take the first price found

        # print(f"Price: {price_value[0]}")

        driver.switch_to.new_window('tab')
        sanitized_title_text = urllib.parse.quote_plus(title_text)
        search_ebay_flip = "https://www.ebay.com/sch/i.html?_nkw=" + sanitized_title_text + "&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
        driver.get(search_ebay_flip)
        break

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
            date_match = re.search(r'(\d{1,2}):(\d{1,2})', title_text)
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