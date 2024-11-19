from discordwebhook import Discord

def notify_to_discord_channel(title_text, image, average_sold_price, possible_buy_links, price_range, release_dates, search_ebay_flip):
    discord = Discord(url="https://discordapp.com/api/webhooks/1302301351878852741/X-0BTXp8LsZn0_1W1lNkClyCvnKztHGvpZIwoknOE5_xm3VRXXxdqZEwv-wF2Dpzqxuu")
    title = f"🤖{title_text}"

    # Format possible_buy_links as a list of clickable links
    formatted_links = "\n".join([f"- [Link {i+1}]({link})" for i, link in enumerate(possible_buy_links)])

    fields = [
        {
            "name": "🏷Possible Vinyl Cost",
            "value": price_range,
        },
        {
            "name": "💸Average Sell Price",
            "value": str(average_sold_price),
        },
        {
            "name": "🔗Possible Buy Links",
            "value": formatted_links if formatted_links else "No links available",
        },
        {
            "name": "✅️Ebay Comp",
            "value": f"[Click Here]({str(search_ebay_flip)})",
        },
    ]

    # Conditionally add the "Drop Date" field if release_dates is not empty
    if release_dates:
        fields.insert(2, {  # Insert after "💸Average Sell Price" for better placement
            "name": "⏰ Drop Date",
            "value": f"{', '.join(release_dates)}",
        })

    discord.post(
        username="Hyped.AI",
        avatar_url="https://img.freepik.com/free-vector/basketball-ball-isolated_1284-42545.jpg?w=740&t=st=1699445903~exp=1699446503~hmac=577a11eee3da5efd7a8cd17b51a5896d837165708b389a27a6debb8da8564592",
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
