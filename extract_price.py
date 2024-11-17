import re
from bs4 import BeautifulSoup


def get_result(content):
    # Refined regex to focus on prices like $8.99 or similar (avoid $100.00 if possible)
    # price_matches = re.findall(r'[\$]\s?\d{1,3}(?:\s?[,.\s]\d{3})*(?:[.,]\d{2})?', content)

    # Parse the HTML
    soup = BeautifulSoup(content, 'html.parser')

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
    return price_list