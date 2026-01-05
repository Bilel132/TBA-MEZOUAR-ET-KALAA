from room import Room
import random

class Character:
    """
    Classe pour les personnages non joueurs (PNJ).

    Attributes:
        name (str) : nom du personnage
        description (str) : description du personnage
        current_room (Room) : salle où se trouve le personnage
        msgs (list[str]) : messages que le PNJ peut dire
    """
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs.copy()  # copie pour garder l'original
        self.msg_index = 0       # pour faire parler cycliquement le PNJ

    def __str__(self):
        return f"{self.name} : {self.description}"

    def get_msg(self):
        """Retourne le message suivant du PNJ cycliquement."""
        if not self.msgs:
            return "..."
        msg = self.msgs[self.msg_index]
        self.msg_index = (self.msg_index + 1) % len(self.msgs)
        return msg

    def move(self):
        """Déplace le PNJ aléatoirement dans une pièce adjacente, 50% de chances."""
        if not self.current_room.exits:
            return False
        if random.choice([True, False]):  # 50% de chances de bouger
            possible_rooms = [room for room in self.current_room.exits.values() if room]
            if possible_rooms:
                self.current_room.characters.remove(self)
                self.current_room = random.choice(possible_rooms)
                self.current_room.characters.append(self)
                return True
        return False
