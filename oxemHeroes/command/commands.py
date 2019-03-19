"""Commande pour les classes.

-
"""

import discord


class Commands(object):
    """Traite les commandes reçus pour les classes."""

    def __init__(self, command, gameMember, _message, parameters):
        """Initialise les valeurs de la classe.

           variables :

           parameters:

           return:
        """

        if command_name == "bonusxp":
            message = self.bonusxp()

        elif command_name == "addsilver":
            message = self.add_silver()

        elif command_name == "addjeton":
            message = self.addjeton()

        elif command_name == "giveaway":
            message = self.giveAway()

        return message

    def bonusxp(self, command, gameMember, _message, parameters):
        """."""

        if parameters:
            message = Game.objects.alter_xp(parameters[0])
        else:
            message = command.how_to

        return message

    def addsilver(gameMember):
        """."""
        if len(parameters) == 2 and send_message.mentions:
            gameMember = GameMember.objects.from_discord(send_message.mentions[0])

            if gameMember is not None:
                message = gameMember.add_silver(int(parameters[0]))
            else:
                message = ERRORS['player_dne']
        else:
            message = command.how_to

        return message

    def addjeton(gameMember):
        """."""
        if len(parameters) == 2 and send_message.mentions:
            gameMember = GameMember.objects.from_discord(send_message.mentions[0])

            if gameMember is not None:
                message = gameMember.add_token(int(parameters[0]))
            else:
                message = ERRORS['player_dne']
        else:
            message = command.how_to

        return message

    def giveAway(gameMember):
        """."""
        Giveaway.objects.all().delete()
        Giveaway.objects.create(participants={'participants': []})
        message = "Giveaway créé avec succès"

        return message
