"""Module contenant la classe Character pour les personnages du jeu Naruto Adventure."""
import random

class Character:
    """Représente un personnage dans le jeu Naruto Adventure."""
    def __init__(self, name, description, room, msgs):
        """Initialise un personnage."""
        self.name = name
        self.description = description
        self.current_room = room
        self.msgs = msgs
        self.index = 0
        room.characters[self.name] = self

    def get_msg(self):
        """Retourne un message du personnage de manière cyclique."""
        msg = self.msgs[self.index]
        self.index = (self.index + 1) % len(self.msgs)
        return msg

    def move(self):
        """Déplace le personnage aléatoirement vers une salle voisine."""

        if not self.current_room.exits:
            return False
        if random.choice([True, False]):
            next_room = random.choice(list(self.current_room.exits.values()))
            del self.current_room.characters[self.name]
            self.current_room = next_room
            self.current_room.characters[self.name] = self
            return True
        return False
    