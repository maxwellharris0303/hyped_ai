import re
from bs4 import BeautifulSoup
# import undetected_chromedriver as uc

# driver = uc.Chrome(version_main=130)
# driver.maximize_window()
# driver.get("https://hypebeast.com/2024/8/travis-scott-nike-zoom-field-jaxx-light-chocolate-info")

def get_result(content):
    # Refined regex to focus on prices like $8.99 or similar (avoid $100.00 if possible)
    # price_matches = re.findall(r'[\$]\s?\d{1,3}(?:\s?[,.\s]\d{3})*(?:[.,]\d{2})?', content)

    # Parse the HTML
    soup = BeautifulSoup(content, 'html.parser')

    # Find elements where any attribute contains 'price'
    elements_with_price = soup.find_all(lambda tag: any('price' in str(value).lower() for value in tag.attrs.values()))
    print(len(elements_with_price))

    # price_pattern = re.compile(r'^[\$]\s?\d{1,3}(?:\s?[,.\s]\d{3})*(?:[.,]\d{2})?$')
    price_pattern = re.compile(r'^(USD|usd)?\s?[\$]\s?\d{1,3}(?:\s?[,.\s]\d{3})*(?:[.,]\d{2})?\s?(USD|usd)?$')

    # Filter and print only the lines that match exactly the price format
    price_list = []
    for element in elements_with_price:
        text = element.text.strip()
        if price_pattern.fullmatch(text) and text != "$0.00" and text != "$ 0.00":
            price_list.append(text)

    price_list = list(set(price_list))
    return price_list
# print(get_result(driver.page_source))