"""Commande pour les gameMember.

- choisir : Permet de choisir un héros parmis la liste des héros
- recruter : Permet de recruter un héros
- xp : Renvoi un message contenant le niveau, le titre et l'xp obtenu jusque la
- silver : Renvoi un message contenant le nombre de silver possédé par un joueur
- contribution : ???????? a changer ??????????
- jeton : Renvoi un message contenant le nombre de silver possédé par un joueur
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

        elif command.name == "recruter":
            files, message = self.recruter(command, gameMember, parameters)

        elif command.name == "xp":
            message = self.get_experience(gameMember)

        elif command.name == "silver":
            message = self.get_silver(gameMember)

        elif command.name == "silvermax":
            message = self.get_silver_max(gameMember)

        elif command.name == "jeton":
            message = self.get_token(gameMember)

        return files, message

    def choisir(self, command, gameMember, _message, parameters):
        """Gère le choix du héros par le joueur.

           Retourne un message et des fichiers de type DiscordFile.
        """

        files = None

        if parameters:
            if parameters[0].lower() in HERO_LIST:
                if gameMember is None:
                    message = GameMember.objects.create_character(_message, parameters[0].lower())
                else:
                    if gameMember.token > 0:
                        if gameMember.classe.name == parameters[0].lower():
                            message = ERRORS['already_hero']

                        elif parameters[0].lower() in gameMember.inventory['hero']:
                            message = gameMember.update_character(parameters[0].lower())

                        else:
                            message = ERRORS['not_own']
                    else:
                        message = ERRORS['not_enough_token']

            else:
                message = ERRORS['hero_dne']

        else:
            message = command.how_to
            files = []
            path = "{}/oxemHeroes/classe/static/image".format(settings.DJANGO_ROOT)

            if gameMember is not None:
                hero_list = gameMember.inventory['hero']

            else:
                hero_list = FREE_HERO_LIST

            for each in hero_list:
                files.append(discord.File(os.path.join(path, "{}.png".format(each))))

        return files, message

    def recruter(self, command, gameMember, parameters):
        """Permet d'acheter un héro et l'ajouter à sa liste de héros possédés.

           Retourne un message et des DiscordFiles si l'utilisateur souhaite découvrir
           quels sont les héros disponible à l'achat.
        """

        files = None

        if parameters:
            if parameters[0].lower() in gameMember.inventory['hero']:
                message = ERRORS['already_own']

            elif parameters[0].lower() in HERO_LIST:
                message = gameMember.buy_hero(parameters[0].lower())

            else:
                message = ERRORS['hero_dne']

        else:
            message = command.how_to + "\n```Css\n [/!\ Lord Typus s'écrit lord_typus /!\]```"
            files = []
            path = "{}/oxemHeroes/classe/static/image".format(settings.DJANGO_ROOT)
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
        return gameMember.get_silvermax()

    def get_token(self, gameMember):
        """Retourne un message contenant les jetons du joueur."""
        return gameMember.get_token()
