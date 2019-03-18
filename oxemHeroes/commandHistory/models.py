from django.db import models
from django.utils import timezone

from oxemHeroes.command.models import Command
from oxemHeroes.member.models import Member


class CommandHistoryQuerySet(models.QuerySet):
    """Requête de base pour l'historique des commandes."""

    def _get_commandHistory(self, command_name, message):
        """Récupère la dernière utilisation de la commande par le joueur.

           parameter:
           - String command_name = nom de la commande utilisée
           - String message = message contenant la commande

           return :
           - CommandHistory commandHistory (la commande concernée)
           - Boolean created = Boolean permettant de vérifier si la commande est à sa première utilisation
        """

        member, created = Member.objects.from_message(message)
        command = Command.objects.get(name=command_name)

        try:
            commandHistory = self.get(member=member, command=command)

        except self.model.DoesNotExist:
            """Si la commandHistory n'existe pas on la créer."""

            commandHistory = self.create(member=member, command=command)
            created = True

        return commandHistory, created

    def check_cooldown(self, command_name, message, cooldown, force=False):
        """Vérifie si la commande peut être réutilisé.

           Si la commandHistory vient d'être créé, can_use est à True par défaut

           parameter:
           - String command_name = nom de la commande utilisée
           - String message = message contenant la commande
           - Integer cooldown = temps en minute avant de pouvoir réutiliser la commande
           - Boolean force = permet l'utilisation de la commande sans prise en compte du cooldown

           return:
           - Boolean can_use = True si la commande peut être utilisé, False sinon
        """

        commandHistory, created = self._get_commandHistory(command_name, message)
        now = timezone.now()

        can_use = True

        if not created:
            used_since = (now - commandHistory.last_used).total_seconds()//60
            if used_since >= cooldown or force:
                commandHistory.last_used = now
                commandHistory.save(update_fields=['last_used'])
            else:
                can_use = used_since

        return can_use

    def update_bonus(self, command_name, message, bonus):
        """Met à jour le bonus.

           Le bonus est utilisé par :
           - Shosizuke : si la valeur est à 1 c'est un critique
           - Talkoran : bonus sur son gain en silver allant de 0 à 20

           parameter:
           - String command_name = nom de la commande utilisée
           - String message = message contenant la commande
           - Integer bonus = bonus à appliquer

           return:
           - Integer bonus = bonus à appliquer
        """

        commandHistory, created = self._get_commandHistory(command_name, message)

        if commandHistory.bonus <= 20:
            commandHistory.bonus += bonus
        if commandHistory.bonus > 20:
            commandHistory.bonus = 20

        if bonus == -1:
            commandHistory.bonus = 0

        commandHistory.save(update_fields=['bonus'])

        return commandHistory.bonus

    def get_bonus(self, command_name, message):
        """Renvoi le bonus.

           Si la commandHistory vient d'être créée, detruit la commandHistory et renvoi 0
           Ceci pour indiquer à Shosizuke que cela correspond à sa première compétence

           return:
           - Integer bonus = bonus à appliquer
        """

        commandHistory, created = self._get_commandHistory(command_name, message)
        if created:
            commandHistory.delete()
            return 0

        return self._get_commandHistory(command_name, message)[0].bonus


class CommandHistory(models.Model):
    """Modèle des commandes."""

    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=False)
    command = models.ForeignKey(Command, on_delete=models.CASCADE, null=False)
    last_used = models.DateTimeField(default=timezone.now,
                                     verbose_name="Date de création")

    bonus = models.IntegerField(default=0, null=True)

    objects = CommandHistoryQuerySet.as_manager()

    class Meta:
        unique_together = ('member', 'command',)

    def __str__(self):
        """Override de la méthode __str__."""

        return 'member : {0} - command : {1} - last_used : {2}'.format(self.member.name, self.command, self.last_used)
