from discordwebhook import Discord

def notify_to_discord_channel(first_team_name, second_team_name, different_value, current_url, game_time, pre_game_total, current_total, difference_calibrated):
    discord = Discord(url="https://discordapp.com/api/webhooks/1302301351878852741/X-0BTXp8LsZn0_1W1lNkClyCvnKztHGvpZIwoknOE5_xm3VRXXxdqZEwv-wF2Dpzqxuu")
    title = f"🤖Bratz x Mean Girls Collector Dolls - Karen & Gretchen 2-Pack presale 11/8 eta"
    message = f":face_with_open_eyes_and_hand_over_mouth:  It is [**{str(different_value)}**]({current_url}) different from the pre game total 👀"
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
                "description": message,
                "thumbnail": {"url": "https://img.freepik.com/free-vector/gradient-basketball-logo-template_23-2149373179.jpg?w=740&t=st=1699446730~exp=1699447330~hmac=beaa2f964db5c9ba2f4805f248e5bc42949e5b9c896b89f78de3b6a5d4a2d8dd"},
                "color": 15258703,
                "url": current_url,
                "fields": [
                    {
                        "name": "🏷Possible Vinyl Cost",
                        "value": "Price range: $50.00 - $100.00",
                        # "inline": True
                    },
                    {
                        "name": "💸Average Sell Price",
                        "value": str("pre_game_total"),
                        # "inline": True
                    },
                    {
                        "name": "🔗Possible Buy Links",
                        "value": "[Click Here](https://img.freepik.com/free-vector/gradient-basketball-logo-template_23-2149373179.jpg)",
                        # "inline": True
                    },
                    {
                        "name": "✅️Ebay Comp",
                        "value": str(difference_calibrated),
                        # "inline": True
                    },
                ],
                "image": {
                    "url": "https://i.ebayimg.com/images/g/ws0AAOSwCC9nKt7d/s-l1600.webp"
                },
                # "footer": {
                #     "text": "NBA",
                #     "icon_url": "https://api.sofascore.app/api/v1/unique-tournament/132/image"
                # }
            }
        ],
    )

notify_to_discord_channel("CCC", "BBB", "8", "https://img.freepik.com/", "2023-11-09 02:30", 237.5, 240.5, 5)