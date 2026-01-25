Naruto Adventure

Naruto Adventure est un jeu d’aventure textuel avec interface graphique développé en Python, inspiré de l’univers de Naruto.
Le joueur explore des villages ninjas, interagit avec des personnages, collecte des objets et accomplit des quêtes pouvant mener à une victoire ou une défaite.

Le projet combine programmation orientée objet, logique de jeu, inventaire, quêtes et interface graphique Tkinter.

Concept du jeu

Le joueur incarne un ninja explorant plusieurs villages.
Il peut se déplacer entre des salles, parler à des PNJ, récupérer des objets, accomplir des quêtes et accéder à des salles facultatives.

Objectif principal :
Compléter toutes les quêtes et parler à Gaara au QG de l’Akatsuki pour gagner.

Fonctionnalités

Exploration de salles interconnectées
Salles principales et salles facultatives
Déplacements directionnels (N, S, E, O)
Historique des déplacements et retour arrière
PNJ interactifs avec dialogues
Déplacement automatique de certains PNJ
Inventaire avec gestion du poids
Système de quêtes dynamique
Commandes textuelles complètes
Interface graphique Tkinter
Affichage d’images selon la salle
Affichage d’une carte du monde
Affichage d’un écran de victoire ou de défaite

Commandes principales

help : afficher l’aide
go N / S / E / O : se déplacer
look : observer la salle
take objet : prendre un objet
drop objet : déposer un objet
talk pnj : parler à un personnage
use objet : utiliser un objet
check : afficher l’inventaire
history : voir l’historique
back : revenir en arrière
hide : cacher la carte
quit : quitter le jeu

Structure du projet

main.py : lancement du jeu
game.py : logique principale et interface
actions.py : gestion des commandes
room.py : gestion des salles
player.py : joueur et inventaire
item.py : objets et carte
character.py : personnages
quest.py : système de quêtes
command.py : commandes
assets/ : images du jeu
README.md : documentation

Lancement du jeu

Prérequis :
Python 3.9 ou plus
Pillow

Installation :
pip install pillow

Démarrage :
python main.py

Fins possibles

Fin gagnante :
Toutes les quêtes terminées
Arriver au QG Akatsuki
Parler à Gaara
Affichage de winner.jpg

Fin perdante :
Quêtes incomplètes
Parler à Gaara trop tôt
Affichage de looser.jpg