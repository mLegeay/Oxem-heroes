"""Fichier d'exceptions."""


class CommandError(Exception):
    """Exception levée quand la commande n'est pas renseigné correctement."""

    logging_message = "CommandError"

    def __init__(self, command):
        """Initialise les valeurs de l'exception."""
