# bonus = 5%  des personnes en statut en ligne sur le serveur
# comp_success = message à afficher après utilisation de la compétence
OXEM = {
    'bonus': 0.05,
    'comp_success': "{} déploie la puissance de la lumière pour purger ses ennemis 【 {} XP 】 【 {} Silver 】",
}

# crit = 20%  de chance d'effectuer un critique
# comp_success = message à afficher après utilisation de la compétence
SHOSIZUKE = {
    'crit': 0.20,
    'comp_success': "{} massacre ses ennemis en une unique attaque dévastatrice {} 【 {} XP 】 【 {} Silver 】",
}

# fail_rate = taux d'echec de la compétence
# min_bonus = minimum pour le bonus en cas de réussite
# max_bonus = maximum pour le bonus en cas de réussite
# comp_success = message à afficher après la réussite du pillage
# comp_failed = message à afficher après l'echec du pillage
TALKORAN = {
    'fail_rate': 0.067,
    'min_bonus': 0,
    'max_bonus': 5,
    'comp_success': ("{} après avoir pillé un village sans défense, " +
                     "allume un feu et fait cuire des merguez-chipolatas 【 {} XP 】 【 {} Silver 】"),
    'comp_failed': ("{} s'est fait repousser par la milice locale" +
                    "qui avait anticipée son attaque sur le village ▶️ Perte du bonus 【 {} XP 】 【 {} Silver 】")
}

TYPUS = {
    'comp_success': "{} invoque des potions de sagesse pour le groupe 【 {} XP 】 【 {} Silver 】",
}

# non_authorized = message à afficher quand la compétence ne correspond pas à sa classe
# on_cd = message à afficher quand la compétence est encore en cooldown
ERRORS = {
    'non_authorized': "Vous n'avez pas le droit d'utiliser cette commande, pas touche !",
    'on_cd': "Vous pourrez utiliser la commande dans {}mn",
}
