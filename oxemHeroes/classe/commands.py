"""Commande pour les classes.

- Aquillon : Compétence de Shosizuke
    S'il effectue un critique (20%) il peut relancer sa compétence sans CoolDown de plus,
    cela double les silvers gagnés
- Justice : Compétence d'Oxem
    Gagne un bonus d'xp de 5% en fonction du nombre de joueurs en ligne
- Pillage : Compétence de Talkoran
    S'il réussie, il cumul un bonus sur ses silvers, s'il échoue le bonus retourne à 0
"""

import discord
from random import *
from oxemHeroes.classe.constants import ERRORS, OXEM, SHOSIZUKE, TALKORAN, TYPUS
from oxemHeroes.commandHistory.models import CommandHistory
from oxemHeroes.game.models import Game


class Commands(object):
    """Traite les commandes reçus pour les classes."""

    def __init__(self, gameMember):
        """Initialise les valeurs de la classe.

           variables :
           - Integer experience : l'expérience acquis
           - Integer silver : la quantité de silver récolté grâce à la compétence
           - GameMember gameMember : le membre ayant effectué la commande de compétence

           parameters:
           - GameMember gameMember : le membre ayant effectué la commande de compétence
        """

        self.gameMember = gameMember

        self.experience = self.gameMember.classe.xp_comp
        self.silver = randint(self.gameMember.classe.min_silver_comp, self.gameMember.classe.max_silver_comp)

    def process(self, command_name, _message):
        """Initialise les valeurs de la classe.

           variables :
           - Integer bonus : le bonus correspond à un critique pour Aquillon et à un bonus en silver pour Pillage
           - String message : message a renvoyé à l'utilisateur (ne pas confondre self.message et _message)
           - Boolean force : permet de forcer l'utilisation de la commande sans CD
           - Boolean success : compétence de talkoran, permet de vérifier si son bonus retourne à 0 ou augmente

           parameters:
           - String command_name : nom de la commande utilisée
           - String _message : message contenant la commande

           return:
           - String message : message a renvoyé à l'utilisateur (ne pas confondre self.message et _message)
        """

        force = False
        success = True
        bonus = None

        if command_name == "aquillon" and self.gameMember.classe.name == "shosizuke":
            force, bonus = self.aquillon(force, _message, command_name)

        elif command_name == "justice" and self.gameMember.classe.name == "oxem":
            self.justice(_message)

        elif command_name == "pillage" and self.gameMember.classe.name == "talkoran":
            bonus, success = self.pillage(success)

        elif command_name == "potion" and self.gameMember.classe.name == "lord_typus":
            self.potion()

        else:
            self.message = ERRORS['non_authorized']
            return self.message

        self.can_use(bonus, _message, force, success, command_name)

        return self.message

    def aquillon(self, force, _message, command_name):
        """Compétence de Shosizuke.

           Shosizuke a 20% de chance d'effectuer un critique.
           S'il effectue un critique, il peut réutiliser sa compétence sans cooldown.
           De plus en cas de critique les silvers obtenus sont doublés

           variables :
           - String is_crit : si la compétence est un crit, la valeur devient ' ▶️ CRITIQUE '
           ceci afin que le message de réussite informe l'utilisateur de ce critique.
           - Integer Bonus : si le bonus est égale à 1 c'est un critique sinon c'est un coup simple.
        """
        is_crit = ''

        if CommandHistory.objects.get_bonus(command_name, _message) != 0:
            force = True

        if SHOSIZUKE['crit'] >= random():
            bonus = 1
            is_crit = ' ▶️ CRITIQUE '
            self.silver *= 2
        else:
            bonus = -1

        self.message = SHOSIZUKE['comp_success'].format(self.gameMember.member.name,
                                                        is_crit,
                                                        int(self.experience * (1 + Game.objects.get_bonusxp() / 100)),
                                                        self.silver)

        return force, bonus

    def justice(self, _message):
        """Compétence d'Oxem.

           Oxem gagne un bonus à son xp représentant 5% des joueurs ayant le statut en ligne sur le serveur.

           variable:
           - Tuple member_list : liste des membres du serveur.
        """

        member_list = _message.channel.members

        bonus = int(len(list(filter(lambda connected: connected.status == discord.Status.online,
                                    member_list))) * OXEM['bonus'])
        self.experience += bonus
        self.message = OXEM['comp_success'].format(self.gameMember.member.name,
                                                   int(self.experience * (1 + Game.objects.get_bonusxp() / 100)),
                                                   self.silver)

    def pillage(self, success):
        """Compétence de Talkoran.

           Talkoran a 6% de chance d'échouer son pillage.
           S'il réussit le pillage il cumule un bonus allant de 0 à 20 sur ses silvers.
           Le bonus octroyé à chaque réussite va de 0 à 5.
           S'il échoue, le bonus retourne à 0.

           Bonus = -1 permet de réinitialiser la variable bonus

           variable:
           - Boolean success : Correspond à l'echec ou la réussite du pillage
        """

        success = False if TALKORAN['fail_rate'] >= random() else True

        if success:
            bonus = randint(TALKORAN['min_bonus'], TALKORAN['max_bonus'])

        else:
            bonus = -1
            self.message = TALKORAN['comp_failed'].format(self.gameMember.member.name,
                                                          int(self.experience * (1 +
                                                                                 Game.objects.get_bonusxp() / 100)),
                                                          self.silver)

        return bonus, success

    def potion(self):
        """Compétence de lord typus.

           Lord Typus active un bonus de 30% à l'xp globale
        """

        if Game.objects.get_bonusxp() == 0:
            Game.objects.alter_xp(30)

        self.message = TYPUS['comp_success'].format(self.gameMember.member.name,
                                                    int(self.experience * (1 + Game.objects.get_bonusxp() / 100)),
                                                    self.silver)

    def can_use(self, bonus, _message, force, success, command_name):
        """Vérifie si la commande de l'utilisateur peut être executé en fonction du cooldown."""

        can_use = CommandHistory.objects.check_cooldown(command_name,
                                                        _message,
                                                        self.gameMember.classe.cd_comp,
                                                        force)

        if can_use is True:
            experience = self.gameMember.add_experience(self.experience)

            if command_name == "pillage" and success:
                self.silver += CommandHistory.objects.update_bonus(command_name, _message, bonus)
                self.message = TALKORAN['comp_success'].format(self.gameMember.member.name, experience, self.silver)

            if command_name == "aquillon":
                CommandHistory.objects.update_bonus(command_name, _message, bonus)

            self.gameMember.add_silver(self.silver)

        else:
            self.message = ERRORS['on_cd'].format(int(self.gameMember.classe.cd_comp - can_use))
