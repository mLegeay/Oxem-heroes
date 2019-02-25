# Create your views here.

import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
from oxem_heroes.settings import settings

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

client.run('NTQ5NTk1MzQ0MzQ3MDcwNDY0.D1WKFQ.D4zlIorHPwjjNWeqd5CrywjHb7o')
