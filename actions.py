MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

import random

class Actions:

    # --- Déplacement ---
    def go(game, list_of_words, number_of_parameters):
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        direction = list_of_words[1].upper()
        if direction not in player.current_room.exits:
            print("\nDirection Inconnue !")
            return False

        player.move(direction)
        game.quest_manager.check_quests(game, "move", player.current_room.name)
        return True

    # --- Quitter ---
    def quit(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        print(f"\nMerci {game.player.name} d'avoir joué. Au revoir.\n")
        game.finished = True
        return True

    # --- Aide ---
    def help(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        print("\nCommandes disponibles:")
        for c in game.commands.values():
            print(f" - {c}")
        return True

    # --- Observer ---
    def look(game, args, nb_params):
        room = game.player.current_room
        print(room.get_long_description())

    # --- Prendre objet ---
    def take(game, args, nb_params):
        if len(args) < 2:
            print("Précisez l'objet à prendre.")
            return
        name = args[1]
        room = game.player.current_room
        if name not in room.inventory:
            print(f"'{name}' n'est pas ici.")
            return
        item = room.inventory[name]
        if game.player.current_weight() + item.weight > game.player.max_weight:
            print(f"Impossible de porter '{name}' (poids trop élevé).")
            return
        game.player.inventory[name] = item
        del room.inventory[name]
        print(f"Vous avez pris '{name}'.")
        game.quest_manager.check_quests(game, "item", name)

    # --- Déposer objet ---
    def drop(game, args, nb_params):
        if len(args) < 2:
            print("Précisez l'objet à déposer.")
            return
        name = args[1]
        if name not in game.player.inventory:
            print(f"Vous n'avez pas '{name}'.")
            return
        item = game.player.inventory[name]
        room = game.player.current_room
        room.inventory[name] = item
        del game.player.inventory[name]
        print(f"Vous avez déposé '{name}'.")

    # --- Inventaire ---
    def check(game, args, nb_params):
        print(game.player.get_inventory())

    # --- Parler à un PNJ ---
    def talk(game, args, nb_params):
        if len(args) != 2:
            print("\nUsage : talk <nom_PNJ>\n")
            return False
        name = args[1].lower()
        room = game.player.current_room
        found = False
        for char in room.characters.values():
            if char.name.lower() == name:
                print(f"\n{char.get_msg()}\n")
                found = True
                break
        if not found:
            print(f"Aucun PNJ nommé '{name}' ici.")
        game.quest_manager.check_quests(game, "talk", name)
        return found

    # --- Utiliser objet ---
    def use(game, args, nb_params):
        if len(args) != 2:
            print("\nUsage : use <nom_objet>\n")
            return False
        name = args[1]
        if name not in game.player.inventory:
            print(f"Vous n'avez pas '{name}'.")
            return False
        item = game.player.inventory[name]
        if hasattr(item, "use"):
            item.use(game.player, game)
        else:
            print(f"'{name}' ne peut pas être utilisé.")
        game.quest_manager.check_quests(game, "use", name)
        return True
