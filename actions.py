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

        Examples:
        
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
                    
        # Afficher la description de la nouvelle pièce (et donc ses sorties)
        print(game.player.current_room.get_long_description()) 
        game.player.current_room.get_long_description()
        
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
            print("Vous disposez des items suivants:")
            if not player.inventory:
                print("\nVotre inventaire est vide.\n")
            else:
                for item in player.inventory.values():
                    print(f"    - {item} : {item.description}, ({item.weight} kg)")
        except Exception:
            print("Impossible d'afficher l'inventaire.")
        return True