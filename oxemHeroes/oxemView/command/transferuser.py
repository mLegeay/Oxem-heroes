from oxemHeroes.classe.models import Classe
from oxemHeroes.command.models import Command
from oxemHeroes.commandHistory.models import CommandHistory
from oxemHeroes.game.models import Game
from oxemHeroes.gameMember.models import GameMember
from oxemHeroes.giveAway.models import Giveaway
from oxemHeroes.member.models import Member

from oxemHeroes.bot.models import CommandHistory as old_CH
from oxemHeroes.bot.models import Game as old_Game
from oxemHeroes.bot.models import GameMember as old_GM
from oxemHeroes.bot.models import Member as old_Member

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Commande de transfert des données de l'ancienne base à la nouvelle."""

    help = "Transfère user."

    def handle(self, *args, **options):
        """Fonctionnement de la commande."""

        commandHistory = old_CH.objects.all()
        game = old_Game.objects.all()
        gameMember = old_GM.objects.all()
        member = old_Member.objects.all()

        for each in commandHistory:
            CommandHistory.objects.create(member=each.member,
                                          command=each.command,
                                          last_used=each.last_used,
                                          bonus=each.bonus)

        for each in game:
            Game.objects.create(silver=each.silver, bonus_xp=each.bonus_xp)

        for each in gameMember:
            GameMember.objects.create(member=each.member,
                                      classe=each.classe,
                                      joined_at=each.joined_at,
                                      experience=each.experience,
                                      silver=each.silver,
                                      token=each.token,)

        for each in member:
            Member.objects.create(discord_id=each.discord_id,
                                  name=each.name,
                                  joined_at=each.joined_at,
                                  discriminator=each.discriminator)
