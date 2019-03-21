"""Ajout de display au module Admin de Django."""

from django.contrib import admin
from oxemHeroes.classe.models import Classe
from oxemHeroes.command.models import Command
from oxemHeroes.commandHistory.models import CommandHistory
from oxemHeroes.game.models import Game
from oxemHeroes.gameMember.models import GameMember
from oxemHeroes.giveAway.models import Giveaway
from oxemHeroes.member.models import Member


class ClasseAdmin(admin.ModelAdmin):
    """Gère l'affichage des classe sur django-admin."""

    list_display = ('name', 'xp_comp', 'min_silver_comp',
                    'max_silver_comp', 'cd_comp')
    list_filter = ('name',)
    search_fields = ('name',)


class CommandAdmin(admin.ModelAdmin):
    """Gère l'affichage des commandes sur django-admin."""

    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name',)


class CommandHistoryAdmin(admin.ModelAdmin):
    """Gère l'affichage de l'historique de commande sur django-admin."""

    list_display = ('member', 'command', 'last_used', 'bonus')
    list_filter = ('command',)
    search_fields = ('member__name',)


class GameAdmin(admin.ModelAdmin):
    """Gère l'affichage du jeu sur django-admin."""

    list_display = ('silver', 'bonus_xp')


class GameMemberAdmin(admin.ModelAdmin):
    """Gère l'affichage des joueurs sur django-admin."""

    list_display = ('member', 'classe', 'joined_at',
                    'experience', 'silver', 'token')
    list_filter = ('classe',)
    search_fields = ('member__name',)


class GiveawayAdmin(admin.ModelAdmin):
    """Gère l'affichage du giveaway sur django-admin."""

    list_display = ('participants',)


class MemberAdmin(admin.ModelAdmin):
    """Gère l'affichage des membres sur django-admin."""

    list_display = ('name', 'discriminator', 'discord_id', 'joined_at')
    search_fields = ('name', 'discord_id',)


admin.site.register(Classe, ClasseAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(CommandHistory, CommandHistoryAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameMember, GameMemberAdmin)
admin.site.register(Giveaway, GiveawayAdmin)
admin.site.register(Member, MemberAdmin)
