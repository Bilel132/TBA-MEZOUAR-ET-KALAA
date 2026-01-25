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
        text = f"\n📍 {self.name} — {self.description}\n"
        text += f"Sorties: {', '.join(self.exits.keys())}\n"
        if self.inventory:
            text += "\nObjets:\n"
            for i in self.inventory.values():
                text += f" - {i}\n"
        if self.characters:
            text += "\nPNJ:\n"
            for c in self.characters.values():
                text += f" - {c.name} : {c.description}\n"
        return text
