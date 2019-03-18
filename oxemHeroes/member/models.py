from django.db import models


class MemberQuerySet(models.QuerySet):
    """Requête de base pour les membres."""

    def _get_member(self, discord_user):
        """Récupère l'utilisateur discord et l'insère dans la base de données s'il n'existe pas.
           return :
           - Member member (membre correspondant à l'utilisateur discord)
           - Boolean created (Boolean permettant de savoir si l'utilisateur est nouveau ou non).
        """

        created = False

        try:
            member = self.get(discord_id=discord_user.id)
            if member.name != discord_user.name:
                member.name = discord_user.name
                member.save()

        except self.model.DoesNotExist:
            """Si l'utilisateur n'existe pas on le créer."""

            member = self.create(discord_id=discord_user.id,
                                 name=discord_user.name,
                                 discriminator=discord_user.discriminator,
                                 joined_at=discord_user.joined_at)

            created = True

        except Exception as error:
            """En cas d'erreur, créer un log pour pouvoir reproduire et corriger le bug."""

            EventsLog.objects.create(error=error, command="get_member")

        return member, created

    def from_message(self, message):
        """Renvoi le membre (Member) associé au message discord."""

        return self._get_member(message.author)

    def from_discord(self, discord_user):
        """Renvoi le membre (Member) associé à l'utilisateur discord."""

        return self._get_member(discord_user)[0]


class Member(models.Model):
    """Modèle des utilisateurs ayant utilisé au moins une commande OxemHeroes.

       discord_id = id discord (419757496912183297)
       name = pseudonyme discord
       joined_at = date à laquelle l'utilisateur à effectué sa première commande
       discriminator = 4 chiffres après le # du pseudo discord
    """

    discord_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    joined_at = models.DateTimeField()

    discriminator = models.CharField(max_length=10)

    objects = MemberQuerySet.as_manager()

    def __str__(self):
        """Override de la méthode __str__."""

        return '{0}#{1}'.format(self.name, self.discriminator)
