# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        
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
        couloir.exits = {"N" : None, "E" : cuisine, "S" : chateau, "O" : bibliotheque, "U" : couloir, "D" : None}
        cuisine.exits = {"N" : None, "E" : None, "S" : None, "O" : couloir, "U" : None, "D" : None}
        bibliotheque.exits = {"N" : None, "E" : couloir, "S" : None, "O" : None, "U" : None, "D" : None}
        chateau.exits = {"N" : couloir, "E" : None, "S" : foret, "O" : None, "U" : None, "D" : None}
        foret.exits = {"N" : None, "E" : ruines, "S" : pont, "O" : village, "U" : None, "D" : None}
        village.exits = {"N" : None, "E" : foret, "S" : None, "O" : None, "U" : None, "D" : None}
        ruines.exits = {"N" : None, "E" : grotte, "S" : montagne, "O" : foret, "U" : None, "D" : None}
        pont.exits = {"N" : foret, "E" : montagne, "S" : None, "O" : None, "U" : None, "D" : None}
        ##ATTENTION : pas d'issue pour la grotte ! Par quel côté choisir pour retombé sur la fôret ?
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
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
