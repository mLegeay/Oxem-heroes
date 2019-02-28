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
    print(Game.objects.from_message(message))
    if(message.author.bot) return

    if not message.content.startswith('!') return

    command = message.content[1:].split(' ')[0]
    parameters = message.content[1:].split(' ')
    parameters.pop(0)

    if command is not None:
        Command.objects.execute(message, command, parameters)


client.run(settings.TOKEN)
