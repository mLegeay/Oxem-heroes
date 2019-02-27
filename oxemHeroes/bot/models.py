from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


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
    avatar = models.CharField(max_length=255, null=True)
    bot = models.BooleanField(default=False)

    objects = MemberQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return '{0}#{1}'.format(self.name, self.discriminator)


class GameQuerySet(models.QuerySet):
    """Requête de base pour les informations de partie."""

    def _get_game(self, discord_user):

        created = False
        member = Member.objects.from_discord(discord_user.id)
        try:
            game = self.get(member=member)
        except self.model.DoesNotExist:
            game = self.create(member=member)
            created = True

        return game, created

    def from_message(self, message):
        return self._get_game(message.author)[0]

    def from_discord(self, discord_user):
        return self._get_game(discord_user)[0]


class Game(models.Model):
    """Modèle des informations sur les joueurs jouant à OxemHeroes."""

    member = models.ForeignKey(on_delete=models.CASCADE, to='Member', null=False)
    joined_at = models.DateTimeField(default=timezone.now,
                                     verbose_name="Date de création")

    experience = models.IntegerField(default=0)
    silver = models.IntegerField(default=0)

    objects = GameQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return '{0} - xp : {1} - silver : {2}'.format(self.member.name, self.experience, self.silver)


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

        command = self.get(name=command_name)

        return command

    def from_message(self, command_name):
        return self._get_command(command_name)[0]


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
