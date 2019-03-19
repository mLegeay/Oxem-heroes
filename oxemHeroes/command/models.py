from django.db import models
from oxemHeroes.classe.commands import Commands


class CommandQuerySet(models.QuerySet):
    """Requête de base pour les commandes."""

    def _get_command(self, command_name):

        try:
            command = self.get(name=command_name)

        except self.model.DoesNotExist:
            command = None

        return command

    def execute(self, send_message, command_name, parameters):

        files = None

        if command_name in COMMAND_LIST:
            command = self._get_command(command_name)

            gameMember = GameMember.objects.from_message(send_message)

            if command_name in PLAYER_COMMAND or command_name in SKILL_LIST:
                if command.name == "choisir":
                    if gameMember is None and parameters:
                        if parameters[0].lower() in HERO_LIST:
                            message = GameMember.objects.create_character(send_message, parameters[0].lower())
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

                elif gameMember is None:
                    message = ERRORS['not_a_player']

                elif command_name == "xp":
                    message = gameMember.get_experience()

                elif command_name == "silver":
                    message = Game.objects.get_silver()

                elif command_name == "contribution":
                    message = gameMember.get_silver()

                elif command_name == "jeton":
                    message = gameMember.get_token()

                elif command_name in SKILL_LIST:
                    message = Commands(command_name, gameMember, send_message)

            elif send_message.author.guild_permissions.administrator and command_name in ADMIN_COMMAND_LIST:
                if command_name == "bonusxp":
                    if parameters:
                        message = Game.objects.alter_xp(parameters[0])
                    else:
                        message = command.how_to

                elif command_name == "addsilver":
                    if len(parameters) == 2 and send_message.mentions:
                        gameMember = GameMember.objects.from_discord(send_message.mentions[0])

                        if gameMember is not None:
                            message = gameMember.add_silver(int(parameters[0]))
                        else:
                            message = ERRORS['player_dne']
                    else:
                        message = command.how_to

                elif command_name == "addjeton":
                    if len(parameters) == 2 and send_message.mentions:
                        gameMember = GameMember.objects.from_discord(send_message.mentions[0])

                        if gameMember is not None:
                            message = gameMember.add_token(int(parameters[0]))
                        else:
                            message = ERRORS['player_dne']
                    else:
                        message = command.how_to

                elif command_name == "giveaway":
                    Giveaway.objects.all().delete()
                    Giveaway.objects.create(participants={'participants': []})
                    message = "Giveaway créé avec succès"

            elif command_name == "participer":
                message = Giveaway.objects.participer(send_message)

            else:
                message = ERRORS['non_authorized']

        elif command_name in HELP_COMMAND:

            if parameters:
                command = self._get_command(parameters[0])

                if command is not None:
                    message = "`{}`".format(command.how_to)
                else:
                    message = ERRORS['command_dne']
            else:
                message = HELP_MESSAGE['start']

                for each in PLAYER_COMMAND:
                    command = self._get_command(each)
                    message += "- {}: {}\n".format(command.name, command.description)

                message += HELP_MESSAGE['classe']

                for each in SKILL_LIST:
                    command = self._get_command(each)
                    message += "- {}: {}\n".format(command.name, command.description)

                message += HELP_MESSAGE['end']

        else:
            message = ERRORS['command_dne']

        return message, files


class Command(models.Model):
    """Modèle des commandes."""

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    how_to = models.CharField(max_length=100)

    objects = CommandQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return '{0} - active : {1} - admin? : {2}'.format(self.name)
