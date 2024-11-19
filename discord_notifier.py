from discordwebhook import Discord
from urllib.parse import urlparse
import re
import tldextract

def notify_to_discord_channel(title_text, image, average_sold_price, possible_buy_links, price_range, nearest_date, search_ebay_flip):
    discord = Discord(url="https://discordapp.com/api/webhooks/1302301351878852741/X-0BTXp8LsZn0_1W1lNkClyCvnKztHGvpZIwoknOE5_xm3VRXXxdqZEwv-wF2Dpzqxuu")
    title = f"🤖 {title_text}"

    core_domains = [f"{tldextract.extract(link).domain}.{tldextract.extract(link).suffix}" for link in possible_buy_links]

    # print(core_names)  # Output: ['amazon', 'bestbuy']

    # Format the core domains as clickable links
    formatted_links = "\n".join(
        [f"- [{domain}]({link})" for domain, link in zip(core_domains, possible_buy_links)]
    )

    fields = [
        {
            "name": "🏷 Possible Vinyl Cost",
            "value": price_range,
        },
        {
            "name": "💸 Average Sell Price",
            "value": str(average_sold_price),
        },
        {
            "name": "🔗 Possible Buy Links",
            "value": formatted_links if formatted_links else "No links available",
        },
        {
            "name": "✅️ Ebay Comp",
            "value": f"[Click Here]({str(search_ebay_flip)})",
        },
    ]

    # Conditionally add the "Drop Date" field if release_dates is not empty
    if nearest_date != "":
        fields.insert(2, {  # Insert after "💸 Average Sell Price"
            "name": "⏰ Drop Date",
            "value": nearest_date,
        })
    else:
        fields.insert(2, {  # Insert after "💸 Average Sell Price"
            "name": "⏰ Drop Date",
            "value": "In Stock Now"
        })

    discord.post(
        username="Hyped.AI",
        avatar_url="https://cdn.discordapp.com/attachments/1300808163167178762/1306824151125983242/Untitled_design.png?ex=673caf95&is=673b5e15&hm=3c0c523823b8af987dab66d441c715a0b66a3c2a4789b72f8f7315b53a25afe5&",
        embeds=[
            {
                "title": title,
                "thumbnail": {"url": image},
                "color": 15258703,
                "fields": fields,
                "image": {
                    "url": image
                },
            }
        ],
    )

