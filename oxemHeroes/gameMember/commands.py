"""Commande pour les gameMember.

- choisir : Permet de choisir un héros parmis la liste des héros
- xp : Renvoi un message contenant le niveau, le titre et l'xp obtenu jusque la
"""
import os

from django.conf import settings
from oxemHeroes.gameMember.constants import HERO_LIST, ERRORS
from oxemHeroes.gameMember.models import GameMember

import discord


class Commands(object):
    """Traite les commandes reçus pour les classes."""

    def __init__(self):
        """Initialise les valeurs de la classe."""

    def process(self, command, gameMember, _message, parameters):
        """variables :
           - DiscordFile files : fichier à envoyer avec le message
           - String message  : Message renvoyé en réponse à l'utilisateur

           parameters:
           - Command command : commande utilisée par l'utilisateur
           - GameMember gameMember : Utilisateur ayant lancée la commande
           - String _message  : Message envoyé par l'utilisateur
           - Tuple parameters : Liste des mots utilisés après la commande

           return:
           - DiscordFile files : fichier à envoyer avec le message
           - String message  : Message renvoyé en réponse à l'utilisateur
        """

        files = None

        if command.name == "choisir":
            files, message = self.choisir(command, gameMember, _message, parameters)

        elif command.name == "xp":
            message = self.get_experience(gameMember)

        elif command.name == "silver":
            message = self.get_silver(gameMember)

        elif command.name == "contribution":
            message = self.get_silver(gameMember)

        elif command.name == "jeton":
            message = self.get_token(gameMember)

        return files, message

    def choisir(self, command, gameMember, _message, parameters):
        """."""

        files = None

        if gameMember is None and parameters:
            if parameters[0].lower() in HERO_LIST:
                message = GameMember.objects.create_character(_message, parameters[0].lower())

            else:
                message = ERRORS['hero_dne']

        elif gameMember is not None and parameters:
            message = ERRORS['deja_choisis']

        else:
            message = command.how_to
            files = []
            path = "{}/oxemHeroes/bot/static/image".format(settings.DJANGO_ROOT)
            for file in os.listdir(path):
                if os.path.isfile(os.path.join(path, file)):
                    files.append(discord.File(os.path.join(path, file)))

        return files, message

    def get_experience(self, gameMember):
        """Retourne un message contenant l'experience, le level et le titre du joueur."""
        return gameMember.get_experience()

    def get_silver(self, gameMember):
        """Retourne un message contenant les silvers du joueur."""
        return gameMember.get_silver()

    def get_silver_max(self, gameMember):
        """Retourne un message contenant les silvers accumulés joueur."""
        return gameMember.get_silver()

    def get_token(self, gameMember):
        """Retourne un message contenant les jetons du joueur."""
        return gameMember.get_token()
