# Create your views here.

import discord
import asyncio

from discord.ext.commands import Bot
from discord.ext import commands
from django.conf import settings

from oxemHeroes.command.models import Command
from oxemHeroes.gameMember.models import GameMember
from oxemHeroes.classe.commands import Commands as c_classe
from oxemHeroes.gameMember.commands import Commands as c_gameMember

from oxemHeroes.bot.constants import COMMAND_LIST, PLAYER_COMMAND, SKILL_LIST

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

    if not message.content.startswith('%'):
        return

    command = message.content[1:].split(' ')[0]
    parameters = message.content[1:].split(' ')
    parameters.pop(0)

    command = None if len(command) == 0 else command

    if command is not None:
        content, files = execute(message, command, parameters)
        await message.channel.send(content=content, files=files)


def execute(send_message, command_name, parameters):

    files = None

    if command_name in COMMAND_LIST:
        command = Command.objects.from_name(command_name)
        gameMember = GameMember.objects.from_message(send_message)

        if command_name in PLAYER_COMMAND or command_name in SKILL_LIST:
            if command.name == "choisir":
                instance_gameMember = c_gameMember()
                files, message = instance_gameMember.process(command, gameMember, send_message, parameters)

            elif gameMember is None:
                message = ERRORS['not_a_player']

            elif command_name in SKILL_LIST:
                instance_classe = c_classe(gameMember)
                message = instance_classe.process(command_name, send_message)

        elif send_message.author.guild_permissions.administrator and command_name in ADMIN_COMMAND_LIST:

            if command_name == "giveaway":
                Giveaway.objects.all().delete()
                Giveaway.objects.create(participants={'participants': []})
                message = "Giveaway créé avec succès"

        elif command_name == "participer":
            message = Giveaway.objects.participer(send_message)

        else:
            message = ERRORS['non_authorized']

    elif command_name in HELP_COMMAND:

        if parameters:
            command = Command.objects._get_command(parameters[0])

            if command is not None:
                message = "`{}`".format(command.how_to)
            else:
                message = ERRORS['command_dne']
        else:
            message = HELP_MESSAGE['start']

            for each in PLAYER_COMMAND:
                command = Command.objects._get_command(each)
                message += "- {}: {}\n".format(command.name, command.description)

            message += HELP_MESSAGE['classe']

            for each in SKILL_LIST:
                command = Command.objects._get_command(each)
                message += "- {}: {}\n".format(command.name, command.description)

            message += HELP_MESSAGE['end']

    else:
        message = ERRORS['command_dne']

    return message, files


client.run(settings.TOKEN)
