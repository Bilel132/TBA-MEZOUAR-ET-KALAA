class Player:
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.max_weight = 10
        self.health = 100

    def move(self, direction):
        room = self.current_room.get_exit(direction)
        if not room:
            print("Pas de sortie dans cette direction.")
            return False
        
        self.history.append(self.current_room)
        self.current_room = room
        print(f"\nVous êtes maintenant dans {room.name}\n{room.get_long_description()}")
        return True

    def current_weight(self):
        return sum(i.weight for i in self.inventory.values())

    def get_inventory(self):
        if not self.inventory:
            return "Inventaire vide."
        
        txt = "Inventaire:\n"
        for i in self.inventory.values():
            txt += f" - {i}\n"
        txt += f"\nPoids: {self.current_weight()}/{self.max_weight} kg"
        return txt

    def get_history(self):
        if not self.history:
            return "Historique vide."
        return "Historique des salles: " + " -> ".join([r.name for r in self.history])
