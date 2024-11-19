import re
from bs4 import BeautifulSoup
# import undetected_chromedriver as uc

# url = "https://creations.mattel.com/products/rlc-porsche-959-hwf18?srsltid=AfmBOorZpC7tXgQGJpCC54B9-RmqE4eFtpQQgn9jFPx5e4ZNxOYT02a7"

# driver = uc.Chrome(version_main=130)
# driver.maximize_window()
# driver.get(url)
# URL of the product page

def get_result(content):
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Extract all text content from the HTML
    text_content = soup.get_text()

    # Define regex patterns for various date formats
    date_patterns = [
        r"\d{4}-\d{2}-\d{2}",         # Matches YYYY-MM-DD
        r"\d{2}/\d{2}/\d{4}",         # Matches MM/DD/YYYY
        r"[A-Za-z]+\s\d{1,2},\s\d{4}", # Matches Month DD, YYYY
        r"\d{1,2}\s[A-Za-z]+\s\d{4}",  # Matches DD Month YYYY
    ]

    # Combine all patterns into one
    combined_pattern = "|".join(date_patterns)

    # Find all matches
    dates = re.findall(combined_pattern, text_content)

    # Remove duplicates and sort
    unique_dates = sorted(set(dates))

    # # Print the results
    # for date in unique_dates:
    #     print(date)
    
    return unique_dates
