# Create your views here.

import discord
import asyncio

from discord.ext.commands import Bot
from discord.ext import commands
from django.conf import settings

from oxemHeroes.bot.models import Member, Game, Command

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)


@client.event
async def on_message(message):

    if(message.author.bot):
        return

    if not message.content.startswith('!'):
        return

    command = message.content[1:].split(' ')[0]
    parameters = message.content[1:].split(' ')
    parameters.pop(0)

    command = None if len(command) == 0 else command

    if command is not None:
        content, files = Command.objects.execute(message, command, parameters)
        await message.channel.send(content=content, files=files)


client.run(settings.TOKEN)
