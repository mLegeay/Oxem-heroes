PLAYER_COMMAND = [
    "choisir",
    "jeton",
    "recruter",
    "silver",
    "silvermax",
    "xp",
]

SKILL_LIST = [
    "aquillon",
    "justice",
    "pillage",
    "potion",
]

ADMIN_DONE = {
    'add_silver': "Vous avez attribué {} silver à {}.",
    'add_token': "Vous avez attribué {} jetons à {}.",
    'bonus_xp': "Le bonus est de {}%. Pour le retirer, !bonusxp 0",
}

ERRORS = {
    'command_dne': "La commande n'existe pas ...",
    'invalid_parameter_ga': "{} n'est pas une valeur valide, le nombre de gagnant doit être strictement supérieur à 0",
    'no_giveaway': "Pas de giveaway en cours",
    'no_participant': "Il n'y a pas de participants au giveaway ...",
    'not_enough_participants': "Il n'y a pas assez de participants par rapport aux nombre de gagnants choisi",
    'player_dne': "Ce joueur n'existe pas",
}

HELP_MESSAGE = {
    'start': "Liste des commandes :\n```Commandes générales :\n",
    'classe': "\nCommandes de classe :\n",
    'end': "```\n Utiliser !help <command> ou !aide <command> pour avoir plus de détails.",
}

GIVEAWAY = {
    'success': "Giveaway créé avec succès",
    'winner': "Le gagnant est : {} ! Bravo à lui/elle !",
    'winners': "Les gagnants sont : {} ! Bravo à eux !"
}
