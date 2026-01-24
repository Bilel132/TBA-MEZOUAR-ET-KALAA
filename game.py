# game.py
# Import modules
from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from quest import Quest, QuestManager
from item import Item, Beamer, Potion, Scroll, Map, Key, Torch

import tkinter as tk
from PIL import Image, ImageTk
import sys
import os

# ------------------ GAME CLASS ------------------

class Game:
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.quest_manager = QuestManager()

    def win(self):
        return self.quest_manager.is_completed()

    def loose(self):
        if self.player.current_room.name == "QG Akatsuki" and "anneau" not in self.player.inventory:
            return True
        return False

    def setup(self, player_name):
        # --- Commands ---
        self.commands["help"] = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", " <direction> : se déplacer", Actions.go, 1)
        self.commands["history"] = Command("history", " : afficher l'historique", Actions.history, 0)
        self.commands["back"] = Command("back", " : revenir à la salle précédente", Actions.back, 0)
        self.commands["look"] = Command("look", " : observer la pièce", Actions.look, 0)
        self.commands["take"] = Command("take", " <item> : prendre un objet", Actions.take, 1)
        self.commands["drop"] = Command("drop", " <item> : déposer un objet", Actions.drop, 1)
        self.commands["check"] = Command("check", " : vérifier l'inventaire", Actions.check, 0)
        self.commands["talk"] = Command("talk", " <PNJ> : parler à un PNJ", Actions.talk, 1)
        self.commands["charge"] = Command("charge", " : mémoriser la salle avec Beamer", Actions.charge, 0)
        self.commands["fire"] = Command("fire", " : téléporter avec Beamer", Actions.fire, 0)
        self.commands["use"] = Command("use", " <item> : utiliser un objet", Actions.use, 1)
        self.commands["read"] = Command("read", " <item> : lire un parchemin", Actions.read, 1)
        self.commands["map"] = Command("map", " : afficher la carte", Actions.map, 0)

        # --- Rooms ---
        konoha = Room("Konohagakure", "dans le village caché de la Feuille, entouré d'arbres et de ninjas.")
        suna = Room("Sunagakure", "dans le village du Sable, balayé par un vent brûlant.")
        kiri = Room("Kirigakure", "dans le village de la Brume, noyé dans un brouillard permanent.")
        iwa = Room("Iwagakure", "dans le village de la Roche, entouré de montagnes massives.")
        kusa = Room("Kusagakure", "dans le village de l'Herbe, où les champs ondulent sous la brise.")
        kumo = Room("Kumogakure", "dans le village des Nuages, haut perché dans les montagnes.")
        oto = Room("Otogakure", "dans le village du Son, rempli de sons étranges.")
        akatsuki = Room("QG Akatsuki", "dans le repaire secret de l'Akatsuki, une grotte ornée de nuages rouges.")
        hokage = Room("Bureau du Hokage", "dans le bureau circulaire du Hokage, rempli de rouleaux confidentiels.")
        kiri_prison = Room("Prison de Kirigakure", "dans un sous-sol humide où résonnent des gouttes sinistres.")
        gedo = Room("Salle du Gedo Mazo", "devant la statue démoniaque géante, source d'énergie sinistre.")
        suna_archive = Room("Archives de Sunagakure", "dans une salle remplie de parchemins anciens et secrets.")

        self.rooms.extend([konoha,suna,kiri,iwa,kusa,kumo,oto,akatsuki,hokage,kiri_prison,gedo,suna_archive])

        # --- Exits ---
        konoha.exits = {"N": None,"E": suna,"S": iwa,"O": None,"UP": hokage,"DOWN": None}
        suna.exits = {"N": None,"E": kiri,"S": None,"O": konoha,"UP": suna_archive,"DOWN": None}
        kiri.exits = {"N": None,"E": None,"S": kusa,"O": suna,"UP": None,"DOWN": kiri_prison}
        iwa.exits = {"N": konoha,"E": akatsuki,"S": None,"O": None,"UP": None,"DOWN": None}
        kusa.exits = {"N": kiri,"E": kumo,"S": None,"O": None,"UP": None,"DOWN": None}
        kumo.exits = {"N": None,"E": None,"S": None,"O": oto,"UP": None,"DOWN": None}
        oto.exits = {"N": None,"E": kumo,"S": None,"O": akatsuki,"UP": None,"DOWN": None}
        akatsuki.exits = {"N": None,"E": oto,"S": None,"O": iwa,"UP": None,"DOWN": gedo}
        hokage.exits = {"UP": None,"DOWN": konoha}
        kiri_prison.exits = {"UP": kiri,"DOWN": None}
        gedo.exits = {"UP": akatsuki,"DOWN": None}
        suna_archive.exits = {"UP": None,"DOWN": suna}

        # --- Player ---
        self.player = Player(player_name)
        self.player.current_room = konoha

        # --- Quests ---
        self.quest_manager.add_quest(Quest("Trouver le parchemin", "Récupérer le parchemin secret", ["item:parchment1"], ["XP"]))
        self.quest_manager.add_quest(Quest("Visiter Sunagakure", "Se rendre dans le village du Sable", ["move:Sunagakure"], ["XP"]))
        self.quest_manager.add_quest(Quest("Parler à Gaara", "Interagir avec Gaara", ["talk:Gaara"], ["XP"]))

    # --- Command processing ---
    def process_command(self, command_string):
        if not command_string.strip():
            return
        words = command_string.split()
        command_word = words[0]
        if command_word not in self.commands:
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help'.\n")
        else:
            command = self.commands[command_word]
            command.action(self, words, command.number_of_parameters)

# ------------------ STDOUT REDIRECTOR ------------------

class _StdoutRedirector:
    def __init__(self,text_widget):
        self.text_widget = text_widget
    def write(self,text):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end",text)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")
    def flush(self):
        pass

# ------------------ GUI ------------------
class GameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jeu d'aventure")
        self.geometry("800x600")
        self.assets_dir = "assets/"

        # ------------------ Texte ------------------
        self.text_area = tk.Text(self, height=20, width=60, state="disabled", bg="black", fg="white")
        self.text_area.grid(row=0, column=0, rowspan=4, columnspan=4, padx=10, pady=10, sticky="nsew")

        # ------------------ Frame image bienvenue ------------------
        self.welcome_frame = tk.Frame(self, bg="black", bd=2, relief="ridge")
        self.welcome_frame.grid(row=1, column=4, rowspan=2, padx=10, pady=10)
        self.welcome_image_label = tk.Label(self.welcome_frame)
        self.welcome_image_label.pack(padx=5, pady=5)

        # Charger l'image de bienvenue
        image_path = os.path.join(self.assets_dir, "Konohagakure.png")
        if os.path.exists(image_path):
            image = Image.open(image_path).resize((300, 300))
            self.welcome_photo = ImageTk.PhotoImage(image)
            self.welcome_image_label.configure(image=self.welcome_photo)

        # ------------------ Frame image salle ------------------
        self.room_frame = tk.Frame(self, bg="black", bd=2, relief="ridge")
        self.room_frame.grid(row=0, column=4, rowspan=4, padx=10, pady=10)
        self.image_label = tk.Label(self.room_frame)
        self.image_label.pack(padx=5, pady=5)

        # ------------------ Entrée utilisateur ------------------
        self.input_entry = tk.Entry(self, width=50)
        self.input_entry.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.input_entry.bind("<Return>", self.start_game)

        self.send_button = tk.Button(self, text="Commencer", command=self.start_game)
        self.send_button.grid(row=4, column=3, padx=10, pady=5, sticky="ew")

        self.name_label = tk.Label(self, text="Entrez votre nom:")
        self.name_label.grid(row=0, column=0, columnspan=4, padx=10, pady=5)

    # ------------------ Début du jeu ------------------
    def start_game(self, event=None):
        player_name = self.input_entry.get().strip()
        if not player_name:
            return
        self.input_entry.delete(0, "end")
        self.name_label.destroy()
        self.welcome_frame.destroy()  # Supprimer l'image de bienvenue

        self.send_button.config(text="Envoyer", command=self.process_input)

        self.game = Game()
        self.game.setup(player_name)
        sys.stdout = _StdoutRedirector(self.text_area)

        self.create_move_buttons()
        self.update_room_display()

    # ------------------ Traitement des commandes ------------------
    def process_input(self, event=None):
        command_string = self.input_entry.get()
        self.input_entry.delete(0, "end")
        self.game.process_command(command_string)
        self.update_room_display()

    # ------------------ Boutons de déplacement ------------------
    def create_move_buttons(self):
        tk.Button(self, text="N", command=lambda: (self.game.process_command("go N"), self.update_room_display())).grid(row=0, column=5, padx=5, pady=5)
        tk.Button(self, text="S", command=lambda: (self.game.process_command("go S"), self.update_room_display())).grid(row=2, column=5, padx=5, pady=5)
        tk.Button(self, text="E", command=lambda: (self.game.process_command("go E"), self.update_room_display())).grid(row=1, column=6, padx=5, pady=5)
        tk.Button(self, text="O", command=lambda: (self.game.process_command("go O"), self.update_room_display())).grid(row=1, column=4, padx=5, pady=5)

    # ------------------ Mise à jour de la salle ------------------
    def update_room_display(self):
        room = self.game.player.current_room
        print(room.get_long_description())

        # Image de la salle
        image_path = os.path.join(self.assets_dir, f"{room.name}.png")
        if os.path.exists(image_path):
            image = Image.open(image_path).resize((300, 300))
            self.room_image = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.room_image)
        else:
            self.image_label.configure(image='')


    def start_game(self,event=None):
        player_name = self.input_entry.get().strip()
        if not player_name:
            return
        self.input_entry.delete(0,"end")
        self.name_label.destroy()

        #supprimer l'image de bienvenue ici
        self.welcome_image_label.destroy()

        self.send_button.config(text="Envoyer", command=self.process_input)

        self.game = Game()
        self.game.setup(player_name)
        sys.stdout = _StdoutRedirector(self.text_area)

        self.create_move_buttons()
        self.update_room_display()

    def process_input(self,event=None):
        command_string = self.input_entry.get()
        self.input_entry.delete(0,"end")
        self.game.process_command(command_string)
        self.update_room_display()

    def create_move_buttons(self):
        tk.Button(self,text="N",command=lambda: (self.game.process_command("go N"),self.update_room_display())).grid(row=0,column=5)
        tk.Button(self,text="S",command=lambda: (self.game.process_command("go S"),self.update_room_display())).grid(row=2,column=5)
        tk.Button(self,text="E",command=lambda: (self.game.process_command("go E"),self.update_room_display())).grid(row=1,column=6)
        tk.Button(self,text="O",command=lambda: (self.game.process_command("go O"),self.update_room_display())).grid(row=1,column=4)

    def update_room_display(self):
        room = self.game.player.current_room
        print(room.get_long_description())

        # Image
        image_path = os.path.join(self.assets_dir, f"{room.name}.png")
        if os.path.exists(image_path):
            image = Image.open(image_path).resize((300,300))
            self.room_image = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.room_image)
        else:
            self.image_label.configure(image='')

# ------------------ MAIN ------------------

if __name__ == "__main__":
    gui = GameGUI()
    gui.mainloop()
