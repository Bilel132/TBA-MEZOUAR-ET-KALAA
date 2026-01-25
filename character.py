import random

class Character:
    def __init__(self, name, description, room, msgs):
        self.name = name
        self.description = description
        self.current_room = room
        self.msgs = msgs
        self.index = 0
        room.characters[self.name] = self  # Ajout automatique dans la salle

    def get_msg(self):
        """Retourne le message suivant cycliquement"""
        msg = self.msgs[self.index]
        self.index = (self.index + 1) % len(self.msgs)
        return msg

    def move(self):
        """Se déplace aléatoirement dans une salle adjacente (50% de chance)"""
        if not self.current_room.exits:
            return False
        if random.choice([True, False]):
            next_room = random.choice(list(self.current_room.exits.values()))
            del self.current_room.characters[self.name]
            self.current_room = next_room
            self.current_room.characters[self.name] = self
            return True
        return False
