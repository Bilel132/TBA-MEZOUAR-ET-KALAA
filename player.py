# Define the Player class.
class Player():
    """ Cette classe représente le joueur dans le jeu.

    Attributes :
        name (str) : name of the player
        current_room (Room) : the room where the player is

    Methods : 
        __init__(self, name) : The constructor.
        move(self, direction) : it moves the player to the place we chose.

    Examples : 
    >>> from room import Room
    >>> forest = Room("Forest", "une forêt enchantée")
    >>> cave = Room("Cave", "une grotte sombre")
    >>> forest.exits = {"N": cave}
    >>> cave.exits = {"S": forest}
    >>> p = Player("Alice")
    >>> p.current_room = forest
    >>> p.current_room.name
    'Forest'
    >>> p.move("N")
    True
    >>> p.current_room.name
    'Cave'
    >>> p.move("E")
    False


"""
    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []          # Historique des salles visitées
        self.inventory = {}        # Inventaire du joueur : name -> Item
        self.max_weight = 10       # Poids max transportable

    
    # Define the move method.
    def move(self, direction):
        if not self.current_room:
            print("Vous n'êtes dans aucune salle !")
            return False
            
        self.history.append(self.current_room)

        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits(direction)

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        print(self.get_history())
        return True
    
    def get_history(self):
        if not self.history:
            return "Vous n'avez encore visité aucune pièce."
        s = "Vous avez déjà visité les pièces suivantes:\n"
        for room in self.history:
            s += f"    - {room.description}\n"
        return s

    
    def get_inventory(self):
        if not self.inventory:
            return "Votre inventaire est vide."
        s = "Vous disposez des items suivants:\n"
        for item in self.inventory.values():
            s += f"    - {item}\n"
        return s

        
        

    