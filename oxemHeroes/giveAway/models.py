from django.contrib.postgres.fields import JSONField
from django.db import models

from oxemHeroes.giveAway.constants import PARTICIPER, PARTICIPER_ERROR
from oxemHeroes.member.models import Member


class GiveawayQuerySet(models.QuerySet):
    """Requête de base pour les informations de giveaway."""

    def _get_giveaway(self):
        """Récupère le giveAway en cours.
           return :
           - GiveAway giveaway (Un seul giveAway à la fois)
        """

        return self.all().first()

    def _get_participants(self):
        """Récupère une liste des participants au giveAway.
           return :
           - [participants] (liste des participants d'un giveAway)
        """

        return self._get_giveaway().participants['participants']

    def participer(self, send_message):
        message = PARTICIPER

        member, created = Member.objects.from_message(send_message)

        giveaway = self._get_giveaway()
        participants = self._get_participants()

        if member.__str__() not in participants:
            giveaway.participants['participants'].append(member.__str__())
            giveaway.save()

        else:
            message = PARTICIPER_ERROR

        return message


class Giveaway(models.Model):
    """Modèle des Giveaway."""

    participants = JSONField()

    objects = GiveawayQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return 'participants : {0}'.format(self.participants)
