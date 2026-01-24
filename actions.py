from item import Beamer, Potion, Scroll, Map

MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 paramètre.\n"

class Actions:

    def go(game, words, n):
        if len(words) != n + 1:
            print(MSG1.format(command_word=words[0]))
            return False
        
        directions = {
            "n":"N","nord":"N",
            "s":"S","sud":"S",
            "e":"E","est":"E",
            "o":"O","ouest":"O",
            "up":"UP","u":"UP",
            "down":"DOWN","d":"DOWN"
        }
        d = words[1].lower()
        if d not in directions:
            print("Direction invalide.")
            return False
        
        moved = game.player.move(directions[d])
        if moved:
            game.quest_manager.check_quests(game, "move", game.player.current_room.name)
        return True

    def look(game, words, n):
        print(game.player.current_room.get_long_description())
        return True

    def quit(game, words, n):
        print("\nMerci d'avoir joué !\n")
        game.finished = True
        return True

    def help(game, words, n):
        print("\nCommandes disponibles:")
        for cmd in game.commands.values():
            print(f" - {cmd.command_word}{cmd.help_string}")
        return True

    def take(game, words, n):
        if len(words) != 2:
            return False
        item = words[1]
        room = game.player.current_room
        
        if item not in room.inventory:
            print("Objet introuvable.")
            return False
        
        obj = room.inventory[item]
        if game.player.current_weight() + obj.weight > game.player.max_weight:
            print("Trop lourd.")
            return False
        
        game.player.inventory[item] = obj
        del room.inventory[item]
        print(f"{item} pris.")
        game.quest_manager.check_quests(game, "item", item)
        return True

    def drop(game, words, n):
        if len(words) != 2:
            return False
        item = words[1]

        if item not in game.player.inventory:
            print("Objet non possédé.")
            return False
        
        game.player.current_room.inventory[item] = game.player.inventory[item]
        del game.player.inventory[item]
        print(f"{item} déposé.")
        return True

    def check(game, words, n):
        print(game.player.get_inventory())
        return True

    def talk(game, words, n):
        if len(words) != 2:
            return False
        
        name = words[1].lower()
        room = game.player.current_room
        
        for c in room.characters.values():
            if c.name.lower() == name:
                print(c.get_msg())
                game.quest_manager.check_quests(game, "talk", c.name)
                return True
        
        print("PNJ introuvable.")
        return False

    def use(game, words, n):
        if len(words) != 2:
            return False
        
        name = words[1]
        if name not in game.player.inventory:
            print("Objet absent.")
            return False
        
        obj = game.player.inventory[name]
        if hasattr(obj, "use"):
            obj.use(game.player, game)
            if isinstance(obj, Potion):
                del game.player.inventory[name]
            return True
        
        print("Impossible d'utiliser.")
        return False

    def charge(game, words, n):
        for obj in game.player.inventory.values():
            if isinstance(obj, Beamer):
                obj.charge(game.player)
                return True
        print("Aucun Beamer.")
        return False

    def fire(game, words, n):
        for obj in game.player.inventory.values():
            if isinstance(obj, Beamer):
                obj.fire(game.player)
                return True
        print("Aucun Beamer.")
        return False

    def read(game, words, n):
        name = words[1]
        if name in game.player.inventory and isinstance(game.player.inventory[name], Scroll):
            game.player.inventory[name].use(game.player)
            return True
        print("Pas un parchemin.")
        return False

    def map(game, words, n):
        for obj in game.player.inventory.values():
            if isinstance(obj, Map):
                obj.use(game.player, game)
                return True
        print("Aucune carte.")
        return False
