text = {'https://americanbrickstore.com/muunilinst-arc-trooper-minifigures-star-wars-the-clone-wars-clone-troopers-muunilinst-10/': ['$3.99'], 'https://americanbrickstore.com/phase-1-clone-trooper-minifigures-star-wars-captain-rex-commander-cody-commander-wolffe-muunilinst-arc-trooper/': ['$6.99', '$3.99'], 'https://americanbrickstore.com/captain-fordo-arc-trooper-minifigure-star-wars-the-clone-wars-clone-trooper-muunilinst-10/': ['$3.99']}

# Loop through the dictionary and print each URL with its prices
for url, prices in text.items():
    print(f"URL: {url}")
    print(f"Price: {prices}")

print(len(text))