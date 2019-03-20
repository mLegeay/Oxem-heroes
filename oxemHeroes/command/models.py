from django.db import models


class CommandQuerySet(models.QuerySet):
    """Requête de base pour les commandes."""

    def _get_command(self, command_name):

        try:
            command = self.get(name=command_name)

        except self.model.DoesNotExist:
            command = None

        return command

    def from_name(self, command_name):

        return self._get_command(command_name)


class Command(models.Model):
    """Modèle des commandes."""

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    how_to = models.CharField(max_length=100)

    objects = CommandQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return '{0}'.format(self.name)
