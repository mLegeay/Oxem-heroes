from django.db import models

from oxemHeroes.game.constants import ADMIN_DONE, DONE


class GameQuerySet(models.QuerySet):
    """Requête de base pour les informations de partie."""

    def _get_game(self):
        return self.all().first()

    def add_silver(self, silver):
        game = self._get_game()
        game.silver += silver
        game.save(update_fields=['silver'])

    def alter_xp(self, bonus_xp):
        game = self._get_game()
        game.bonus_xp = bonus_xp
        game.save(update_fields=['bonus_xp'])
        return ADMIN_DONE['bonus_xp'].format(self._get_game().bonus_xp)

    def get_silver(self):
        return DONE['silver_global'].format(self._get_game().silver)

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
