"""Commande pour les command.

- help/aide : liste les commandes et comment les utiliser
- addjeton : ajoute des jetons à un utilisateur donnée
- add silver : ajoute des silvers à un utilisateur donnée
- bonusxp : modifier le bonus d'xp sur l'expérience gagnée
- giveaway : créer un giveaway
"""

from random import *

import discord
from oxemHeroes.command.constants import (ADMIN_DONE, ERRORS, GIVEAWAY,
                                          HELP_MESSAGE, PLAYER_COMMAND,
                                          SKILL_LIST)
from oxemHeroes.command.exceptions import CommandError
from oxemHeroes.command.models import Command
from oxemHeroes.game.models import Game
from oxemHeroes.gameMember.models import GameMember
from oxemHeroes.giveAway.models import Giveaway
from oxemHeroes.utils import check_param_type


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

        if len(parameters) != 0:
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
            message = self.addsilver(command, _message, parameters)

        elif command.name == "addjeton":
            message = self.addjeton(command, _message, parameters)

        elif command.name == "giveaway":
            message = self.giveAway()

        elif command.name == "gagnant":
            message = self.winner(command, parameters)

        return message

    def bonusxp(self, command, parameters):
        """Modifie le multiplicateur d'expérience."""

        if parameters:
            message = Game.objects.alter_xp(parameters[0])
        else:
            message = command.how_to

        return message

    def addsilver(self, command, _message, parameters):
        """Ajoute des silvers pour un utilisateur donnée."""

        try:
            if len(parameters) == 2 and _message.mentions and int(parameters[0]):
                gameMember = GameMember.objects.from_discord(_message.mentions[0])

                if gameMember is not None:
                    silver = gameMember.add_silver(int(parameters[0]))
                    message = ADMIN_DONE['add_silver'].format(silver, gameMember.member.name)

                else:
                    message = ERRORS['player_dne']
            else:
                raise CommandError(command)

        except (CommandError, ValueError):
            message = command.how_to

        return message

    def addjeton(self, command, _message, parameters):
        """Ajoute des jetons pour un utilisateur donnée."""

        try:
            if len(parameters) == 2 and _message.mentions and int(parameters[0]):
                gameMember = GameMember.objects.from_discord(_message.mentions[0])

                if gameMember is not None:
                    token = gameMember.add_token(int(parameters[0]))
                    message = ADMIN_DONE['add_token'].format(token, gameMember.member.name)
                else:
                    message = ERRORS['player_dne']
            else:
                raise CommandError(command)

        except (CommandError, ValueError):
            message = command.how_to

        return message

    def giveAway(self):
        """Démarre un giveaway."""

        Giveaway.objects.all().delete()
        Giveaway.objects.create(participants={'participants': []})
        message = GIVEAWAY['success']

        return message

    def winner(self, command, parameters):
        """Donne un nom de gagnant et supprime le giveaway."""

        participants = Giveaway.objects.first()

        if participants is not None:
            participants = participants.participants['participants']

            if len(parameters) != 0:
                if check_param_type("int", parameters[0]):
                    gagnants = int(parameters[0])
                    if len(participants) >= gagnants:
                        if gagnants > 0:
                            winner_list = []

                            while len(winner_list) < gagnants:
                                winner_member = participants[randint(0, len(participants) - 1)]
                                if winner_member not in winner_list:
                                    winner_list.append(winner_member)

                            for each in winner_list:
                                message = "{} ".format(each)

                            message = GIVEAWAY['winners'].format(message)
                            Giveaway.objects.all().delete()

                        else:
                            message = ERRORS['invalid_parameter_ga'].format(gagnants)

                    else:
                        message = ERRORS['not_enough_participants']

                else:
                    message = command.how_to

            elif len(participants) != 0:
                winner_member = participants[randint(0, len(participants) - 1)]
                Giveaway.objects.all().delete()
                message = GIVEAWAY['winner'].format(winner_member)

            else:
                message = ERRORS['no_participant']
        else:
            message = ERRORS['no_giveaway']

        return message
