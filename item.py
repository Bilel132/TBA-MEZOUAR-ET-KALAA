# pylint= disable=too-few-public-methods
"""Gestion des objets du jeu, y compris la carte et autres items."""
class Item:
    """Classe de base pour tous les objets du jeu."""
    def __init__(self, name, description, weight):
        """Initialise un objet avec un nom, une description et un poids."""
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        """Retourne une description textuelle de l'objet."""
        return f"{self.name} : {self.description} ({self.weight} kg)"


# ------------------ CARTE ------------------
class Map(Item):
    """Carte permettant de visualiser les villages/salles."""
    def __init__(self, name="carte", description="Carte du monde ninja", weight=0.2):
        super().__init__(name, description, weight)

    def use(self, _player, game):
        """Affiche la carte et les quêtes actives du jeu."""
        print("🗺️ Voici la carte !")
        # Affiche la carte en GUI
        if game.game_gui:
            game.game_gui.show_map()
        # Affiche aussi les quêtes actives
        print("\n📜 Quêtes actives :")
        for q in game.quest_manager.quests:
            if q.active and not q.completed:
                print(f" - {q.name}")
                