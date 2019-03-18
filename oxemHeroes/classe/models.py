from django.db import models


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
