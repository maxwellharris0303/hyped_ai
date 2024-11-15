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

title_text = "PRESALE - PlayStation 5 Dual Sense 30th Anniversary Controller PRESALE! ✅"
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