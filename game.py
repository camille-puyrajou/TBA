# Description: Game class

# Import modules

from room import Room
from item import Item
from beamer import Beamer
from player import Player
from command import Command
from actions import Actions
from character import Character
import copy

# Toggle debugging messages across modules. Import this variable from other modules
# as: `from game import DEBUG` and guard debug prints with `if DEBUG: ...`
DEBUG = False
 
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
        characters = Command("characters", " : lister les personnages présents dans la pièce", Actions.characters, 0)
        self.commands["characters"] = characters
        talk = Command("talk", " <character_name> : parler à un personnage dans la pièce", Actions.talk, 1)
        self.commands["talk"] = talk
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
        mer = Room("Mer", "une mer calme et paisible.")
        self.rooms.append(mer)
        montagne = Room("Montagne", "les montagnes du royaume.")
        self.rooms.append(montagne)
        cristaux = Room("Cristaux", "une grotte de cristal.")
        self.rooms.append(cristaux)
        ciel = Room("Ciel", "les airs ! Vous vous dirigez en direction du repère du sorcier à dos de dragon.")
        self.rooms.append(ciel)
        repere = Room("Repère du sorcier", "le repère du sorcier...")
        self.rooms.append(repere)
        fontaine = Room("Fontaine", "une fontaine magique.")
        self.rooms.append(fontaine)
        Maison_du_sage = Room("Maison du sage", "la maison du sage.")
        self.rooms.append(Maison_du_sage)
        Le_jardin = Room("Le jardin du jardinier", "un jardin rempli de plante et de fruit et légumes.")
        self.rooms.append(Le_jardin)
        L_épicerie = Room("L'épicerie", " Le lieux de travail d'Elra qui vend toute sorte d'herbe et potions.")
        self.rooms.append(L_épicerie)
        sous_sol_du_sorcier = Room("Sous-sol du sorcier", "le sous-sol du sorcier, rempli de potions et ingrédients mystérieux.")
        self.rooms.append(sous_sol_du_sorcier)
        bibliothèque_du_sorcier = Room("Bibliothèque du sorcier", "la bibliothèque du sorcier, remplie de livres anciens et de parchemins magiques.")
        self.rooms.append(bibliothèque_du_sorcier)
        couloir_du_sorcier = Room("Couloir du sorcier", "le couloir du sorcier, menant à différentes pièces mystérieuses.")
        self.rooms.append(couloir_du_sorcier)
        salle_de_rituel = Room("Salle de rituel", "la salle de rituel du sorcier, où des cérémonies magiques ont lieu.")
        self.rooms.append(salle_de_rituel)

        # Create exits for rooms

        chambre.exits = {"N" : None, "E" : penderie, "S" : None, "O" : None, "U" : None, "D" : couloir} 
        penderie.exits = {"N" : None, "E" : None, "S" : None, "O" : chambre, "U" : None, "D" : None}
        couloir.exits = {"N" : None, "E" : cuisine, "S" : chateau, "O" : bibliotheque, "U" : chambre, "D" : None}
        cuisine.exits = {"N" : None, "E" : None, "S" : None, "O" : couloir, "U" : None, "D" : None}
        bibliotheque.exits = {"N" : None, "E" : couloir, "S" : None, "O" : None, "U" : None, "D" : None}
        chateau.exits = {"N" : couloir, "E" : None, "S" : foret, "O" : None, "U" : None, "D" : None}
        foret.exits = {"N" : chateau, "E" : None, "S" : fontaine, "O" : None, "U" : None, "D" : None}
        fontaine.exits = {"N" : foret, "E" : ruines, "S" : pont, "O" : village, "U" : None, "D" : None}
        village.exits = {"N" : L_épicerie, "E" : fontaine, "S" : Le_jardin, "O" : Maison_du_sage, "U" : None, "D" : None}
        Le_jardin.exits = {"N" : village, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}
        L_épicerie.exits ={"N" : None, "E" : None, "S" : village, "O" : None, "U" : None, "D" : None}
        Maison_du_sage.exits = {"N" : None, "E" : village, "S" : None, "O" : None, "U" : None, "D" : None}
        ruines.exits = {"N" : None, "E" : grotte, "S" : montagne, "O" : foret, "U" : None, "D" : None}
        pont.exits = {"N" : foret, "E" : None, "S" : None, "O" : None, "U" : mer, "D" : None}
        ##Comme le personnage est prit au piège dans la grotte, pourquoi ne pas faire un sénario ou il ferme les yeux puis les rouvrent et se retrouve dans la forêt (transition). 
        ### On pourrait demander à la personne d'utiliser la commende 'go ?' pour que celle-ci le ramène à la forêt.
        grotte.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None,  "?": foret }
        montagne.exits = {"N" : None, "E" : None, "S" : cristaux, "O" : None, "U" : None, "D" : None}
        cristaux.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : ciel, "D" : None}
        ciel.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : repere}
        repere.exits = {"N" : None, "E" : None, "S" : couloir_du_sorcier, "O" : None, "U" : None, "D" : None}
        mer.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : montagne}
        couloir_du_sorcier.exits = {"N" : None, "E" : bibliothèque_du_sorcier, "S" : sous_sol_du_sorcier, "O" : salle_de_rituel, "U" : None, "D" : None}
        sous_sol_du_sorcier.exits = {"N" : couloir_du_sorcier, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}
        salle_de_rituel.exits = {"N" : None, "E" : None, "S" : None, "O" : couloir_du_sorcier, "U" : None, "D" : None}
        bibliothèque_du_sorcier.exits = {"N" : None, "E" : couloir_du_sorcier, "S" : None, "O" : None, "U" : None, "D" : None}





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
        livre_de_sorts = Item("livre de sorts", "un livre de sorts magiques.", 1.5)
        repere.item[livre_de_sorts.name] = livre_de_sorts

        # Characters
        garde = Character("Garde", "un garde vigilant protégeant le château.", chateau, ["Bonjour votre majesté !", "Tout est en ordre dans le château."])
        chateau.item[garde.name] = garde
        bibliothecaire = Character("Bibliothécaire", "un vieux bibliothécaire avec une longue barbe blanche.", bibliotheque, ["Chut ! C'est une bibliothèque.", "Avez-vous besoin d'aide pour trouver un livre ?"])
        bibliotheque.item[bibliothecaire.name] = bibliothecaire
        Cuisinière = Character ("Cuisinière", "Une femme âgée qui cuisine dans la cuisine.", cuisine, ["Bonjour ! Que voulez-vous manger aujourd'hui ?", "J'ai préparé un délicieux repas pour vous."])
        lutin = Character("Lutin", "un petit lutin espiègle avec un chapeau pointu.", foret, ["Bienvenue dans la forêt enchantée !", "Faites attention aux créatures magiques."])
        foret.item[lutin.name] = lutin
        Cinerio = Character("Cinerio", "un vieil homme sage avec une longue barbe grise.", repere, ["Vous avez fait un long voyage pour arriver ici.", "La sagesse est la clé de nombreux mystères."])
        repere.item[Cinerio.name] = Cinerio
        Cylian = Character("Cylian", "un grand dragon rouge avec des écailles étincelantes.", ciel, ["Rohouuuuu ! Je suis le gardien des airs.", "Monte sur mon dos pour un voyage inoubliable !"])
        ciel.item[Cylian.name] = Cylian
        Zeph = Character("Zeph", "un sorcier mystérieux vêtu d'une robe sombre.", repere, ["Vous avez réussi à me trouver.", "Le véritable pouvoir réside en vous."])
        repere.item[Zeph.name] = Zeph
        Willow = Character("Willow", "une petite fée lumineuse avec des ailes scintillantes.", cristaux, ["Bienvenue dans la grotte de cristal.", "La magie est partout autour de nous."])
        cristaux.item[Willow.name] = Willow
        Pêcheur = Character("Pêcheur", "un pêcheur robuste qui vend des bateaux.", pont, ["La mer est calme aujourd'hui.", "Vous voulez acheter un bateau ?"])
        pont.item[Pêcheur.name] = Pêcheur
        Elra = Character("Elra", "une jeune Herboriste .", village, ["Salut ! Je fournis toujours pleins de potion pour être prêt pour l'aventures.", "As-tu entendu parler des ruines anciennes ?"])
        village.item[Elra.name] = Elra
        Sully = Character("Sully", "un animal fantastique fidèle au joueur.", chambre, ["Je suis prêt pour l'aventure !", "N'oublie pas de me nourrir."])
        couloir.item[Sully.name] = Sully
        Villageois1 = Character("Villageois1", "la piplette du village qui absorbe tout votrre temps.", village, ["Bonjour ! Comment se passe votre journée ?", "Avez-vous entendu parler des rumeurs du village ?"])
        village.item[Villageois1.name] = Villageois1
        Villageois2 = Character("Villageois2", "L'historien du villa, il vous raccontera des histoires.", village, ["Salut ! J'ai une histoire incroyable à te raconter.", "Le village est plein de mystères."])
        village.item[Villageois2.name] = Villageois2
        Villageois3 = Character("Villageois3", "Le guide du village  qui aime aider les voyageurs.", village, ["Bonjour ! Comment puis-je vous aider aujourd'hui ?", "Le village est un endroit accueillant."])
        village.item[Villageois3.name] = Villageois3
        Villageois4 = Character("Villageois4", "une petite fille qui aime chanter des chansons.", village, ["Salut ! Voulez-vous entendre une chanson ?", "La musique est la langue universelle."])
        village.item[Villageois4.name] = Villageois4
        Villageois5 = Character("Villageois5", "Le jardinier qui aime les plantes et la végetation .", village, ["Bonjour ! Avez-vous besoin de conseils sur le jardinage ?", "Les plantes sont mes amies."])
        village.item[Villageois5.name] = Villageois5


        
                                   

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
        # Optional debug output for developers
        if DEBUG:
            try:
                print("DEBUG: process_command: ", list_of_words)
            except Exception:
                pass

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys() and command_word != "":
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        elif command_word == "":
            self.process_command(input("> "))
        else:
            command = self.commands[command_word]
            previous_room = None
            try:
                previous_room = self.player.current_room
            except Exception:
                previous_room = None

            try:
                command.action(self, list_of_words, command.number_of_parameters)
                if DEBUG:
                    try:
                        print(f"DEBUG: executed command '{command_word}'")
                    except Exception:
                        pass
            except Exception:
                pass

            # Faire avancer les PNJ uniquement si le joueur a changé de pièce
            try:
                if self.player and self.player.current_room is not previous_room:
                    self.tick_npcs()
            except Exception:
                pass

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

    def tick_npcs(self):
        """Fait tenter un déplacement à tous les PNJ du jeu.

        Si un PNJ part de / arrive dans la pièce du joueur, affiche
        un petit message pour que le joueur le remarque.
        """
        npcs = []
        for room in self.rooms:
            for obj in list(room.item.values()):
                # import local to avoid circular import issues
                try:
                    from character import Character
                except Exception:
                    Character = None
                if Character and isinstance(obj, Character):
                    npcs.append(obj)

        for npc in npcs:
            old_room = npc.current_room
            moved = False
            try:
                moved = npc.move()
            except Exception:
                moved = False


def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
 