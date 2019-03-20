"""Commande pour les classes.

-
"""

import discord

from oxemHeroes.game.models import Game
from oxemHeroes.gameMember.models import GameMember


class Commands(object):
    """Traite les commandes reçus pour les classes."""

    def __init__(self):
        """Initialise les valeurs de la classe."""

    def process(self, command, gameMember, _message, parameters):
        """variables :

           parameters:

           return:
        """

        if command.name == "bonusxp":
            message = self.bonusxp(command, gameMember, parameters)

        elif command.name == "addsilver":
            message = self.addsilver(gameMember, _message, parameters)

        elif command.name == "addjeton":
            message = self.addjeton(gameMember, _message, parameters)

        elif command.name == "giveaway":
            message = self.giveAway(gameMember)

        return message

    def bonusxp(self, command, gameMember, parameters):
        """."""

        if parameters:
            message = Game.objects.alter_xp(parameters[0])
        else:
            message = command.how_to

        return message

    def addsilver(self, gameMember, _message, parameters):
        """."""
        if len(parameters) == 2 and _message.mentions:
            gameMember = GameMember.objects.from_discord(_message.mentions[0])

            if gameMember is not None:
                message = gameMember.add_silver(int(parameters[0]))
            else:
                message = ERRORS['player_dne']
        else:
            message = command.how_to

        return message

    def addjeton(self, gameMember, _message, parameters):
        """."""
        if len(parameters) == 2 and _message.mentions:
            gameMember = GameMember.objects.from_discord(_message.mentions[0])

            if gameMember is not None:
                message = gameMember.add_token(int(parameters[0]))
            else:
                message = ERRORS['player_dne']
        else:
            message = command.how_to

        return message

    def giveAway(self, gameMember):
        """."""
        Giveaway.objects.all().delete()
        Giveaway.objects.create(participants={'participants': []})
        message = "Giveaway créé avec succès"

        return message
