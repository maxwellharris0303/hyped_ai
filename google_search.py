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
from bs4 import BeautifulSoup

# title_text = "Presale The Stanley X LoveShackFancy Holiday Quencher | 20 OZ - Rosa Beaux Pink"


def search(title_text):
    sanitized_title_text = urllib.parse.quote_plus(title_text)
    print(sanitized_title_text)
    options = uc.ChromeOptions()
    driver = uc.Chrome(version_main=130)
    driver.maximize_window()
    driver.get("https://www.google.com/search?q=" + sanitized_title_text)

    unwanted_links = [
        "google.com",
        "ebay.com",
        "stockx.com",
        "instagram.com",
        "facebook.com",
        "reddit.com",
        "tiktok.com"
        
    ]

    search_result = driver.find_element(By.CSS_SELECTOR, "div[id=\"search\"]")

    hrefs = [element.get_attribute('href') for element in search_result.find_elements(By.TAG_NAME, 'a') if element.get_attribute('href') and element.get_attribute('href').startswith("http")]

    possible_links_unfiltered = [link for link in hrefs if not any(unwanted in link for unwanted in unwanted_links)]

    possible_links_unfiltered = list(set(possible_links_unfiltered))

    print(possible_links_unfiltered)

    print(len(possible_links_unfiltered))

    # Convert array to a comma-separated string
    hrefs_string = ", ".join(possible_links_unfiltered)

    print(hrefs_string)

    prompt = (
        "Sort through the links. ONLY OUTPUT LINKS THAT COULD BE THE PRODUCT LINK MATCHING THE PRODUCT: "
        + title_text +
        " IF THERE ARE MULTIPLE LINKS YOU BELIEVE ARE POSSIBLE, YOU CAN INCLUDE MULTIPLE BUT ONLY OUTPUT LINKS, NO EXTRA WORDING: "
        + hrefs_string
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
    # Splitting the content by " \n" and storing it in a list
    links_list = [link.strip() for link in response_message.split("\n")]
    print("COMPLETED LIST:")
    print(links_list)

    result = {}

    for link in links_list:
        driver.get(link)

        # Get the page source
        page_source = driver.page_source
        # Refined regex to focus on prices like $8.99 or similar (avoid $100.00 if possible)
        price_matches = re.findall(r'[\$]\s?\d{1,3}(?:\s?[,.\s]\d{3})*(?:[.,]\d{2})?', page_source)
        # print(set(list(price_matches)))
        # print(price_matches)

        # Parse the HTML
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find elements where any attribute contains 'price'
        elements_with_price = soup.find_all(lambda tag: any('price' in str(value).lower() for value in tag.attrs.values()))

        price_pattern = re.compile(r'^[\$]\s?\d{1,3}(?:\s?[,.\s]\d{3})*(?:[.,]\d{2})?$')

        # Filter and print only the lines that match exactly the price format
        price_list = []
        for element in elements_with_price:
            text = element.text.strip()
            if price_pattern.fullmatch(text) and text != "$0.00" and text != "$ 0.00":
                price_list.append(text)

        price_list = list(set(price_list))
        print(price_list)
        if len(price_list) != 0:
            result[link] = price_list
    driver.quit()
    return result

# print(search("Presale The Stanley X LoveShackFancy Holiday Quencher | 20 OZ - Rosa Beaux Pink"))