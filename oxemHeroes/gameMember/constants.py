# Xp requis pour passer au niveau suivant
XP_REQUIRE = {
    1: 100,
    2: 230,
    3: 400,
    4: 580,
    5: 800,
    6: 1000,
    7: 1300,
    8: 1500,
    9: 1800,
    10: 2000,
    11: 2200,
    12: 2500,
    13: 2680,
    14: 3000,
    15: 3400,
    16: 3800,
    17: 4000,
    18: 4500,
    19: 5000,
    20: 5800,
    21: 6500,
    22: 7000,
    23: 7600,
    24: 8000,
    25: 8800,
    26: 10000,
    27: 11000,
    28: 12200,
    29: 14000,
    30: 16000,
    31: 17800,
    32: 19000,
    33: 20000,
    34: 23000,
    35: 25000,
    36: 28000,
    37: 30000,
    38: 32000,
    39: 35000,
    40: 39000,
    41: 45000,
    42: 52000,
    43: 55000,
    44: 59000,
    45: 65000,
    46: 76000,
    47: 80000,
    48: 84000,
    49: 100000,
    50: 120000,
    51: 140000,
    52: 180000,
    53: 220000,
    54: 260000,
    55: 300000,
    56: 350000,
    57: 400000,
    58: 450000,
    59: 500000
}

# Titre correspondant au niveau
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

# Liste des héros jouables
FREE_HERO_LIST = [
    "oxem",
    "shosizuke",
    "talkoran",
]

# Liste des héros jouables
HERO_LIST = [
    "oxem",
    "shosizuke",
    "talkoran",
    "lord_typus",
]

# choisir : message de choix de héros
# recruter : message de recrutement de héros
# silver_user : message affichant les silvers du joueur
# silver_user_max : message affichant les silvers cumulés du joueur
# token_user : message affichant les jetons du joueur
# xp : message affichant l'xp du joueur
DONE = {
    'choisir': "Vous jouez désormais le héros {} !",
    'recruter': "Vous venez d'acheter le héros {} !",
    'silver_user': "Tu possèdes actuellement {} Silver !",
    'silver_user_max': "Tu as récolté {} Silver !",
    'token_user': "Tu possèdes {} jetons.",
    'xp': "【 {} 】 Niveau {} » {} XP",
}

# already_hero : l'utilisateur a indiqué un héros qu'il joue déjà
# hero_dne : l'utilisateur a indiqué un héros qui n'existe pas
# not_enough_silver : l'utilisateur ne possède pas assez de silvers
# not_enough_token : l'utilisateur ne possède pas assez de jetons
# not_own : l'utilisateur ne possède pas le héros
ERRORS = {
    'already_hero': "Vous jouez déjà ce héros.",
    'hero_dne': "Ce héros n'existe pas.",
    'not_enough_silver': "Tu n'as pas assez de silver pour acheter ce héros.",
    'not_enough_token': "Tu n'as pas assez de jeton pour changer de héros.",
    'not_own': "Tu ne possède pas ce héros (!acheter).",
}
