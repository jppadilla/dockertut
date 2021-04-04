import os
import discord
import asyncio
import anime_scraper as scraper

from random import sample
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
# Token should be in int else it wouldnt work
GUILD = int(os.getenv('GUILD_TOKEN'))
CHANNEL = int(os.getenv('CHANNEL_TOKEN'))

anime_thumbnail = "https://gogoanime.ai/img/icon/logo.png"

quotes = ["Yeah, I ate a big red candle.", 
    "I would like to extend to you an invitation to the pants party.",
    "I don't have any legs, Ron.",
    "I DON'T KNOW WHAT WE'RE YELLING ABOUT!",
    "LOUD NOISES!!",
    "I love carpet. I love lamp.",
    "Yeah, I stabbed a man in the heart.",
    "I'm Brick, I was dead last week."]

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!', flush=True)
    guild = client.get_guild(GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    client.loop.create_task(my_background_task()) 

@client.event
async def on_message(message):
    # Makes sure it wouldnt respond to it's own message
    if message.author == client.user:
        return

    channel = client.get_channel(CHANNEL)
    if channel == message.channel:
        if message.content.startswith('!addanime'):
            await channel.send("Geez another job! Ok wait..")
            await add_command(message.content, channel)
        if message.content.startswith('!watchlist'):
            await send_watchlist(channel)
        if message.content.startswith('!brick'):
            await channel.send(get_brick_quote())

    
# Background Task looping to send embed message to channel
async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL)
    while not client.is_closed():
        print(dt.now(), " Brick is checking list....", flush=True)
        updated_list = scraper.call_scraper()
        if updated_list:
            print(dt.now(), " Brick is Sending....", flush=True)
            embed = discord.Embed(title="Anime Updates!", description="from: GoGoAnime", url=scraper.URL)
            embed.set_thumbnail(url=anime_thumbnail)
            message = create_embed_message(updated_list)
            quote = get_brick_quote()
            embed.add_field(name="New Episodes:", value=message, inline=False)
            embed.add_field(name=quote, value="@everyone", inline=False)
            await channel.send(embed=embed)
            print(dt.now(), " Message Sent!", flush=True)
        else :
            print(dt.now(), "Brick is not dead and there's no new updates.", flush=True)
        await asyncio.sleep(300)

# Creates the message for the New Episodes Field return string
def create_embed_message(updated_list):
    anime_links = scraper.create_links(updated_list)
    message = ""
    for anime in updated_list:
        message += f"[{anime} Episode {updated_list[anime]}]({anime_links[anime]})\n"
    print("Brick is updating:\n", message, flush=True)
    return message

# Randomize Brick quotes returns string
def get_brick_quote():
    return sample(quotes, 1)[0]

async def add_command(content, channel):
    if(scraper.link_checker(content)):
        print(dt.now(), "Brick is adding the new anime", flush=True)
        anime_list = scraper.add_anime(content)
        message = ""
        for anime in anime_list:
            message += f"[{anime}]({anime_list[anime]})\n"
        quote = get_brick_quote()
        embed = discord.Embed(title="Added Anime to Watchlist.", url=scraper.URL)
        embed.set_thumbnail(url=anime_thumbnail)
        embed.add_field(name="Watch now!", value=message, inline=False)   
        embed.add_field(name=quote, value="Balle is da beast!", inline=False)    
        await channel.send(embed=embed)
    else:
        await channel.send('Uh oh.. u sux wrong link.')


async def send_watchlist(channel):
    print(dt.now(), "Brick is sending anime watch list..", flush=True)
    anime_links = scraper.get_watchlist()
    guild = client.get_guild(GUILD)
    message = ""
    quote = get_brick_quote()
    for anime in anime_links:
        message += f"[{anime}]({anime_links[anime]})\n"
    embed = discord.Embed(title="Anime watchlist.", description=guild.name, url=scraper.URL)
    embed.set_thumbnail(url=anime_thumbnail)
    embed.add_field(name="Links:", value=message, inline=False)   
    embed.add_field(name=quote, value="- Brick", inline=False)
    await channel.send(embed=embed)

client.run(TOKEN)

