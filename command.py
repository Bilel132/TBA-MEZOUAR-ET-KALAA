"""Module contenant la classe Command pour gérer les commandes du jeu Naruto Adventure."""
class Command:
    """Représente une commande dans le jeu."""
    def __init__(self, command_word, help_string, action, number_of_parameters):
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters

    def __str__(self):
        return f"{self.command_word} : {self.help_string}"
    def execute(self, game, args):
        """Exécute la commande avec les arguments fournis."""
        self.action(game, args, self.number_of_parameters)