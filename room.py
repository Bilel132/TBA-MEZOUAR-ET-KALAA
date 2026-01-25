class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}

    def set_exit(self, direction, room):
        self.exits[direction] = room

    def get_exit(self, direction):
        return self.exits.get(direction)

    def get_long_description(self):
        txt = f"\n📍 {self.name} — {self.description}\n"
        txt += "Sorties: " + ", ".join(self.exits.keys()) + "\n"

        if self.inventory:
            txt += "\nObjets:\n"
            for i in self.inventory.values():
                txt += f" - {i}\n"

        if self.characters:
            txt += "\nPNJ:\n"
            for c in self.characters.values():
                txt += f" - {c.name}\n"

        return txt
