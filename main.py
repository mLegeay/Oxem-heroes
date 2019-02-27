# Create your views here.

import discord
import asyncio

from discord.ext.commands import Bot
from discord.ext import commands
from django.conf import settings

from oxemHeroes.bot.models import Member, Game

client = commands.Bot(command_prefix="?")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(settings.TOKEN)


@client.event
async def on_message(message):
    print(Game.objects.from_message(message))
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run(settings.TOKEN)
