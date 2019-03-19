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

        files = None

        if command.name == "choisir":
            files, message = self.choisir(command, gameMember, _message, parameters)

        elif command.name == "xp":
            message = self.get_experience()

        elif command.name == "silver":
            message = self.get_silver()

        elif command.name == "contribution":
            message = self.get_silver()

        elif command.name == "jeton":
            message = self.get_token()

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

    def get_experience(gameMember):
        """."""
        return gameMember.get_experience()

    def get_silver(gameMember):
        """."""
        return gameMember.get_silver()

    def get_silver_max(gameMember):
        """."""
        return gameMember.get_silver()

    def get_token(gameMember):
        """."""
        return gameMember.get_token()
