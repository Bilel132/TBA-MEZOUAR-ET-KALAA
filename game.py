import tkinter as tk
from PIL import Image, ImageTk
import os, sys

from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from quest import Quest, QuestManager
from item import Item, Map


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


class Game:
    def __init__(self):
        self.commands = {}
        self.rooms = []
        self.player = None
        self.quest_manager = QuestManager()
        self.finished = False
        self.game_gui = None

    def setup(self, player_name):
        self.player = Player(player_name)

        self.commands = {
            "help": Command("help","aide",Actions.help,0),
            "go": Command("go","se déplacer",Actions.go,1),
            "look": Command("look","observer",Actions.look,0),
            "take": Command("take","prendre objet",Actions.take,1),
            "drop": Command("drop","déposer objet",Actions.drop,1),
            "talk": Command("talk","parler",Actions.talk,1),
            "use": Command("use","utiliser",Actions.use,1),
            "check": Command("check","inventaire",Actions.check,0),
            "quit": Command("quit","quitter",Actions.quit,0),
            "back": Command("back","retour",Actions.back,0),
            "history": Command("history","historique",Actions.history,0),
            "hide": Command("hide","cacher carte",Actions.hide,0)
        }

        # --- ROOMS ---
        konoha = Room("Konohagakure","Village ninja")
        suna = Room("Sunagakure","Village du sable")
        iwa = Room("Iwagakure","Village de pierre")
        kiri = Room("Kirigakure","Village de la brume")
        kumo = Room("Kumogakure","Village de la foudre")
        oto = Room("Otogakure","Village du son")
        kusa = Room("Kusagakure","Village de l’herbe")
        qg = Room("QG Akatsuki","Repaire ennemi")

        bureau = Room("Bureau du Hokage","Salle secrète")
        prison = Room("Prison de Kiri","Salle facultative")
        archives = Room("Archives Suna","Salle facultative")

        # --- EXITS ---
        konoha.exits = {"E": suna, "S": kumo, "N": bureau}
        suna.exits = {"W": konoha, "E": iwa, "S": archives, "N": qg}
        iwa.exits = {"W": suna, "N": kusa}
        kusa.exits = {"S": iwa, "E": kiri}
        kiri.exits = {"W": kusa, "S": prison, "E": qg}
        kumo.exits = {"N": konoha, "E": oto}
        oto.exits = {"W": kumo, "N": qg}

        bureau.exits = {"S": konoha}
        prison.exits = {"N": kiri}
        archives.exits = {"N": suna}
        qg.exits = {"S": suna, "W": oto, "O": kiri}

        # --- ITEMS ---
        konoha.inventory["kunai"] = Item("kunai","arme ninja",1)
        konoha.inventory["carte"] = Map()

        # --- CHARACTERS ---
        Character("Naruto","Héros ninja",konoha,["Dattebayo !"])
        Character("Sasuke","Rival ninja",suna,["Tch..."])
        Character("Gaara","Kazekage",qg,["Je protège mon village"])

        self.rooms = [konoha,suna,iwa,kiri,kumo,oto,kusa,qg,bureau,prison,archives]
        self.player.current_room = konoha

        # --- QUESTS ---
        self.quest_manager.add_quest(Quest("Aller à Sunagakure","Voyager",["move:Sunagakure"],["XP"]))
        self.quest_manager.add_quest(Quest("Prendre Kunai","Objet",["item:kunai"],["XP"]))
        self.quest_manager.add_quest(Quest("Parler à Gaara","PNJ",["talk:gaara"],["XP"]))
        self.quest_manager.add_quest(Quest("Aller au QG Akatsuki","Voyager",["move:QG Akatsuki"],["XP"]))

        for q in self.quest_manager.quests:
            q.activate()

    def process(self, text):
        parts = text.split()
        if not parts:
            return
        cmd = parts[0].lower()
        if cmd in self.commands:
            self.commands[cmd].action(self, parts, self.commands[cmd].number_of_parameters)
        else:
            print("❌ Commande inconnue.")


class GameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔥 Naruto Adventure")
        self.geometry("1200x750")
        self.configure(bg="#222")

        self.game = Game()
        self.game.game_gui = self

        self.ask_name_screen()

    def ask_name_screen(self):
        self.name_frame = tk.Frame(self, bg="#222")
        self.name_frame.pack(expand=True)

        tk.Label(self.name_frame, text="Entre ton prénom :", fg="white", bg="#222", font=("Consolas",16)).pack(pady=10)
        self.name_entry = tk.Entry(self.name_frame, font=("Consolas",14))
        self.name_entry.pack(pady=5)

        tk.Button(self.name_frame, text="Commencer", command=self.start_game).pack(pady=15)

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            name = "Joueur"

        self.name_frame.destroy()
        self.game.setup(name)
        self.build_gui()

        print(f"\n🎮 Bienvenue {name} dans Naruto Adventure !")
        self.refresh()

    def build_gui(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        self.text = tk.Text(self, bg="black", fg="white", font=("Consolas",12), state="disabled")
        self.text.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=10)

        sys.stdout = Redirect(self.text)

        self.image_label = tk.Label(self, bg="#222")
        self.image_label.grid(row=0, column=1, padx=10, pady=10)

        self.entry = tk.Entry(self, font=("Consolas",12))
        self.entry.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        self.entry.bind("<Return>", self.send)

        tk.Button(self, text="Envoyer", command=self.send).grid(row=4, column=1)

        nav = tk.Frame(self, bg="#222")
        nav.grid(row=5, column=1, pady=15)

        tk.Button(nav, text="↑ N", command=lambda:self.move("N")).grid(row=0, column=1)
        tk.Button(nav, text="← O", command=lambda:self.move("O")).grid(row=1, column=0)
        tk.Button(nav, text="→ E", command=lambda:self.move("E")).grid(row=1, column=2)
        tk.Button(nav, text="↓ S", command=lambda:self.move("S")).grid(row=2, column=1)

    def send(self, event=None):
        cmd = self.entry.get()
        self.entry.delete(0,"end")
        self.game.process(cmd)
        self.refresh()

    def move(self, direction):
        self.game.process(f"go {direction}")
        self.refresh()

    def refresh(self):
        room = self.game.player.current_room
        print("\n" + room.get_long_description())

        if hasattr(self, "showing_end_screen") and self.showing_end_screen:
            return

        img_path = f"assets/{room.name}.png"
        if os.path.exists(img_path):
            img = Image.open(img_path).resize((420,420))
            self.pic = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.pic)
        else:
            self.image_label.config(image="")

    def show_victory(self):
        self.showing_end_screen = True
        path = "assets/winner.jpg"
        print("DEBUG: Chargement image victoire ->", path)

        if os.path.exists(path):
            img = Image.open(path).resize((420,420))
            self.pic = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.pic)
            self.image_label.image = self.pic

        print("\n🏆 VICTOIRE ! Jeu terminé.")

    def show_looser(self):
        self.showing_end_screen = True
        path = "assets/looser.jpg"
        print("DEBUG: Chargement", path)

        if os.path.exists(path):
            img = Image.open(path).resize((420,420))
            self.pic = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.pic)
            self.image_label.image = self.pic
            print("\n❌ GAME OVER")
        else:
            print("❌ looser.jpg introuvable")


if __name__ == "__main__":
    GameGUI().mainloop()
