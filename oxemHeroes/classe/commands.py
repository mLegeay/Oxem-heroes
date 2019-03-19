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
from oxemHeroes.classe.constants import ERRORS, OXEM, SHOSIZUKE, TALKORAN
from oxemHeroes.commandHistory.models import CommandHistory


class Commands(object):
    """Traite les commandes reçus pour les classes."""

    def __init__(self, command_name, gameMember, _message):
        """Initialise les valeurs de la classe.

           variables :
           - Integer bonus : le bonus correspond à un critique pour Aquillon et à un bonus en silver pour Pillage
           - Integer experience : l'expérience acquis
           - Integer silver : la quantité de silver récolté grâce à la compétence
           - String message : message a renvoyé à l'utilisateur (ne pas confondre self.message et _message)
           - Boolean force : permet de forcer l'utilisation de la commande sans CD
           - Boolean success : compétence de talkoran, permet de vérifier si son bonus retourne à 0 ou augmente
           - GameMember gameMember : le membre ayant effectué la commande de compétence

           parameters:
           - String command_name : nom de la commande utilisée
           - String _message : message contenant la commande
           - GameMember gameMember : le membre ayant effectué la commande de compétence

           return:
           - String message : message a renvoyé à l'utilisateur (ne pas confondre self.message et _message)
        """
        force = False
        success = True
        bonus = None

        self.gameMember = gameMember

        self.experience = self.gameMember.classe.xp_comp
        self.silver = randint(self.gameMember.classe.min_silver_comp, self.gameMember.classe.max_silver_comp)

        if command_name == "aquillon" and self.gameMember.classe.name == "shosizuke":
            force, bonus = self.aquillon(force, _message, command_name)

        elif command_name == "justice" and self.gameMember.classe.name == "oxem":
            self.justice(_message)

        elif command_name == "pillage" and self.gameMember.classe.name == "talkoran":
            bonus, success = self.pillage(success)

        else:
            self.message = ERRORS['non_authorized']
            return self.message

        self.can_use(bonus, _message, force, success, command_name)

        return self.message

    def aquillon(self, force, _message, command_name):
        """."""
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
                                                        self.experience,
                                                        self.silver)

        return force, bonus

    def justice(self, _message):
        """."""

        member_list = _message.channel.members

        bonus = int(len(list(filter(lambda connected: connected.status == discord.Status.online,
                                    member_list))) * OXEM['bonus'])
        self.experience += bonus
        self.message = OXEM['comp_success'].format(self.gameMember.member.name, self.experience, self.silver)

    def pillage(self, success):
        """."""

        success = False if TALKORAN['fail_rate'] >= random() else True

        if success:
            bonus = randint(TALKORAN['min_bonus'], TALKORAN['max_bonus'])

        else:
            bonus = -1
            self.message = TALKORAN['comp_failed'].format(self.gameMember.member.name, self.experience, self.silver)

        return bonus, success

    def can_use(self, bonus, _message, force, success, command_name):
        """."""

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
