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
EMOJI: dict = {"Spielleiter": '🖊️', 'Spieler': '📜'}
ROLE_DICT: dict = {}
REACT_MSG_ID: int

bot = commands.Bot(command_prefix="!")
rest = Rest()


@bot.event
async def on_ready():
    guild: discord.Guild = discord.utils.get(bot.guilds, id=int(GUILD))
    await getChHistory(discord.utils.get(guild.channels, id=int(WORK_CH_ID)))
    await checkRoleCh(discord.utils.get(guild.channels, id=int(ROLE_CH_ID)))
    global ROLE_DICT
    for role in guild.roles:
        ROLE_DICT[role.name] = role
    log.info(f'{bot.user.name} has connected to Discord!')
    print("Ready")


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if msg.channel.id == int(WORK_CH_ID):
        await wrapMsgCheck(msg)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.message_id != REACT_MSG_ID:
        return
    if payload.member.bot:
        return
    for role, emoji in EMOJI.items():
        if (payload.emoji.name != emoji):
            continue
        await payload.member.add_roles(ROLE_DICT[role])


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if payload.message_id != REACT_MSG_ID:
        return
    for role, emoji in EMOJI.items():
        if payload.emoji.name != emoji:
            continue
        guild: discord.Guild = discord.utils.get(
            bot.guilds, id=int(payload.guild_id))
        member = await guild.fetch_member(payload.user_id)
        await member.remove_roles(ROLE_DICT[role])


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
    global REACT_MSG_ID
    react: list = ["Spielleiter", "Spieler"]
    check_msg: str = f"""Rollen Auswahl
Reagiere mit diesem Emote um dir selbst die Rolle zu geben

{EMOJI[react[0]]}  : Spielleiter

{EMOJI[react[1]]}  : Rollenspieler"""
    check: bool = False
    messages = await channel.history(limit=200).flatten()
    for message in messages:
        if message.author != bot.user:
            continue
        if hash(message.content) != hash(check_msg):
            check = True
        else:
            REACT_MSG_ID = message.id
    if check or len(messages) == 0:
        message = await channel.send(check_msg)
        REACT_MSG_ID = message.id
        for r in EMOJI.values():
            await message.add_reaction(r)
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
