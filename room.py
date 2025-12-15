# Define the Room class.

class Room:
    """

Cette classe représente les lieux dans le jeu. ce que j'ai ajouté

Attributes :
    name (str) : name of the room
    description (str) : description of the room
    exits (dict) : dictionary that contains all the maps to each rooms

Methods :
    __init__(self, name, description) : The constructor.
    get_exit(self, direction) : Return the room 
    get_exit_string(self) : returns a string listing all the availables get_exit_string
    get_long_description(self) : Returns a full desription of the room 

Examples :

>>> forest = Room("Forest", "dans une forêt enchantée")
>>> cave = Room("Cave", "dans une grotte sombre")
>>> forest.exits["N"] = cave
>>> cave.exits["S"] = forest
>>> from player import Player
>>> player = Player("Alice")
>>> player.current_room = forest
>>> player.current_room.name
'Forest'
>>> player.current_room.description
'dans une forêt enchantée'

"""


 # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        if not self.inventory:
            return "Il n'y a rien ici."
        s = "La pièce contient :\n"
        for item in self.inventory.values():
            s += f"    - {item}\n"
        return s
