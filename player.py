class Player:
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.max_weight = 10

    def current_weight(self):
        return sum(i.weight for i in self.inventory.values())

    def get_inventory(self):
        if not self.inventory:
            return "Inventaire vide"
        txt = "🎒 Inventaire:\n"
        for i in self.inventory.values():
            txt += f" - {i}\n"
        return txt

    def get_history(self):
        return " → ".join(r.name for r in self.history) if self.history else "Vide"
