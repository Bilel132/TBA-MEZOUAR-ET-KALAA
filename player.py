"""Gestion du joueur du jeu."""
class Player:
    """Représente le joueur et son état dans le jeu."""
    def __init__(self, name):
        """Initialise un joueur avec un nom."""
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.max_weight = 10

    def current_weight(self):
        """Retourne le poids total des objets transportés."""
        return sum(i.weight for i in self.inventory.values())

    def get_inventory(self):
        """Retourne une description textuelle de l'inventaire."""
        if not self.inventory:
            return "Inventaire vide"
        items = [f" - {i}" for i in self.inventory.values()]
        return "🎒 Inventaire:\n" + "\n".join(items)

    def get_history(self):
        """Retourne l'historique des salles visitées."""
        return " → ".join(r.name for r in self.history) if self.history else "Vide"
