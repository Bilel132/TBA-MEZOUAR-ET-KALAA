# ------------------ COMMAND ------------------
"""
Fichier : command.py
Description : Définit la classe Command pour représenter une commande du jeu.
"""

class Command:
    """
    Cette classe représente une commande. Une commande est composée d'un mot-clé, d'une aide,
    d'une action à exécuter et du nombre de paramètres attendus.

    Attributes:
        command_word (str): Le mot de la commande.
        help_string (str): La chaîne d'aide affichée pour la commande.
        action (function): La fonction à exécuter lors de l'appel de la commande.
        number_of_parameters (int): Le nombre de paramètres attendus.

    Methods:
        __init__(self, command_word, help_string, action, number_of_parameters): Constructeur.
        __str__(self): Représentation textuelle de la commande.
    """

    def __init__(self, command_word, help_string, action, number_of_parameters):
        """
        Initialise une nouvelle commande.

        Args:
            command_word (str): mot de la commande
            help_string (str): description de la commande
            action (function): fonction à exécuter
            number_of_parameters (int): nombre de paramètres attendus
        """
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters

    def __str__(self):
        """
        Retourne une représentation textuelle de la commande.
        Exemple : "go : Permet de se déplacer dans une direction."
        """
        return f"{self.command_word} : {self.help_string}"
