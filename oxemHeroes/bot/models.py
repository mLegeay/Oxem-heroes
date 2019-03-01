import os
from datetime import datetime
from random import *

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone

import discord

from .constants import (ADD_PARAM,
                        ADD_SILVER_DONE,
                        ADD_SILVER_USER,
                        BONUS_XP,
                        CHOISIR_DONE,
                        CHOISIR_FAIL,
                        COMMAND_LIST,
                        COMMAND_NOT_EXIST,
                        DEJA_CHOISIS,
                        LEVEL_LIST,
                        NON_AUTHORIZED,
                        ON_CD,
                        SHOSI_COMP,
                        SHOSI_CRIT,
                        SILVER_GLOBAL,
                        SILVER_USER,
                        TALK_COMP,
                        TALK_FAIL,
                        TALK_RATE_FAIL,
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
        return self._get_member(message.author)

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
        self.save(update_fields=['silver'])
        Game.objects.add_silver(silver)
        return ADD_SILVER_DONE.format(silver, self.member.name)

    def add_experience(self, experience):
        self.experience = experience * (1 + Game.objects.get_bonusxp() / 100)
        self.save(update_fields=['experience'])

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

    xp_comp = models.IntegerField(default=0)
    min_silver_comp = models.IntegerField(default=0)
    max_silver_comp = models.IntegerField(default=0)

    cd_comp = models.IntegerField(default=0)  # Temps en minute

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

    def get_bonusxp(self):
        return self._get_game().bonus_xp


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

    def _get_commandHistory(self, command_name, message):

        member, created = Member.objects.from_message(message)
        command = Command.objects.get(name=command_name)

        try:
            commandHistory = self.get(member=member, command=command)
        except self.model.DoesNotExist:
            commandHistory = self.create(member=member, command=command)
            created = True

        return commandHistory, created

    def check_cooldown(self, command_name, message, cooldown, force=False):

        commandHistory, created = self._get_commandHistory(command_name, message)
        now = datetime.now()

        can_use = True

        if not created:
            used_since = (now - commandHistory.last_used.replace(tzinfo=None)).total_seconds()//60 - cooldown
            if used_since >= cooldown or force:
                commandHistory.last_used = now
                commandHistory.save(update_fields=['last_used'])
            else:
                can_use = used_since

        return can_use

    def update_bonus(self, command_name, message, bonus):

        commandHistory, created = self._get_commandHistory(command_name, message)

        if commandHistory.bonus <= 20:
            commandHistory.bonus += bonus
        if commandHistory.bonus > 20:
            commandHistory.bonus = 20

        commandHistory.save(update_fields=['bonus'])


class CommandHistory(models.Model):
    """Modèle des commandes."""

    member = models.ForeignKey(on_delete=models.CASCADE, to='Member', null=False, unique=True)
    command = models.ForeignKey(on_delete=models.CASCADE, to='Command', null=False, unique=True)
    last_used = models.DateTimeField(default=timezone.now,
                                     verbose_name="Date de création")

    bonus = models.IntegerField(default=0, null=True)

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

        files = None

        if command_name in COMMAND_LIST:
            command = self._get_command(command_name)

            gameMember = GameMember.objects.from_message(send_message)
            if command.name == "choisir":
                if gameMember is None and parameters:
                    message = GameMember.objects.create_character(send_message, parameters[0])
                elif gameMember is not None and parameters:
                    message = DEJA_CHOISIS
                else:
                    message = command.how_to
                    files = []
                    path = "{}/oxemHeroes/bot/static/image".format(settings.DJANGO_ROOT)
                    for file in os.listdir(path):
                        if os.path.isfile(os.path.join(path, file)):
                            files.append(discord.File(os.path.join(path, file)))

            elif gameMember is None:
                message = "Commencez par choisir un héros."

            elif command_name == "xp":
                message = gameMember.get_experience()

            elif command_name == "silver":
                message = Game.objects.get_silver()

            elif command_name == "contribution":
                message = gameMember.get_silver()

            elif command_name == "justice":
                message = GameMember.objects.from_message(send_message)

            elif command_name == "pillage":
                experience = gameMember.classe.xp_comp
                silver = randint(gameMember.classe.min_silver_comp, gameMember.classe.max_silver_comp)

                success = False if TALK_RATE_FAIL <= random() else True

                if success:
                    bonus = randint(MIN_BONUS_TALK, MAX_BONUS_TALK)

                else:
                    bonus = 0

                can_use = CommandHistory.objects.check_cooldown(command_name, send_message, gameMember.classe.cd_comp)

                if can_use is True:
                    CommandHistory.objects.update_bonus(command_name, send_message, gameMember.classe.cd_comp, bonus)
                    silver += bonus
                    if success:
                        message = TALK_COMP.format(gameMember.member.name, experience, silver)
                    else:
                        message = TALK_FAIL.format(gameMember.member.name, experience, silver)
                else:
                    message = ON_CD.format(int(gameMember.classe.cd_comp - can_use))

            elif command_name == "aquillon" and gameMember.classe.name == "shosizuke":
                is_crit = ''
                force = False
                experience = gameMember.classe.xp_comp
                silver = randint(gameMember.classe.min_silver_comp, gameMember.classe.max_silver_comp)

                if SHOSI_CRIT >= random():
                    is_crit = ' ▶️ CRITIQUE '
                    silver *= 2
                    force = True

                can_use = CommandHistory.objects.check_cooldown(command_name, send_message,
                                                                gameMember.classe.cd_comp, force)

                if can_use is True:
                    message = SHOSI_COMP.format(gameMember.member.name, is_crit, experience, silver)
                else:
                    message = ON_CD.format(int(gameMember.classe.cd_comp - can_use))

            elif send_message.author.guild_permissions.administrator == "cacajuete":
                if command_name == "bonusxp":
                    if parameters:
                        message = Game.objects.alter_xp(parameters[0])
                    else:
                        message = ADD_PARAM

                elif command_name == "addsilver":
                    if len(parameters) == 2 and send_message.mentions:
                        gameMember = GameMember.objects.from_discord(send_message.mentions[0])

                        if gameMember is not None:
                            message = gameMember.add_silver(int(parameters[0]))
                        else:
                            message = ADD_SILVER_USER
                    else:
                        message = ADD_PARAM

            else:
                message = NON_AUTHORIZED

        else:
            return COMMAND_NOT_EXIST, files

        return message, files


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
