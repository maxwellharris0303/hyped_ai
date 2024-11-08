import discord
from discord.ext import commands
import asyncio

# Create a bot instance
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)
CHANNEL_ID = 1295757053997879332

# Event: Bot is ready and connected to the server
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        while True:
            await channel.send('Hello, World!')
            await asyncio.sleep(10)  # Wait for 10 seconds

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself to prevent recursion
    if message.author == bot.user:
        return

    # Send greeting message
    await message.channel.send(f'Hello {message.author.name}!')

    # Process commands
    await bot.process_commands(message)

# Command: !hello
@bot.command()
async def hello1(ctx):
    await ctx.send('Hello, I am your friendly Discord bot!')
    
async def send_message_every_5_seconds():
    await bot.wait_until_ready()  # Wait until the bot is ready
    while not bot.is_closed():
        channel = bot.get_channel(1130361535391334422)  # Replace YOUR_CHANNEL_ID with the ID of the channel you want to send messages to
        await channel.send("This is a message sent every 5 seconds.")
        await asyncio.sleep(5)
# Run the bot
bot.run('MTMwMDkxMTc2MTU0ODkwNjUxNg.GslcYm.kUi-YZ-WvZeHch8pL6KcR7fM4JAcPjTAyZO6iA')

# Run the send_message_every_5_seconds() function as a separate task
bot.loop.create_task(send_message_every_5_seconds())