import os

import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} has connected to Discord!')
    print(f'{guild.name}(id: {guild.id})')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'''Hallo {member.name}, Willkommen bei den
                                 Papierkriegern!''')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.channel)
    response = "Just a Test"

    if message.content == "!test":
        await message.channel.send(response)

client.run(TOKEN)
