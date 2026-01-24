class Quest:
    """Classe représentant une quête dans le jeu."""
    def __init__(self, name, description, objectives, rewards):
        self.name = name
        self.description = description
        self.objectives = objectives  # liste d'objectifs, ex : ["reach:Konoha"]
        self.rewards = rewards        # liste de récompenses
        self.completed = False
        self.active = False

    def activate(self):
        self.active = True

    def complete_objective(self, obj):
        if obj in self.objectives:
            self.objectives.remove(obj)
        if not self.objectives:
            self.completed = True

    def is_completed(self):
        return self.completed


class QuestManager:
    """Gère toutes les quêtes du jeu."""
    def __init__(self):
        self.quests = []

    def add_quest(self, quest):
        self.quests.append(quest)

    def activate_quest(self, quest_name):
        for quest in self.quests:
            if quest.name == quest_name:
                quest.activate()

    def check_objective(self, obj):
        for quest in self.quests:
            if quest.active:
                quest.complete_objective(obj)

    def check_quests(self, game, action_type, target):
        """
        Méthode pour correspondre aux appels d'actions.py.
        Exemples d'action_type : "move", "item", "talk"
        target : nom de salle, item ou PNJ
        """
        obj_string = f"{action_type}:{target}"
        for quest in self.quests:
            if quest.active:
                if obj_string in quest.objectives:
                    quest.complete_objective(obj_string)

    def is_completed(self):
        return all(quest.completed for quest in self.quests)

    def list_quests(self):
        for quest in self.quests:
            status = "MISSION ACCOMPLIE" if quest.completed else "MISSION ECHOUE"
            print(f"{quest.name} - {status}: {quest.description}")
