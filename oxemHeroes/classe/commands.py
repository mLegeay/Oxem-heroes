
class CrmNotificationProcessor(object):
    """Traite les notifications reçues par le crm.
    """

    def __init__(self):
        force = False
        success = True
        experience = gameMember.classe.xp_comp
        silver = randint(gameMember.classe.min_silver_comp, gameMember.classe.max_silver_comp)

        if command_name == "aquillon" and gameMember.classe.name == "shosizuke":
            message, force, silver, bonus = self.aquillon(force, silver)

        elif command_name == "justice" and gameMember.classe.name == "oxem":
            message = self.justice(send_message)

        elif command_name == "pillage" and gameMember.classe.name == "talkoran":
            message = self.pillage(success)

        else:
            message = ERRORS['non_authorized']
            return message

        return self.can_use(message)

    def aquillon(self):
        """."""
        is_crit = ''

        if CommandHistory.objects.get_bonus(command_name, send_message) != 0:
            force = True

        if SHOSIZUKE['crit'] >= random():
            bonus = 1
            is_crit = ' ▶️ CRITIQUE '
            silver *= 2
        else:
            bonus = -1

        message = SHOSIZUKE['comp_success'].format(gameMember.member.name, is_crit, experience, silver)

        return message, force, silver, bonus

    def justice(self, send_message):
        """."""

        member_list = send_message.channel.members

        bonus = int(len(list(filter(lambda connected: connected.status == discord.Status.online,
                                    member_list))) * OXEM['bonus'])
        experience += bonus
        message = OXEM['comp_success'].format(gameMember.member.name, experience, silver)

        return message

    def pillage(self):
        """."""

        success = False if TALKORAN['fail_rate'] >= random() else True

        if success:
            bonus = randint(TALKORAN['min_bonus'], TALKORAN['max_bonus'])

        else:
            bonus = -1
            message = TALKORAN['comp_failed'].format(
                gameMember.member.name, experience, silver)

    def can_use(self, message):
        """."""

        can_use = CommandHistory.objects.check_cooldown(command_name, send_message, gameMember.classe.cd_comp, force)

        if can_use is True:
            experience = gameMember.add_experience(experience)

            if command_name == "pillage" and success:
                silver += CommandHistory.objects.update_bonus(command_name, send_message, bonus)
                message = TALKORAN['comp_success'].format(gameMember.member.name, experience, silver)

            if command_name == "aquillon":
                CommandHistory.objects.update_bonus(command_name, send_message, bonus)

            gameMember.add_silver(silver)

        else:
            message = ERRORS['on_cd'].format(int(gameMember.classe.cd_comp - can_use))

        return message
