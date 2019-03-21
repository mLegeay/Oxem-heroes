"""Commande pour les gameMember.

- participer : Permet de participer à un giveaway
"""

from oxemHeroes.giveAway.models import Giveaway


class Commands(object):
    """Traite les commandes reçus pour les classes."""

    def __init__(self):
        """Initialise les valeurs de la classe."""

    def process(self, command, _message):
        """variables :
           - String message  : Message renvoyé en réponse à l'utilisateur

           parameters:
           - Command command : commande utilisée par l'utilisateur
           - String _message  : Message envoyé par l'utilisateur

           return:
           - String message  : Message renvoyé en réponse à l'utilisateur
        """

        if command.name == "participer":
            message = self.participer(_message)

        return message

    def participer(self, _message):
        """Permet de participer à un giveaway."""

        return Giveaway.objects.participer(_message)
