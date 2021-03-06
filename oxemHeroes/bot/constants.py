XP_REQUIRE = {
    100: 1,
    230: 2,
    400: 3,
    580: 4,
    800: 5,
    1000: 6,
    1300: 7,
    1500: 8,
    1800: 9,
    2000: 10,
    2200: 11,
    2500: 12,
    2680: 13,
    3000: 14,
    3400: 15,
    3800: 16,
    4000: 17,
    4500: 18,
    5000: 19,
    5800: 20,
    6500: 21,
    7000: 22,
    7600: 23,
    8000: 24,
    8800: 25,
    10000: 26,
    11000: 27,
    12200: 28,
    14000: 29,
    16000: 30,
    17800: 31,
    19000: 32,
    20000: 33,
    23000: 34,
    25000: 35,
    28000: 36,
    30000: 37,
    32000: 38,
    35000: 39,
    39000: 40,
    45000: 41,
    52000: 42,
    55000: 43,
    59000: 44,
    65000: 45,
    76000: 46,
    80000: 47,
    84000: 48,
    100000: 49,
    120000: 50,
    140000: 51,
    180000: 52,
    220000: 53,
    260000: 54,
    300000: 55,
    350000: 56,
    400000: 57,
    450000: 58,
    500000: 59
}

LEVEL_LIST = {
    1: "Nouveau",
    2: "Débutant",
    3: "Novice",
    4: "Recrue",
    5: "Soldat",
    6: "Apprenti Héros",
    7: "Jeune Explorateur",
    8: "Aventurier maladroit",
    9: "Dompteur d'Ours",
    10: "Protecteur",
    11: "Banquier",
    12: "Apprenti Magicien",
    13: "Archiviste",
    14: "Vagabond Solitaire",
    15: "Rôdeur du Gondor",
    16: "Guerrier",
    17: "Aventurier",
    18: "Chasseur de Prime",
    19: "Chevalier Jedi",
    20: "Gardien de la Regalia",
    21: "Super Soldat",
    22: "Héros de Shonen",
    23: "Perfectionniste",
    24: "Rêveur",
    25: "Collectionneur",
    26: "Chercheur",
    27: "Invocateur",
    28: "Commandant",
    29: "Elite",
    30: "Héros",
    31: "Gamer",
    32: "Super Gamer",
    33: "Jeune Prince",
    34: "Super Héros",
    35: "Avengers",
    36: "Chasseur de Dragon",
    37: "Conquérant",
    38: "Enfant de Dragon",
    39: "Leader",
    40: "Space Marines",
    41: "Gardien de la Galaxie",
    42: "Chasseur d'étoile",
    43: "Baron",
    44: "Sultan",
    45: "Monarque",
    46: "Invincible",
    47: "Destructeur",
    48: "Tueur de Dragon",
    49: "Parangon",
    50: "Légende",
    51: "Seigneur Sith",
    52: "Christ Cosmique",
    53: "Archange",
    54: "Démon primordial",
    55: "Seigneur des Enfers",
    56: "Sauveur",
    57: "Farmeur Chinois",
    58: "Forgeur d'étoile",
    59: "Hardcore Gamer",
    60: "Grand Amiral de la Regalia",
}

COMMAND_LIST = [
    "choisir",
    "contribution",
    "jeton",
    "silver",
    "xp",
    "addjeton",
    "addsilver",
    "bonusxp",
    "participer",
    "aquillon",
    "justice",
    "pillage",
    "giveaway",
    "participer",
]

PLAYER_COMMAND = [
    "choisir",
    "contribution",
    "jeton",
    "silver",
    "xp",
]

SKILL_LIST = [
    "aquillon",
    "justice",
    "pillage",
]

ADMIN_COMMAND_LIST = [
    "addjeton",
    "addsilver",
    "bonusxp",
    "giveaway",
]

HERO_LIST = [
    "oxem",
    "shosizuke",
    "talkoran",
]

OXEM = {
    'bonus': 0.05,
    'comp_success': "{} déploie la puissance de la lumière pour purger ses ennemis 【 {} XP 】 【 {} Silver 】",
}

SHOSIZUKE = {
    'crit': 0.20,
    'comp_success': "{} massacre ses ennemis en une unique attaque dévastatrice {} 【 {} XP 】 【 {} Silver 】",
}

TALKORAN = {
    'fail_rate': 0.067,
    'min_bonus': 0,
    'max_bonus': 5,
    'comp_success': ("{} après avoir pillé un village sans défense, " +
                     "allume un feu et fait cuire des merguez-chipolatas 【 {} XP 】 【 {} Silver 】"),
    'comp_failed': ("{} s'est fait repousser par la milice locale" +
                    "qui avait anticipée son attaque sur le village ▶️ Perte du bonus 【 {} XP 】 【 {} Silver 】")
}

ADMIN_DONE = {
    'add_silver': "Vous avez attribué {} silver à {}.",
    'add_token': "Vous avez attribué {} jetons à {}.",
    'bonus_xp': "Le bonus est de {}%. Pour le retirer, !bonusxp 0",
}

DONE = {
    'choisir': "Vous jouez désormais le héros {} !",
    'silver_global': "Nous disposons actuellement de {} Silver",
    'silver_user': "{} a récolté {} Silver pour la communauté !",
    'token_user': "Tu possèdes {} jetons.",
    'xp': "【 {} 】 Niveau {} » {} XP",
}

ERRORS = {
    'command_dne': "La commande n'existe pas ...",
    'deja_choisis': "Vous avez déjà choisi un héros.",
    'hero_dne': "Ce héros n'existe pas.",
    'non_authorized': "Vous n'avez pas le droit d'utiliser cette commande, pas touche !",
    'not_a_player': "Commencez par choisir un héros. (!choisir)",
    'on_cd': "Vous pourrez utiliser la commande dans {}mn",
    'player_dne': "Ce joueur n'existe pas",
}

HELP_COMMAND = ['help', 'aide']

HELP_MESSAGE = {
    'start': "Liste des commandes :\n```Commandes générales :\n",
    'classe': "\nCommandes de classe :\n",
    'end': "```\n Utiliser !help <command> ou !aide <command> pour avoir plus de détails.",
}
