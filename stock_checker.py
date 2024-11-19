import re
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

# Initialize the undetected Chrome driver
driver = uc.Chrome(version_main=130)
driver.maximize_window()
driver.get("https://yesgk.com/products/dragon-ball-standing-frieza-second-form-resin-statue-break-studio-pre-order")

def get_result(content):
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove <script> and <style> tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Define the regex pattern for full match
    pattern = re.compile(r"^(out of stock|sold out|unavailable)$", re.IGNORECASE)

    # Iterate through all elements
    for element in soup.find_all(True):
        # Get the stripped text content of the element
        text = element.get_text(strip=True)
        if text and re.match(pattern, text):
            print(f"Exact match found: {text}")

# Pass the page source to the function
get_result(driver.page_source)

# Close the driver
driver.quit()
