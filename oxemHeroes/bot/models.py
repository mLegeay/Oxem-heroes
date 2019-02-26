from django.db import models


class MemberQuerySet(models.QuerySet):
    """Requête de base pour les membres."""

    def _get_member(self, discord_user):

        created = False
        try:
            Member.objects.get(discord_id=discord_user.id)
            if member.name != discord_user.name:
                member.name = discord_user.name
                member.save()
        except:
            member = Member.objects.create(discord_id=discord_user.id,
                                           name=name,
                                           discriminator=discriminator,
                                           joined_at=joined_at)
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
