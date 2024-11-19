import re

def clean_title(title):
    # Remove "presale" or similar terms (case-insensitive)
    title = re.sub(r'\b(confirmed presale|presale confirmed|confirmed pre-sale|pre-sale confirmed|presale|pre-order|preorder|pre-sale|order)\b', '', title, flags=re.IGNORECASE)
    
    # Remove emojis (any character that isn't a basic letter, number, punctuation, or whitespace)
    title = re.sub(r'[^\w\s,.\'-]', '', title)

    # Remove extra spaces from the string
    title = re.sub(r'\s+', ' ', title).strip()

    return title

# Example usage
titles = [
    'CALENDAR BOX Pre-Sale Pre-Order!!!',
    'Bunny Big Plush Authentic Official PRESALE CONFIRMED ORDER',
    'CALENDAR BOX PREORDER PRESALE',
    '【Pre-sale】CT Toys Mafex No.186 Scarlet Spider-',
    'Cossack Colonel 1:32 Painted Toy Soldier Pre-Sale | Collectible Level',
    'Frieza 2nd form DB Studio Resin Dragon Ball Figurine Statue 1/6 Presale',
    'UNCANNY X-MEN #3 GRANOV SAVAGE ROGUE NYCC SET T RADE & VIRIGN VARIANTS PRESALE',
    'Cossack Colonel 1:32 Painted Toy Soldier Pre-Sale | Art Level',
    'Paul Skenes - 2024 MLB Topps NOW OS-2 ROOKIE OF THE YEAR ROY - PRESALE Limited!',
    'Kith x Batman The Noble Collection Batpod | PRESALE ✅',
    'CONFIRMED PRE-SALE Kith x Batman The Noble Collection Batpod | PRESALE ✅',
    # Add more titles as needed
]

cleaned_titles = [clean_title(title) for title in titles]

for title in cleaned_titles:
    print(title)
