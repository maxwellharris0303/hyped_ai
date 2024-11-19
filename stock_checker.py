import re
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

# Initialize the undetected Chrome driver
driver = uc.Chrome(version_main=130)
driver.maximize_window()
driver.get("https://www.warhammer.com/en-WW/shop/tau-empire-retaliation-cadre-2024?queryID=cbc34c8e69f72de08dedcc3ada1205c2&srsltid=AfmBOooDat22iM61Zb2rlyP_c0tVuaH5999wo6OOSGSMT2w2Z0Au2qqz")

def get_result(content):
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove <script> and <style> tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Define the regex pattern for full match
    pattern_out_stock = re.compile(r"^(out of stock|sold out|unavailable)$", re.IGNORECASE)
    pattern_in_stock = re.compile(r"^\s*\d*\s*(in stock|add to cart|pre-order|pre-order now|add to wishlist|available)$", re.IGNORECASE)

    out_stock_array = []
    in_stock_array = []
    # Iterate through all elements
    for element in soup.find_all(True):
        # Get the stripped text content of the element
        text = element.get_text(strip=True)
        if text and re.match(pattern_out_stock, text):
            out_stock_array.append(text.lower())
        if text and re.match(pattern_in_stock, text):
            in_stock_array.append(text.lower())
    
    out_stock_array = list(set(out_stock_array))
    in_stock_array = list(set(in_stock_array))
    print(f"Out of stock match found: {out_stock_array}")
    print(f"In stock match found: {in_stock_array}")

# Pass the page source to the function
get_result(driver.page_source)

# Close the driver
driver.quit()
