import os
import discord

from rest import Rest
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')
WORK_CH_ID = os.getenv('WORK_CH_ID')

bot = commands.Bot(command_prefix="!")
rest = Rest()


async def getChHistory(channel: discord.TextChannel):
    message: discord.Message
    async for message in channel.history(limit=200):
        if not message.author.bot:
            print(message)
            rest.makeRequest()


@bot.event
async def on_ready():
    # print(bot.guilds)
    guild: discord.Guild = discord.utils.get(bot.guilds, id=int(GUILD))
    await getChHistory(discord.utils.get(guild.channels, id=int(WORK_CH_ID)))
    # print(guild.channels)
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(msg):
    print(msg.channel.id)
    if msg.author == bot.user:
        return

    print(type(msg.channel.id))
    if msg.channel.id == 757688430132985967:
        await msg.channel.send("nerv nicht")

bot.run(TOKEN)
