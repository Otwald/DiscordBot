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
        await wrapMsgCheck(message)


@bot.event
async def on_ready():
    # print(bot.guilds)
    guild: discord.Guild = discord.utils.get(bot.guilds, id=int(GUILD))
    await getChHistory(discord.utils.get(guild.channels, id=int(WORK_CH_ID)))
    # print(guild.channels)
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if msg.channel.id == int(WORK_CH_ID):
        await wrapMsgCheck(msg)


async def wrapMsgCheck(message: discord.Message):
    """
    checks if msg is not from a bot, and if msg was already send to website
    if not send it and adds reaction to the msg
    """
    if message.author.bot:
        return
    if checkMsgReact(message.reactions):
        if rest.makeRequest(msg=message.content):
            await message.add_reaction('✅')
        else:
            await message.add_reaction('❌')


def checkMsgReact(reacts: list) -> bool:
    """
    checks list of reactions on a message to see if one is from the bot
    """
    for react in reacts:
        if react.me:
            return False
    return True


bot.run(TOKEN)
