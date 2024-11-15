from discordwebhook import Discord

def notify_to_discord_channel(title_text, image, average_sold_price, possible_buy_links, price_range, search_ebay_flip):


    discord = Discord(url="https://discordapp.com/api/webhooks/1302301351878852741/X-0BTXp8LsZn0_1W1lNkClyCvnKztHGvpZIwoknOE5_xm3VRXXxdqZEwv-wF2Dpzqxuu")
    title = f"🤖{title_text}"
    # message = f":face_with_open_eyes_and_hand_over_mouth:  It is [**{str(different_value)}**]({current_url}) different from the pre game total 👀"
    # discord.post(content=message)
    discord.post(
        username="Hyped.AI",
        avatar_url="https://img.freepik.com/free-vector/basketball-ball-isolated_1284-42545.jpg?w=740&t=st=1699445903~exp=1699446503~hmac=577a11eee3da5efd7a8cd17b51a5896d837165708b389a27a6debb8da8564592",
        # content=title,
        embeds=[
            {
                # "author": {
                #     "name": "Contact us ☎️ ",
                #     "url": "https://www.watcher.com",
                #     "icon_url": ""
                # },
                "title": title,
                # "description": message,
                "thumbnail": {"url": image},
                "color": 15258703,
                # "url": current_url,
                "fields": [
                    {
                        "name": "🏷Possible Vinyl Cost",
                        "value": price_range,
                        # "inline": True
                    },
                    {
                        "name": "💸Average Sell Price",
                        "value": str(average_sold_price),
                        # "inline": True
                    },
                    {
                        "name": "🔗Possible Buy Links",
                        # "value": "[Click Here](https://img.freepik.com/free-vector/gradient-basketball-logo-template_23-2149373179.jpg)",
                        "value": f"{', '.join(possible_buy_links)}",
                        # "inline": True
                    },
                    {
                        "name": "✅️Ebay Comp",
                        "value": f"[Click Here]({str(search_ebay_flip)})",
                        # "inline": True
                    },
                ],
                "image": {
                    "url": image
                },
                # "footer": {
                #     "text": "NBA",
                #     "icon_url": "https://api.sofascore.app/api/v1/unique-tournament/132/image"
                # }
            }
        ],
    )

# notify_to_discord_channel("CCC", "BBB", "8", "https://img.freepik.com/", "2023-11-09 02:30", 237.5, 240.5, 5)