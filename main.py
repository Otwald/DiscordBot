import os
import discord
import logging as log

from rest import Rest
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
log.basicConfig(filename='example.log', level=log.INFO,
                format='%(asctime)s - %(levelname)s -  %(message)s')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')
WORK_CH_ID = os.getenv('WORK_CH_ID')
ROLE_CH_ID = os.getenv('ROLE_CH_ID')

bot = commands.Bot(command_prefix="!")
rest = Rest()


@bot.event
async def on_ready():
    guild: discord.Guild = discord.utils.get(bot.guilds, id=int(GUILD))
    await getChHistory(discord.utils.get(guild.channels, id=int(WORK_CH_ID)))
    await checkRoleCh(discord.utils.get(guild.channels, id=int(ROLE_CH_ID)))
    log.info(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if msg.channel.id == int(WORK_CH_ID):
        await wrapMsgCheck(msg)


@bot.event
async def on_reaction_add(reaction: discord.reaction, user: discord.User):
    print(reaction)
    print(discord.User)


async def getChHistory(channel: discord.TextChannel) -> None:
    """
    gets rundenvorestellungs history to hand them to the wrapper
    """
    message: discord.Message
    async for message in channel.history(limit=200):
        await wrapMsgCheck(message)


async def checkRoleCh(channel: discord.TextChannel) -> None:
    """
    checks or posts message for the role menu channel
    """
    message: discord.Message
    check_msg: str = """
Rollen Auswahl
Reagiere mit diesem Emote um dir selbst die Rolle zu geben

:pen_ballpoint:  : Spielleiter

:scroll:  : Rollenspieler"""
    check: bool = False
    messages = await channel.history(limit=200).flatten()
    print(check_msg)
    if len(messages) == 0:
        await channel.send(check_msg)
        return
    for message in messages:
        if message.author != bot.user:
            continue
        if message.content != check_msg:
            check = True
    if check:
        await channel.send(check_msg)
        log.info("Added Role Channels Default Msg")


async def wrapMsgCheck(message: discord.Message) -> None:
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
