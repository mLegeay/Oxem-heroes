"""Commande pour les command.

- help/aide : liste les commandes et comment les utiliser
- addjeton : ajoute des jetons à un utilisateur donnée
- add silver : ajoute des silvers à un utilisateur donnée
- bonusxp : modifier le bonus d'xp sur l'expérience gagnée
- giveaway : créer un giveaway
"""

import discord
from oxemHeroes.command.constants import (ADMIN_DONE, ERRORS, GIVEAWAY,
                                          HELP_MESSAGE, PLAYER_COMMAND,
                                          SKILL_LIST)
from oxemHeroes.command.models import Command
from oxemHeroes.game.models import Game
from oxemHeroes.gameMember.models import GameMember
from oxemHeroes.giveAway.models import Giveaway


class Commands(object):
    """Traite les commandes reçus pour les classes."""

    def __init__(self):
        """Initialise les valeurs de la classe."""

    def help_command(self, parameters):
        """variables :
           - Command command : commande pour laquelle de l'aide est recherché
           - String message : message à renvoyer à l'utilisateur

           parameters:
           - [parameters] liste des paramètres qui suivent la commande

           return:
           - String message : message à renvoyer à l'utilisateur
        """

        if parameters:
            command = Command.objects.from_name(parameters[0])

            if command is not None:
                message = "`{}`".format(command.how_to)
            else:
                message = ERRORS['command_dne']
        else:
            message = HELP_MESSAGE['start']

            for each in PLAYER_COMMAND:
                command = Command.objects.from_name(each)
                message += "- {}: {}\n".format(command.name, command.description)

            message += HELP_MESSAGE['classe']

            for each in SKILL_LIST:
                command = Command.objects.from_name(each)
                message += "- {}: {}\n".format(command.name, command.description)

            message += HELP_MESSAGE['end']

        return message

    def admin_command(self, command, _message, parameters):
        """variables :
           - String message : message à renvoyer à l'utilisateur

           parameters:
           - Command command : commande executé par l'utilisateur
           - String _message : message de l'utilisateur contenant la commande
           - [parameters] : paramètres ajouté à la suite de la commande

           return:
           - String message : message à renvoyer à l'utilisateur
        """

        if command.name == "bonusxp":
            message = self.bonusxp(command, parameters)

        elif command.name == "addsilver":
            message = self.addsilver(_message, parameters)

        elif command.name == "addjeton":
            message = self.addjeton(_message, parameters)

        elif command.name == "giveaway":
            message = self.giveAway()

        return message

    def bonusxp(self, command, parameters):
        """Modifie le multiplicateur d'expérience."""

        if parameters:
            message = Game.objects.alter_xp(parameters[0])
        else:
            message = command.how_to

        return message

    def addsilver(self, _message, parameters):
        """Ajoute des silvers pour un utilisateur donnée."""

        if len(parameters) == 2 and _message.mentions:
            gameMember = GameMember.objects.from_discord(_message.mentions[0])

            if gameMember is not None:
                silver = gameMember.add_silver(int(parameters[0]))
                message = ADMIN_DONE['add_silver'].format(silver, gameMember.member.name)

            else:
                message = ERRORS['player_dne']
        else:
            message = command.how_to

        return message

    def addjeton(self, _message, parameters):
        """Ajoute des jetons pour un utilisateur donnée."""

        if len(parameters) == 2 and _message.mentions:
            gameMember = GameMember.objects.from_discord(_message.mentions[0])

            if gameMember is not None:
                token = gameMember.add_token(int(parameters[0]))
                message = ADMIN_DONE['add_token'].format(token, gameMember.member.name)
            else:
                message = ERRORS['player_dne']
        else:
            message = command.how_to

        return message

    def giveAway(self):
        """Démarre un giveaway."""

        Giveaway.objects.all().delete()
        Giveaway.objects.create(participants={'participants': []})
        message = GIVEAWAY['success']

        return message
