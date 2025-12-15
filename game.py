# Description: Game class

# Import modules

from room import Room
from item import Item
from beamer import Beamer
from player import Player
from command import Command
from actions import Actions
import copy

 
class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.history = []
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        look = Command("look", " : regarder la pièce (liste des objets présents)", Actions.look, 0)
        self.commands["look"] = look
        history = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back
        inventory = Command("inventory", " : afficher l'inventaire du joueur", Actions.inventory, 0)
        self.commands["inventory"] = inventory
        take = Command("take", " <item_name> : prendre un objet dans la pièce", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item_name> : déposer un objet de l'inventaire dans la pièce", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : examiner l'inventaire du joueur", Actions.check, 0)
        self.commands["check"] = check
        charge = Command("charge", " <slot_name> : charger le beamer dans un slot nommé", Actions.charge, 1)
        self.commands["charge"] = charge
        fire = Command("fire", " <slot_name> : téléporter le joueur vers le slot nommé", Actions.fire, 1)
        self.commands["fire"] = fire
        
        list_beamer = Command("list_beamer", " : lister les slots du beamer", Actions.list_beamer, 0)
        self.commands["list_beamer"] = list_beamer
        # Setup rooms

        chambre = Room("Chambre", "votre chambre.")
        self.rooms.append(chambre)
        penderie = Room("Penderie", "votre penderie.")
        self.rooms.append(penderie)
        couloir = Room("Couloir", "un couloir de votre château.")
        self.rooms.append(couloir)
        cuisine = Room("Cuisine", "la cuisine de votre château.")
        self.rooms.append(cuisine)
        bibliotheque = Room("Bibliothèque", "la bibliothèque du château.")
        self.rooms.append(bibliotheque)
        chateau = Room("Chateau", "la cour du château.")
        self.rooms.append(chateau)
        foret = Room("Forêt enchentée", "une forêt enchantée, peuplée d'animaux extraordianires.")
        self.rooms.append(foret)
        village = Room("Village", "un village paisible.")
        self.rooms.append(village)
        ruines = Room("Ruines", "les ruines d'un ancien temple.")
        self.rooms.append(ruines)
        pont = Room("Pont", "sur un ponton. Vous contemplez la mer à perte de vue.")
        self.rooms.append(pont)
        grotte = Room("Grotte", "une grotte sombre et sinueuse.")
        self.rooms.append(grotte)
        montagne = Room("Montagne", "les montagnes du royaume.")
        self.rooms.append(montagne)
        cristaux = Room("Cristaux", "une grotte de cristal.")
        self.rooms.append(cristaux)
        ciel = Room("Ciel", "les airs ! Vous vous dirigez en direction du repère du sorcier à dos de dragon.")
        self.rooms.append(ciel)
        repere = Room("Repère du sorcier", "le repère du sorcier...")
        self.rooms.append(repere)

        # Create exits for rooms

        chambre.exits = {"N" : None, "E" : penderie, "S" : None, "O" : None, "U" : None, "D" : couloir} 
        penderie.exits = {"N" : None, "E" : None, "S" : None, "O" : chambre, "U" : None, "D" : None}
        couloir.exits = {"N" : None, "E" : cuisine, "S" : chateau, "O" : bibliotheque, "U" : chambre, "D" : None}
        cuisine.exits = {"N" : None, "E" : None, "S" : None, "O" : couloir, "U" : None, "D" : None}
        bibliotheque.exits = {"N" : None, "E" : couloir, "S" : None, "O" : None, "U" : None, "D" : None}
        chateau.exits = {"N" : couloir, "E" : None, "S" : foret, "O" : None, "U" : None, "D" : None}
        foret.exits = {"N" : None, "E" : ruines, "S" : pont, "O" : village, "U" : None, "D" : None}
        village.exits = {"N" : None, "E" : foret, "S" : None, "O" : None, "U" : None, "D" : None}
        ruines.exits = {"N" : None, "E" : grotte, "S" : montagne, "O" : foret, "U" : None, "D" : None}
        pont.exits = {"N" : foret, "E" : montagne, "S" : None, "O" : None, "U" : None, "D" : None}
        ##Comme le personnage est prit au piège dans la grotte, pourquoi ne pas faire un sénario ou il ferme les yeux puis les rouvrent et se retrouve dans la forêt (transition). 
        ### On pourrait demander à la personne d'utiliser la commende 'go ?' pour que celle-ci le ramène à la forêt.
        grotte.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None,  "?": foret }
        montagne.exits = {"N" : None, "E" : None, "S" : cristaux, "O" : None, "U" : None, "D" : None}
        cristaux.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : ciel, "D" : None}
        ciel.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : repere}
        repere.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}

        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = chambre 

        # Set up objets in rooms
        diary = Item("diary", "votre carnet relié en cuir. ", 0.7)
        chambre.item[diary.name] = diary
        # Quelques objets supplémentaires répartis sur la map
        sac = Item("sac", "un sac à dos pour commencer votre aventure.", 0.8)
        penderie.item[sac.name] = sac
        pomme = Item("pomme", "une pomme rouge et juteuse.", 0.2)
        cuisine.item[pomme.name] = pomme
        livre = Item("livre", "un vieux grimoire poussiéreux.", 1.2)
        bibliotheque.item[livre.name] = livre
        baguette = Item("Baguette", "une baguette de pain chaud sortie du four.", 0.3)
        cuisine.item[baguette.name] = baguette
        # Placer un Beamer (avec comportements de charge / fire) dans le château
        beamer = Beamer("beamer", "un beamer magique pour vous téléporter. Charger-le dans un lieu pour vous téléporter dans ce lieu à partir d'un autre endroit.", 2)
        chateau.item[beamer.name] = beamer
        artefact = Item("artefact", "un artefact ancien et mystérieux.", 0.9)
        ruines.item[artefact.name] = artefact
        gemme = Item("gemme", "une gemme brillante aux reflets multicolores.", 0.1)
        cristaux.item[gemme.name] = gemme
        pendantif = Item("pendantif", "un pendentif en or orné d'une pierre précieuse se trouve au fond de l'eau.", 0.4)
        pont.item[pendantif.name] = pendantif
        # Cela serait bien que cela soit un PNJ enfant qui donne la peluche au joueur dans le village. Prendre en compte le cas où le sac est déjà rempli (poid 2.5Kg).
        peluche = Item("peluche", "une peluche douce en forme de dragon.", 0.1)
        village.item[peluche.name] = peluche
        oeuf_de_dragon = Item("oeuf de dragon", "un œuf de dragon chaud au toucher.", 2)
        foret.item[oeuf_de_dragon.name] = oeuf_de_dragon
        corne_de_licorne = Item("corne de licorne", "une corne de licorne scintillante. La légende raconte qu'elle porterai bonheur...", 0.3)
        foret.item[corne_de_licorne.name] = corne_de_licorne

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys() and command_word != "":
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        elif command_word == "":
            self.process_command(input("> "))
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")

        # Affiche la description courte de la pièce de départ (sans la liste d'objets).
        print(self.player.current_room.get_short_description())

    def save_state(self):
        snapshot = {
            "player": copy.deepcopy(self.player),
            "rooms": copy.deepcopy(self.rooms)
        }
        self.history.append(snapshot)

    def restore_state(self):
        if self.history:
            snapshot = self.history.pop()
            self.player = snapshot["player"]
            self.rooms = snapshot["rooms"]
            # Restaurer l'état sans afficher automatiquement l'inventaire de la pièce.
            print(self.player.current_room.get_short_description())
        else:
            print("\nAucune pièce précédente dans l'historique.\n")


def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
 