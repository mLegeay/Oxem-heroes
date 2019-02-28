from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone

from .constants import (ADD_PARAM,
                        ADD_SILVER_USER,
                        BONUS_XP,
                        CHOISIR_DONE,
                        CHOISIR_FAIL,
                        COMMAND_LIST,
                        COMMAND_NOT_EXIST,
                        DEJA_CHOISIS,
                        LEVEL_LIST,
                        SILVER_GLOBAL,
                        SILVER_USER,
                        XP,
                        XP_REQUIRE)


class EventsLog(models.Model):
    """Modèle du journal de log."""

    date_created = models.DateTimeField(default=timezone.now,
                                        db_index=True,
                                        verbose_name="Date de l'erreur")
    error = models.TextField(null=False)
    command = models.CharField(max_length=100, null=False)


class MemberQuerySet(models.QuerySet):
    """Requête de base pour les membres."""

    def _get_member(self, discord_user):

        created = False
        try:
            member = self.get(discord_id=discord_user.id)
            if member.name != discord_user.name:
                member.name = discord_user.name
                member.save()
        except self.model.DoesNotExist:
            member = self.create(discord_id=discord_user.id,
                                 name=discord_user.name,
                                 discriminator=discord_user.discriminator,
                                 joined_at=discord_user.joined_at)
            created = True

        except Exception as error:
            EventsLog.objects.create(error=error, command="get_member")

        return member, created

    def from_message(self, message):
        return self._get_member(message.author)[0]

    def from_discord(self, discord_user):
        return self._get_member(discord_user)[0]


class Member(models.Model):
    """Modèle des utilisateurs ayant utilisé au moins une commande OxemHeroes."""

    discord_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    joined_at = models.DateTimeField()

    discriminator = models.CharField(max_length=10)
    bot = models.BooleanField(default=False)

    objects = MemberQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return '{0}#{1}'.format(self.name, self.discriminator)


class GameMemberQuerySet(models.QuerySet):
    """Requête de base pour les informations de partie."""

    def _get_gameMember(self, discord_user):
        created = False
        member = Member.objects.from_discord(discord_user)
        try:
            gameMember = self.get(member=member)
        except self.model.DoesNotExist:
            return None

        return gameMember

    def from_message(self, message):
        return self._get_gameMember(message.author)

    def from_discord(self, discord_user):
        return self._get_gameMember(discord_user)

    def create_character(self, message, name):
        member, created = Member.objects.from_message(message)
        classe = Classe.objects.get_classe(name)

        if not isinstance(classe, str):  # and created is True:
            gameMember = self.create(member=member, classe=classe)
        else:
            return CHOISIR_FAIL

        return CHOISIR_DONE.format(name)


class GameMember(models.Model):
    """Modèle des informations sur les joueurs jouant à OxemHeroes."""

    member = models.ForeignKey(on_delete=models.CASCADE, to='Member', null=False, unique=True)
    classe = models.ForeignKey(on_delete=models.CASCADE, to='Classe', null=False)
    joined_at = models.DateTimeField(default=timezone.now,
                                     verbose_name="Date de création")

    experience = models.IntegerField(default=0)
    silver = models.IntegerField(default=0)

    objects = GameMemberQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return '{0} - xp : {1} - silver : {2}'.format(self.member.name, self.experience, self.silver)

    def _get_level(self, xp):
        for key, value in enumerate(XP_REQUIRE):
            if xp < key:
                return key
        return XP_REQUIRE.keys()[-1]

    def add_silver(self, silver):
        self.silver += silver
        Game.objects.get_game().add_silver(silver)

    def add_experience(self, experience):
        self.experience = experience

    def get_experience(self):
        level = self._get_level(self.experience)
        return XP.format(LEVEL_LIST[level], level, self.experience)

    def get_silver(self):
        return SILVER_USER.format(self.member.name, self.silver)


class ClasseQuerySet(models.QuerySet):
    """Requête de base pour les informations de partie."""

    def get_classe(self, name):
        return self.get(name=name)


class Classe(models.Model):
    """Modèle des classes d'OxemHeroes."""

    name = models.CharField(max_length=50, unique=True)

    min_xp_comp = models.IntegerField(default=0)
    max_xp_comp = models.IntegerField(default=0)
    min_silver_comp = models.IntegerField(default=0)
    max_silver_comp = models.IntegerField(default=0)

    objects = ClasseQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return '{0}'.format(self.name)


class GameQuerySet(models.QuerySet):
    """Requête de base pour les informations de partie."""

    def add_silver(self, silver):
        game = self._get_game()
        game.silver += silver
        game.save(update_fields=['silver'])

    def alter_xp(self, bonus_xp):
        game = self._get_game()
        game.bonus_xp = bonus_xp
        game.save(update_fields=['bonus_xp'])
        return BONUS_XP.format(self._get_game().bonus_xp)

    def _get_game(self):
        return self.all().first()

    def get_silver(self):
        return SILVER_GLOBAL.format(self._get_game().silver)


class Game(models.Model):
    """Modèle des informations d'OxemHeroes."""

    silver = models.IntegerField(default=0)
    bonus_xp = models.IntegerField(default=0)

    objects = GameQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return 'total silver : {1}'.format(self.silver)


class CommandHistoryQuerySet(models.QuerySet):
    """Requête de base pour l'historique des commandes."""

    def _get_commandHistory(self, message):

        created = False
        member = Member.objects.from_message(message)
        command = Command.objects.from_message(message)

        try:
            commandHistory = self.get(member=member)
        except self.model.DoesNotExist:
            commandHistory = self.create(member=member, command=command)
            created = True

        return commandHistory, created

    def from_message(self, message):
        return self._get_commandHistory(message)[0]


class CommandHistory(models.Model):
    """Modèle des commandes."""

    member = models.ForeignKey(on_delete=models.CASCADE, to='Member', null=False)
    command = models.ForeignKey(on_delete=models.CASCADE, to='Command', null=False)
    last_used = models.DateTimeField(default=timezone.now,
                                     verbose_name="Date de création")

    objects = CommandHistoryQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return 'member : {0} - command : {1} - last_used : {2}'.format(self.member.name, self.command, self.last_used)


class CommandQuerySet(models.QuerySet):
    """Requête de base pour les commandes."""

    def _get_command(self, command_name):

        try:
            command = self.get(name=command_name)

        except self.model.DoesNotExist:
            command = None

        return command

    def execute(self, send_message, command_name, parameters):

        if command_name in COMMAND_LIST:
            command = self._get_command(command_name)

            if command.name == "choisir":
                if GameMember.objects.from_message(send_message) is None:
                    message = GameMember.objects.create_character(send_message, parameters[0])
                else:
                    message = DEJA_CHOISIS

            elif command_name == "xp":
                message = GameMember.objects.from_message(send_message).get_experience()

            elif command_name == "silver":
                message = Game.objects.get_silver()

            elif command_name == "contribution":
                message = GameMember.objects.from_message(send_message).get_silver()

            elif send_message.author.guild_permissions.administrator:
                if command_name == "bonusxp":
                    if parameters:
                        message = Game.objects.alter_xp(parameters[0])
                    else:
                        message = ADD_PARAM

                elif command_name == "addsilver":
                    gameMember = GameMember.objects.from_discord(send_message.mentions[0].id)

                    if gameMember is not None:
                        message = gameMember.add_silver(parameters[0])
                    else:
                        message = ADD_SILVER_USER

        else:
            return COMMAND_NOT_EXIST

        return message


class Command(models.Model):
    """Modèle des commandes."""

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    how_to = models.CharField(max_length=100)

    usable_by = JSONField(null=True)
    active = models.BooleanField(default=True)
    admin_command = models.BooleanField(default=False)

    objects = CommandQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return '{0} - active : {1} - admin? : {2}'.format(self.name, self.active, self.admin_command)
