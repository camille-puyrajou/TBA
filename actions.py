# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"
from character1 import Character 
from character2 import Character2
from quests import Quest


class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
            # Affiche la description complète de la pièce (description + sorties + objets)
            print(player.current_room.get_long_description())
            # Puis affiche l'inventaire du joueur (demande explicite)
            print("\n" + player.get_inventory())
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        # Optional debug output
        try:
            from game import DEBUG
        except Exception:
            DEBUG = False
        if DEBUG:
            try:
                print(f"DEBUG: Actions.go called with {list_of_words}")
            except Exception:
                pass

        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1]
        # Take only the first letter and make it uppercase.
        direction = direction.upper()[0] 

        # If the direction is not valid, print an error message and return False.
        if direction not in player.current_room.exits.keys():
            print("\n Cette direction n'existe pas ! Veuillez utiliser une des directions suivantes :\n ", player.current_room.get_exit_string(), "\n")
          
        # Move the player in the direction specified by the parameter.
        else:
            game.save_state()
            player.move(direction)
            return True
        
        
    
    def back (game, list_of_words, number_of_parameters):
        """
        Déplacer le joueur vers la pièce précédemment visitée dans son historique.
        """
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        game.restore_state()  # restaure l’état complet
        return True
        # vérifier qu'il y a une pièce précédente dans l'historique
        if len(player.history) < 2:
            print("\nAucune pièce précédente dans l'historique.\n")
            return False
        
        # Supprimer la pièce actuelle de l'historique (celle d'où l'on revient)
        # Cela garantit que la pièce d'arrivée sera la nouvelle "dernière" de l'historique.
        player.history.pop() # Retire la dernière pièce de l'historique
        previous_room = player.history[-1]
        # trouver la pièce précédente parmi les sorties de la pièce actuelle
        player.current_room = previous_room

        
        if previous_room is None:
            print("\nImpossible de retourner à la pièce précédente dans le jeu.\n")
            player.history.append(game.player.current_room.name)
            return False
        
        # déplacer le joueur vers la pièce précédente
        player.current_room = previous_room
                    
        # Afficher la description de la nouvelle pièce (sans liste d'objets)
        print(game.player.current_room.get_short_description())
        
        # Afficher l'historique mis à jour
        try:
            print(player.get_history())
        except Exception:
            print("Impossible d'afficher l'historique.")

        return True
    
    
    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # Optional debug output
        try:
            from game import DEBUG
        except Exception:
            DEBUG = False
        if DEBUG:
            try:
                print(f"DEBUG: Actions.help called with {list_of_words}")
            except Exception:
                pass

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    def history(game, list_of_words, number_of_parameters):
        """
        Affiche l'historique des pièces visitées par le joueur.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        try:
            print(player.get_history())
        except Exception:
            print("Impossible d'afficher l'historique.")
        return True
    
    def inventory(game, list_of_words, number_of_parameters):
        """
        Affiche l'inventaire du joueur.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        try:
            # Utiliser la représentation centralisée de l'inventaire fournie par Player.get_inventory()
            print(player.get_inventory())
        except Exception:
            print("Impossible d'afficher l'inventaire.")
        return True
    
    def look ( game, list_of_words, number_of_parameters): 
        """
        Affiche la liste des objets présents dans la pièce actuelle.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        player = game.player
        current_room = player.current_room
        try:
            print(current_room.get_inventory())
        except Exception:
            print("Impossible d'afficher les objets présents dans la pièce.")
            
        return True
    
    def take(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de prendre un objet dans la pièce actuelle et de l'ajouter à son inventaire.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        current_room = player.current_room
        item_name = list_of_words[1]

        # Vérifier si l'objet est présent dans la pièce
        if item_name not in current_room.item:
            print(f"\nL'objet '{item_name}' n'est pas présent dans cette pièce.\n")
            return False

        # Prendre l'objet et vérifier s'il s'agit d'un personnage
        item = current_room.item.pop(item_name)
        if isinstance(item, (Character, Character2)):
            # Remettre l'objet dans la pièce car c'est un personnage
            current_room.item[item_name] = item
            print(f"\nVous ne pouvez pas prendre '{item_name}'. C'est un personnage, pas un objet.\n")
            return False

        # Ajouter l'objet à l'inventaire du joueur
        player.inventory[item_name] = item
        print(f"\nVous avez pris l'objet : '{item_name}'.\n")
        
        # Vérifier la capacité de poids
        if player.current_weight() > player.max_weight:
            # Retirer l'objet de l'inventaire du joueur et le remettre dans la pièce
            player.inventory.pop(item_name)
            current_room.item[item_name] = item
            print(f"\nVous ne pouvez pas prendre '{item_name}'. Vous dépassez la capacité maximale de poids ({player.max_weight} kg).\n")
            return False
        return True
    
        

    
    def drop(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de déposer un objet de son inventaire dans la pièce actuelle.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        current_room = player.current_room
        item_name = list_of_words[1]

        # Vérifier si l'objet est présent dans l'inventaire du joueur
        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans votre inventaire.\n")
            return False

        # Déposer l'objet dans la pièce et le retirer de l'inventaire du joueur
        item = player.inventory.pop(item_name)
        current_room.item[item_name] = item
        print(f"\nVous avez déposé l'objet : '{item_name}'.\n")
        return True
    
    def check(game, list_of_words, number_of_parameters):
        """
        Affiche l'inventaire du joueur sans que check prenne d'arguments.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        try:
            # Utiliser la représentation centralisée de l'inventaire fournie par Player.get_inventory()
            print(player.get_inventory())
        except Exception:
            print("Impossible d'afficher l'inventaire.")
        return True


    def charge(game, list_of_words, number_of_parameters):
        player = game.player
        if "beamer" not in player.inventory:
            print("\n Vous n'avez pas de beamer dans votre inventaire.\n")
            return False
        if len(list_of_words) < 2:
            print("\n Vous devez préciser un nom de slot.\n")
            return False
        slot_name = list_of_words[1]
        beamer = player.inventory["beamer"]
        beamer.charge(player, slot_name)
        return True


    def fire(game, list_of_words, number_of_parameters):
        player = game.player
        if "beamer" not in player.inventory:
            print("\n Vous n'avez pas de beamer dans votre inventaire.\n")
            return False
        if len(list_of_words) < 2:
            print("\n Vous devez préciser le nom du slot à utiliser.\n")
            return False
        slot_name = list_of_words[1]
        beamer = player.inventory["beamer"]
        beamer.fire(player, slot_name)
        return True

    
    def list_beamer(game, list_of_words, number_of_parameters):
        player = game.player
        if "beamer" not in player.inventory:
            print("\n Vous n'avez pas de beamer dans votre inventaire.\n")
            return False
        beamer = player.inventory["beamer"]
        beamer.list_slots()
        return True
       
    def characters(game, list_of_words, number_of_parameters):
        """
        Affiche la liste des personnages présents dans la pièce actuelle.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        player = game.player
        current_room = player.current_room
        characters_in_room = [item for item in current_room.item.values() if isinstance(item, (Character, Character2))]
        
        if not characters_in_room:
            print("Il n'y a personne ici.")
            return True
        
        print("Personnages présents dans cette pièce :")
        for character in characters_in_room:
            print(f"- {character.name} : {character.description}")
        
        return True   
        
    def talk(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de parler à un personnage dans la pièce actuelle.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        current_room = player.current_room
        character_name = list_of_words[1]

        # Vérifier si le personnage est présent dans la pièce
        if character_name not in current_room.item or not isinstance(current_room.item[character_name], (Character, Character2)):
            print(f"\nLe personnage '{character_name}' n'est pas présent dans cette pièce.\n")
            return False

        character = current_room.item[character_name]
        message = character.get_msg()
        if not message:
            print(f"\n{character.name} n'a rien à dire pour le moment.\n")
        
        return True
        
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True