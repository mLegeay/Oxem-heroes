# Create your views here.

import asyncio

from django.conf import settings
from django.utils import timezone

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from oxemHeroes.constants import (ADMIN_COMMAND_LIST, COMMAND_LIST, ERRORS,
                                  HELP_COMMAND, PLAYER_COMMAND, SKILL_LIST)
from oxemHeroes.classe.commands import Commands as c_classe
from oxemHeroes.command.commands import Commands as c_command
from oxemHeroes.command.models import Command
from oxemHeroes.commandHistory.models import CommandHistory
from oxemHeroes.game.models import Game
from oxemHeroes.gameMember.commands import Commands as c_gameMember
from oxemHeroes.gameMember.models import GameMember
from oxemHeroes.giveAway.commands import Commands as c_giveAway

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

    bonus_xp = CommandHistory.objects.filter(command=Command.objects.from_name("potion"))

    if bonus_xp is not None:
        if (timezone.now() - bonus_xp.latest("last_used").last_used).total_seconds()//60 > 45 and Game.objects.get_bonusxp() == 30:
            Game.objects.alter_xp(0)

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

            else:
                instance_gameMember = c_gameMember()
                files, message = instance_gameMember.process(command, gameMember, send_message, parameters)

        elif send_message.author.guild_permissions.administrator and command_name in ADMIN_COMMAND_LIST:
            instance_command = c_command()
            message = instance_command.admin_command(command, send_message, parameters)

        elif command_name == "participer":
            instance_command = c_giveAway()
            message = instance_command.process(command, send_message)

        else:
            message = ERRORS['non_authorized']

    elif command_name in HELP_COMMAND:
        instance_command = c_command()
        message = instance_command.help_command(parameters)

    else:
        message = ERRORS['command_dne']

    return message, files


client.run(settings.TOKEN)
