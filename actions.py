"""Module contenant la classe Actions pour gérer toutes les commandes du jeu Naruto Adventure."""
import random
from character import Character
from item import Map

DEBUG = True  # Pour vérification PNJ mobiles

MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:
    """Classe regroupant toutes les actions exécutables par le joueur."""
    def __init__(self, player, quest_manager, game_gui):
        self.player = player
        self.quest_manager = quest_manager
        self.game_gui = game_gui
    
    def go(self, game, list_of_words, number_of_parameters):
        """Déplace le joueur dans la direction ou la salle indiquée."""
        player = game.player
        if len(list_of_words) < 2:
            print("\nPrécisez la direction ou le nom de la salle.")
            return False

        dest = list_of_words[1]

        # Vérifie si la direction est une sortie
        room = None
        for key, r in player.current_room.exits.items():
            if dest.upper() == key.upper() or dest.lower() == key.lower() or dest.lower() == r.name.lower():
                room = r
                break

        if not room:
            print("\nDirection ou salle inconnue !")
            return False

        player.history.append(player.current_room)
        player.current_room = room
        print(f"\nVous êtes maintenant dans {room.name}\n{room.get_long_description()}")

        # Valide les quêtes liées aux déplacements
        game.quest_manager.check_quests(game, "move", player.current_room.name)

        # Déplacement des PNJ après chaque action
        for r in game.rooms:
            for char in list(r.characters.values()):
                char.move()
                if DEBUG:
                    print(f"DEBUG: {char.name} moved to {char.current_room.name}")
        return True

    def quit(self, game, list_of_words, number_of_parameters):
        """Quitte le jeu proprement."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        print(f"\nMerci {game.player.name} d'avoir joué. Au revoir.\n")
        game.finished = True
        return True

    def help(self, game, list_of_words, number_of_parameters):
        """Affiche la liste des commandes disponibles."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        print("\nCommandes disponibles:")
        for c in game.commands.values():
            print(f" - {c}")
        return True

    def look(self, game, args, nb_params):
        """Affiche la description de la salle actuelle."""
        room = game.player.current_room
        print(room.get_long_description())
        return True

    def take(self, game, args, nb_params):
        """Permet de ramasser un objet dans la salle."""
        if len(args) < 2:
            print("Précisez l'objet à prendre.")
            return False
        name = args[1]
        room = game.player.current_room
        if name not in room.inventory:
            print(f"'{name}' n'est pas ici.")
            return False
        item = room.inventory[name]
        if game.player.current_weight() + item.weight > game.player.max_weight:
            print(f"Impossible de porter '{name}' (poids trop élevé).")
            return False
        game.player.inventory[name] = item
        del room.inventory[name]
        print(f"✅ Objet pris : '{name}'")
        game.quest_manager.check_quests(game, "item", name)
        return True

    def drop(self, game, args, nb_params):
        """Permet de déposer un objet de l'inventaire dans la salle."""
        if len(args) < 2:
            print("Précisez l'objet à déposer.")
            return False
        name = args[1]
        if name not in game.player.inventory:
            print(f"Vous n'avez pas '{name}'.")
            return False
        item = game.player.inventory[name]
        game.player.current_room.inventory[name] = item
        del game.player.inventory[name]
        print(f"Objet déposé : '{name}'")
        return True

    def check(self, game, args, nb_params):
        """Affiche l'inventaire du joueur."""
        print(game.player.get_inventory())
        return True

    def talk(self, game, args, nb_params):
        """Permet de parler avec un PNJ dans la salle."""
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

        # 🎯 Fin du jeu avec Gaara
        if room.name == "QG Akatsuki" and name == "gaara":
            if game.quest_manager.is_completed():
                print("DEBUG: Victoire déclenchée")
                game.game_gui.show_victory()
            else:
                print("DEBUG: Défaite déclenchée")
                game.game_gui.show_looser()

        return found


    def use(self, game, args, nb_params):
        """Utilise un objet de l'inventaire."""
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
        # Si c'est la carte, affiche la carte
        if isinstance(item, Map) and hasattr(game.game_gui, "show_map"):
            game.game_gui.show_map()
        return True

    def hide(self, game, args, nb_params):
        """Cache la carte si elle est affichée."""
        # Spécial pour cacher la carte
        if hasattr(game.game_gui, "hide_map"):
            game.game_gui.hide_map()
        return True

    def history(self, game, list_of_words, number_of_parameters):
        """Affiche l'historique des salles visitées."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        print(game.player.get_history())
        return True

    def back(self, game, list_of_words, number_of_parameters):
        """Retourne à la salle précédente visitée."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        if not game.player.history:
            print("\nImpossible de revenir en arrière, aucune salle précédente.\n")
            return False
        previous_room = game.player.history.pop()
        game.player.current_room = previous_room
        print(f"\nRetour à {previous_room.name}")
        print(previous_room.get_long_description())
        return True