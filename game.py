# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        self.commands["history"] = Command("history", " : affiche l'historique des salles visitées", Actions.history, 0)
        self.commands["back"] = Command("back", " : revenir à la salle précédente", Actions.back, 0)
    


        
        # Setup rooms

        konoha = Room("Konohagakure","dans le village caché de la Feuille, entouré d'arbres et de ninjas en entraînement.")
        self.rooms.append(konoha)
        suna = Room("Sunagakure","dans le village du Sable, balayé par un vent brûlant.")
        self.rooms.append(suna)
        kiri = Room("Kirigakure","dans le village de la Brume, noyé dans un brouillard permanent.")
        self.rooms.append(kiri)
        iwa = Room("Iwagakure", "dans le village de la Roche, entouré de montagnes massives.")
        self.rooms.append(iwa)
        kusa = Room("Kusagakure","dans le village de l'Herbe, où les champs ondulent sous la brise.")
        self.rooms.append(kusa)
        kumo = Room("Kumogakure","dans le village des Nuages, haut perché dans les montagnes.")
        self.rooms.append(kumo)
        oto = Room("Otogakure","dans le village du Son, rempli de sons étranges.")
        self.rooms.append(oto)
        akatsuki = Room("QG Akatsuki","dans le repaire secret de l'Akatsuki, une grotte ornée de nuages rouges.")
        self.rooms.append(akatsuki)
        hokage = Room("Bureau du Hokage","dans le bureau circulaire du Hokage, rempli de rouleaux confidentiels.")
        self.rooms.append(hokage)
        kiri_prison = Room("Prison de Kirigakure","dans un sous-sol humide où résonnent des gouttes sinistres.")
        self.rooms.append(kiri_prison)
        gedo = Room("Salle du Gedo Mazo","devant la statue démoniaque géante, source d'énergie sinistre.")
        self.rooms.append(gedo)
        suna_archive = Room("Archives de Sunagakure","dans une salle remplie de parchemins anciens et secrets.")
        self.rooms.append(suna_archive)

 

        # Create exits for rooms

        konoha.exits = {"N": None,"E": suna,"S": iwa, "O": None,"UP": hokage,"DOWN": None}
        suna.exits = {"N": None,"E": kiri,"S": None,"O": konoha,"UP": suna_archive,"DOWN": None}
        kiri.exits = {"N": None,"E": None,"S": kusa,"O": suna,"UP": None,"DOWN": kiri_prison}
        iwa.exits = {"N": konoha,"E": akatsuki,"S": None,"O": None,"UP": None,"DOWN": None}
        kusa.exits = {"N": kiri,"E": kumo,"S": None,"O": None,"UP": None,"DOWN": None}
        kumo.exits = {"N": None,"E": None,"S": None,"O": oto,"UP": None,"DOWN": None}
        oto.exits = {"N": None,"E": kumo,"S": None,"O": akatsuki,"UP": None,"DOWN": None}
        akatsuki.exits = {"N": None,"E": oto,"S": None,"O": iwa,"UP": None,"DOWN": gedo}
        hokage.exits = {"UP": None, "DOWN": konoha}
        kiri_prison.exits = {"UP": kiri, "DOWN": None}
        gedo.exits = {"UP": akatsuki, "DOWN": None}
        suna_archive.exits = {"UP": None, "DOWN": suna}




        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = konoha

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
    
    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        # Si la commande est vide on ne fait rien
        if command_string.strip() == "":
            return
        
        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
