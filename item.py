# item.py

class Item:
    """Classe de base pour tous les objets du jeu."""
    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"

# ------------------ BEAMER ------------------
class Beamer(Item):
    """Téléporteur vers une salle mémorisée."""
    def __init__(self, name="beamer", description="Téléporteur vers une salle mémorisée", weight=1):
        super().__init__(name, description, weight)
        self.saved_room = None

    def charge(self, player):
        """Mémoriser la salle actuelle du joueur."""
        self.saved_room = player.current_room
        print(f"Salle mémorisée : {self.saved_room.name}")

    def fire(self, player):
        """Téléporter le joueur vers la salle mémorisée."""
        if self.saved_room:
            player.current_room = self.saved_room
            print(f"Téléporté vers {self.saved_room.name}")
        else:
            print("Aucune salle mémorisée.")

# ------------------ POTION ------------------
class Potion(Item):
    """Potion qui restaure des points de vie."""
    def __init__(self, name="potion", description="Restaure des points de vie", weight=0.3, heal=50):
        super().__init__(name, description, weight)
        self.heal = heal

    def use(self, player, game=None):
        """Utiliser la potion pour restaurer la santé du joueur."""
        player.health = min(player.health + self.heal, 100)
        print(f"Tu récupères {self.heal} PV. Santé actuelle : {player.health}")

# ------------------ PARCHEMIN ------------------
class Scroll(Item):
    """Parchemin contenant des informations secrètes."""
    def __init__(self, name="parchemin", description="Contient des informations secrètes", weight=0.2, content=""):
        super().__init__(name, description, weight)
        self.content = content

    def use(self, player, game=None):
        """Lire le parchemin."""
        print(f"Lecture du parchemin : {self.content}")

# ------------------ CARTE ------------------
class Map(Item):
    """Carte permettant de visualiser les villages/salles."""
    def __init__(self, name="carte", description="Permet de se repérer sur la map", weight=0.2):
        super().__init__(name, description, weight)

    def use(self, player, game):
        """Afficher la carte des villages/salles disponibles."""
        print("Carte des villages :")
        for room in game.rooms:
            print(f" - {room.name}")

# ------------------ CLE ------------------
class Key(Item):
    """Clé permettant d'ouvrir une porte verrouillée."""
    def __init__(self, name="clé", description="Permet d'ouvrir une porte verrouillée", weight=0.1):
        super().__init__(name, description, weight)
