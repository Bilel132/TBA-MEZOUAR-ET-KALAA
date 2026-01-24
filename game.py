import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from quest import Quest, QuestManager
from item import Item


# -------- REDIRECTION PRINT -> TERMINAL GUI --------
class Redirect:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.config(state="normal")
        self.widget.insert("end", text)
        self.widget.see("end")
        self.widget.config(state="disabled")

    def flush(self):
        pass


# -------- GAME LOGIC --------
class Game:
    def __init__(self):
        self.commands = {}
        self.rooms = []
        self.player = None  # On initialise plus tard
        self.quest_manager = QuestManager()

    def setup(self, player_name):
        # Création du joueur AVEC le prénom
        self.player = Player(player_name)

        # COMMANDS
        self.commands = {
            "help": Command("help"," aide",Actions.help,0),
            "go": Command("go"," déplacement",Actions.go,1),
            "look": Command("look"," observer",Actions.look,0),
            "take": Command("take"," prendre",Actions.take,1),
            "drop": Command("drop"," déposer",Actions.drop,1),
            "talk": Command("talk"," parler",Actions.talk,1),
            "use": Command("use"," utiliser",Actions.use,1),
            "check": Command("check"," inventaire",Actions.check,0),
            "quit": Command("quit"," quitter",Actions.quit,0),
        }

        # ROOMS
        konoha = Room("Konohagakure","Village ninja")
        suna = Room("Sunagakure","Village du sable")
        akatsuki = Room("QG Akatsuki","Repaire ennemi")

        konoha.exits = {"N": suna}
        suna.exits = {"S": konoha, "E": akatsuki}
        akatsuki.exits = {"O": suna}

        konoha.inventory["kunai"] = Item("kunai","arme ninja",1)

        Character("Naruto","Héros ninja",konoha,["Dattebayo!"])

        self.rooms = [konoha, suna, akatsuki]
        self.player.current_room = konoha

        self.quest_manager.add_quest(
            Quest("Aller à Sunagakure","Voyager",["move:Sunagakure"],["XP"])
        )
        self.quest_manager.activate_quest("Aller à Sunagakure")

    def process(self, text):
        parts = text.split()
        if not parts:
            return
        
        cmd = parts[0]
        if cmd in self.commands:
            self.commands[cmd].action(self, parts, self.commands[cmd].number_of_parameters)
        else:
            print("❌ Commande inconnue.")


# -------- GUI --------
class GameGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("🔥 Naruto Adventure")
        self.geometry("1200x750")
        self.configure(bg="#222")

        # DEMANDE DU NOM AVANT LANCEMENT
        self.ask_name_screen()

    def ask_name_screen(self):
        self.name_frame = tk.Frame(self, bg="#222")
        self.name_frame.pack(expand=True)

        tk.Label(self.name_frame, text="Entre ton prénom :", fg="white", bg="#222", font=("Consolas", 16)).pack(pady=10)

        self.name_entry = tk.Entry(self.name_frame, font=("Consolas", 14))
        self.name_entry.pack(pady=5)

        tk.Button(self.name_frame, text="Commencer l'aventure", command=self.start_game).pack(pady=15)

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            name = "Joueur"

        self.name_frame.destroy()

        # Création du jeu avec prénom
        self.game = Game()
        self.game.setup(name)

        self.build_gui()

        print(f"🎮 Bienvenue {name} dans Naruto Adventure !")
        self.refresh()

    def build_gui(self):
        # GRID
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # TERMINAL TEXT
        self.text = tk.Text(self, bg="black", fg="white", font=("Consolas", 12), state="disabled")
        self.text.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=10)

        sys.stdout = Redirect(self.text)

        # IMAGE PANEL
        self.image_label = tk.Label(self, bg="#222")
        self.image_label.grid(row=0, column=1, padx=10, pady=10)

        # ENTRY BAR
        self.entry = tk.Entry(self, font=("Consolas", 12))
        self.entry.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        self.entry.bind("<Return>", self.send)

        # SEND BUTTON
        send_btn = tk.Button(self, text="Envoyer", command=self.send)
        send_btn.grid(row=4, column=1, pady=5)

        # MOVE BUTTONS
        move_frame = tk.Frame(self, bg="#222")
        move_frame.grid(row=5, column=1, pady=15)

        tk.Button(move_frame, text="↑ N", width=6, command=lambda: self.move("N")).grid(row=0, column=1)
        tk.Button(move_frame, text="← O", width=6, command=lambda: self.move("O")).grid(row=1, column=0)
        tk.Button(move_frame, text="→ E", width=6, command=lambda: self.move("E")).grid(row=1, column=2)
        tk.Button(move_frame, text="↓ S", width=6, command=lambda: self.move("S")).grid(row=2, column=1)

    def send(self, event=None):
        cmd = self.entry.get()
        self.entry.delete(0, "end")
        self.game.process(cmd)
        self.refresh()

    def move(self, direction):
        self.game.process(f"go {direction}")
        self.refresh()

    def refresh(self):
        room = self.game.player.current_room
        print("\n" + room.get_long_description())

        img_path = f"assets/{room.name}.png"
        if os.path.exists(img_path):
            img = Image.open(img_path).resize((420, 420))
            self.pic = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.pic)
        else:
            self.image_label.config(image="")


# -------- START --------
if __name__ == "__main__":
    GameGUI().mainloop()
