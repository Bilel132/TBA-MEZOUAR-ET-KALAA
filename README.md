# Naruto Adventure – Jeu d'Aventure Textuel

## Description
**Naruto Adventure** est un jeu d’aventure textuel développé en **Python** avec une interface graphique basée sur Tkinter. Le joueur incarne un ninja dans l'univers de Naruto et explore différents villages, interagit avec des personnages, collecte des objets et accomplit des quêtes.

Ce projet est conçu pour illustrer la programmation orientée objet, la gestion des quêtes, et la création d'une interface graphique simple en Python.

## Fonctionnalités
- Déplacement entre plusieurs salles et villages
- Interaction avec des PNJ (personnages non-joueurs)
- Prise et dépôt d’objets avec gestion du poids
- Système de quêtes avec objectifs et récompenses
- Affichage de l’inventaire et de l’historique des déplacements
- Utilisation d’objets spéciaux (comme la carte)
- Interface graphique avec Tkinter et affichage d’images des salles
- Commandes textuelles complètes (`go`, `look`, `take`, `drop`, `talk`, `use`, `check`, `history`, `back`, `quit`)

## Structure du projet
```
TBA-MEZOUAR-ET-KALAA/
│
├── game.py          # Logique principale du jeu
├── player.py        # Gestion du joueur
├── room.py          # Définition des salles
├── command.py       # Gestion des commandes
├── actions.py       # Actions exécutables par le joueur
├── character.py     # Personnages du jeu
├── quest.py         # Gestion des quêtes
├── item.py          # Objets du jeu (y compris carte)
├── assets/          # Images et ressources
├── __pycache__/     # Fichiers temporaires Python
└── README.md        # Documentation du projet
```

## Prérequis
- Python 3.8 ou supérieur
- Bibliothèques Python : `tkinter`, `Pillow`

## Installation
1. Cloner le dépôt :
```bash
git clone https://github.com/Bilel132/TBA-MEZOUAR-ET-KALAA.git
```
2. Se rendre dans le dossier du projet :
```bash
cd TBA-MEZOUAR-ET-KALAA
```
3. Installer Pillow si nécessaire :
```bash
pip install pillow
```

## Lancement du jeu
```bash
python game.py
```
- Une fenêtre s'ouvrira pour entrer le nom du joueur.
- Utilisez les commandes textuelles ou les boutons de navigation pour interagir avec le jeu.

## Commandes principales
- `go <direction>` : se déplacer vers une salle (N, S, E, O)
- `look` : observer la salle actuelle
- `take <objet>` : prendre un objet
- `drop <objet>` : déposer un objet
- `talk <PNJ>` : parler à un personnage
- `use <objet>` : utiliser un objet
- `check` : afficher l'inventaire
- `history` : afficher l'historique des salles visitées
- `back` : revenir à la salle précédente
- `quit` : quitter le jeu

## Objectifs pédagogiques
- Apprendre la programmation orientée objet en Python
- Créer un moteur de jeu textuel simple
- Implémenter des systèmes de commandes et de quêtes
- Utiliser Tkinter pour l'interface graphique

## Améliorations possibles
- Ajouter des combats ou compétences ninja
- Ajouter plus de PNJ et dialogues interactifs
- Système d’inventaire avancé
- Sauvegarde et chargement de partie
- Événements aléatoires ou mini-quêtes

## Auteurs
Projet réalisé par **MEZOUAR** et **KALAA**.

## Licence
Projet à but éducatif, sans licence spécifique définie.