from django.db import models
from django.utils import timezone

from django.contrib.postgres.fields import JSONField

from oxemHeroes.classe.models import Classe
from oxemHeroes.game.models import Game
from oxemHeroes.gameMember.constants import DONE, LEVEL_LIST, XP_REQUIRE
from oxemHeroes.member.models import Member


class GameMemberQuerySet(models.QuerySet):
    """Requête de base pour les informations de partie."""

    def _get_gameMember(self, discord_user):
        """Récupère le gameMember à partir de l'utilisateur discord.
           return :
           - GameMember gameMember (membre jouant à Oxem-Heroes)
        """

        member = Member.objects.from_discord(discord_user)

        try:
            """On vérifie que le joueur existe bien."""
            gameMember = self.get(member=member)

        except self.model.DoesNotExist:
            """Si le joueur n'existe pas il doit commencer par utiliser la commande !choisir."""
            return None

        return gameMember

    def from_message(self, message):
        """Renvoi le gameMember (GameMember) associé au message discord."""

        return self._get_gameMember(message.author)

    def from_discord(self, discord_user):
        """Renvoi le gameMember (GameMember) associé à l'utilisateur discord."""

        return self._get_gameMember(discord_user)

    def create_character(self, message, name):
        """L'utilisateur créer son personnage.

           Si la classe existe, elle est attribué à un joueur.

           return:
           - str (message indiquant que la création c'est bien déroulée.)
        """

        member, created = Member.objects.from_message(message)
        classe = Classe.objects.get_classe(name)

        if not isinstance(classe, str):
            gameMember = self.create(member=member, classe=classe)

        return DONE['choisir'].format(name)


class GameMember(models.Model):
    """Modèle des informations sur les joueurs jouant à OxemHeroes."""

    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, null=False)
    joined_at = models.DateTimeField(default=timezone.now,
                                     verbose_name="Date de création")

    experience = models.IntegerField(default=0)
    silver = models.IntegerField(default=0)
    max_silver = models.IntegerField(default=0)
    token = models.IntegerField(default=0)

    inventory = JSONField(default={'hero': []})

    objects = GameMemberQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return '{0} - xp : {1} - silver : {2}'.format(self.member.name, self.experience, self.silver)

    def _get_level(self, xp):
        """Renvoi le level du joueur."""

        for key, value in enumerate(XP_REQUIRE):
            if xp < value:
                return key
        return XP_REQUIRE.keys()[-1]

    def add_silver(self, silver):
        """Ajoute des silvers au joueur."""

        self.silver += silver
        self.max_silver += silver
        self.save(update_fields=['silver'])
        Game.objects.add_silver(silver)
        return silver

    def add_token(self, token):
        """Ajoute des jetons au joueur."""

        self.token += token
        self.save(update_fields=['token'])
        return token

    def add_experience(self, experience):
        """Ajoute de l'expérience au joueur."""

        experience = experience * (1 + Game.objects.get_bonusxp() / 100)
        self.experience += experience
        self.save(update_fields=['experience'])

        return int(experience)

    def get_experience(self):
        """Renvoi un message contenant le titre, level et niveau du joueur."""

        level = self._get_level(self.experience) + 1
        return DONE['xp'].format(LEVEL_LIST[level], level, self.experience)

    def get_silver(self):
        """Renvoi un message contenant les silvers du joueur."""

        return DONE['silver_user'].format(self.member.name, self.silver)

    def get_token(self):
        """Renvoi un message contenant les jetons du joueur."""

        return DONE['token_user'].format(self.token)

    def update_character(self, name):
        """L'utilisateur met à jour son personnage.

           Si la classe existe, elle est attribué au joueur.

           return:
           - str (message indiquant que la création c'est bien déroulée.)
        """

        classe = Classe.objects.get_classe(name)

        if not isinstance(classe, str):
            self.classe = classe
            self.token -= 1
            self.save(update_fields=['classe', 'token'])

        return DONE['choisir'].format(name)
