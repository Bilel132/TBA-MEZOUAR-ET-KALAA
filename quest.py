"""Gestion des quêtes du jeu."""
class Quest:
    """Représente une quête avec des objectifs et des récompenses."""
    def __init__(self, name, desc, objectives, rewards):
        """Initialise une quête."""
        self.name = name
        self.description = desc
        self.objectives = objectives
        self.rewards = rewards
        self.active = False
        self.completed = False

    def activate(self):
        """Active la quête."""
        self.active = True

    def complete(self, obj):
        """Valide un objectif de la quête."""
        if obj in self.objectives:
            self.objectives.remove(obj)
        if not self.objectives:
            self.completed = True
            print(f"🏆 Quête terminée : {self.name}")


class QuestManager:
    """Gère l'ensemble des quêtes du jeu."""
    def __init__(self):
        """Initialise le gestionnaire de quêtes."""
        self.quests = []

    def add_quest(self, quest):
        """Ajoute une quête au gestionnaire."""
        self.quests.append(quest)

    def check_quests(self, _game, action, target):
        """Vérifie la progression des quêtes actives."""
        key = f"{action}:{target}"
        for q in self.quests:
            if q.active and not q.completed:
                q.complete(key)

    def is_completed(self):
        """Retourne True si toutes les quêtes sont terminées."""
        return all(q.completed for q in self.quests)