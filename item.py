class Item:
    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"


# Objets spéciaux

class Beamer(Item):
    def __init__(self, name="beamer", description="Téléporteur vers une salle mémorisée", weight=1):
        super().__init__(name, description, weight)
        self.saved_room = None

    def charge(self, player):
        self.saved_room = player.current_room
        print(f"Salle mémorisée : {self.saved_room.name}")

    def fire(self, player):
        if self.saved_room:
            player.current_room = self.saved_room
            print(f"Téléporté vers {self.saved_room.name}")
        else:
            print("Aucune salle mémorisée.")


class Potion(Item):
    def __init__(self, name="potion", description="Restaure des points de vie", weight=0.3, heal=50):
        super().__init__(name, description, weight)
        self.heal = heal

    def use(self, player):
        player.health = min(player.health + self.heal, 100)
        print(f"Tu récupères {self.heal} PV. Santé actuelle : {player.health}")


class Scroll(Item):
    def __init__(self, name="parchemin", description="Contient des informations secrètes", weight=0.2, content=""):
        super().__init__(name, description, weight)
        self.content = content

    def read(self):
        print(f"Lecture du parchemin : {self.content}")


class Map(Item):
    def __init__(self, name="carte", description="Permet de se repérer sur la map", weight=0.2):
        super().__init__(name, description, weight)

    def show_map(self, game):
        print("Carte des villages :")
        for room in game.rooms:
            print(f" - {room.name}")


class Key(Item):
    def __init__(self, name="clé", description="Permet d'ouvrir une porte verrouillée", weight=0.1):
        super().__init__(name, description, weight)


class Torch(Item):
    def __init__(self, name="torche", description="Éclaire une pièce sombre", weight=0.5):
        super().__init__(name, description, weight)