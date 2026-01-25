class Quest:
    def __init__(self, name, desc, objectives, rewards):
        self.name = name
        self.description = desc
        self.objectives = objectives
        self.rewards = rewards
        self.active = False
        self.completed = False

    def activate(self):
        self.active = True

    def complete(self, obj):
        if obj in self.objectives:
            self.objectives.remove(obj)
        if not self.objectives:
            self.completed = True
            print(f"🏆 Quête terminée : {self.name}")


class QuestManager:
    def __init__(self):
        self.quests = []

    def add_quest(self, quest):
        self.quests.append(quest)

    def check_quests(self, game, action, target):
        key = f"{action}:{target}"
        for q in self.quests:
            if q.active and not q.completed:
                q.complete(key)

    def is_completed(self):
        return all(q.completed for q in self.quests)
