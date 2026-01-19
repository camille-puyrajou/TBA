

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

from item import Item
import item
import player
from quests import Quest
import random
import time


class Actions:
    """
    The Actions class contains static methods that define the actions
    that can be performed in the game.
    """

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
        >>> game.setup("TestPlayer")
        >>> Actions.quit(game, ["quit"], 0)
        <BLANKLINE>
        Merci TestPlayer d'avoir joué. Au revoir.
        <BLANKLINE>
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        n = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if n != number_of_parameters + 1:
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
        >>> game.setup("TestPlayer")
        >>> Actions.help(game, ["help"], 0) # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        Voici les commandes disponibles:
            - help : afficher cette aide
            - quit : quitter le jeu
            - go <direction> : se déplacer dans une direction cardinale (N, E, S, O)
            - quests : afficher la liste des quêtes
            - quest <titre> : afficher les détails d'une quête
            - activate <titre> : activer une quête
            - rewards : afficher vos récompenses
        <BLANKLINE>
        True
        >>> Actions.help(game, ["help", "N"], 0)
        <BLANKLINE>
        La commande 'help' ne prend pas de paramètre.
        <BLANKLINE>
        False
        >>> Actions.help(game, ["help", "N", "E"], 0)
        <BLANKLINE>
        La commande 'help' ne prend pas de paramètre.
        <BLANKLINE>
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

        # Vérifier la capacité de poids
        if player.current_weight() + item.weight > player.max_weight:
            # Remettre l'objet dans la pièce
            current_room.item[item_name] = item
            print(f"\nVous ne pouvez pas prendre '{item_name}'. Vous dépassez la capacité maximale de poids ({player.max_weight} kg).\n")
            return False
        
        player.inventory[item_name] = item
        # --- Validation des fragments pour la quête des ruines ---
        if game.player.quest_manager.is_active("La Clé des Ruines"):
            if item_name in ["objet_brisé", "inscription_effacée", "fragment_ancien"]:
                print(f"Vous avez trouvé un fragment : {item_name} !")
                
                # Vérifier si c'est le dernier fragment avant de compléter
                quest = game.player.quest_manager.get_quest_by_title("La Clé des Ruines")
                nb_completed = len(quest.completed_objectives)
                nb_total = len(quest.objectives)
                
                if item_name not in quest.completed_objectives and nb_completed == nb_total - 1:
                    # C'est le dernier fragment, afficher les messages avant de compléter
                    print("\nLes fragments s'assemblent dans vos mains...")
                    print("Vous obtenez la Clé des Ruines !\n")
                    game.player.inventory["clé_des_ruines"] = Item("clé_des_ruines", "Une clé ancienne ouvrant la porte des ruines.", 0.1)
                
                game.player.quest_manager.complete_objective(item_name, "La Clé des Ruines")

        # Check for secrets quest objectives
        secrets_items = ["livre de sorts", "corne de licorne", "artefact"]
        if item_name in secrets_items:
            game.player.quest_manager.complete_objective(f"Trouver {item_name}")

            return True
    
        # --- Mini-quête : Collecte de plantes ---
        if item_name in ["plante_magique", "plante_magique2"]:
            print("\nVous avez trouvé une plante magique !")
            print("Vous gagnez 30 écus.\n")
            player.money += 30
            # Vérifier si Financer le voyage peut être complétée
            if game.player.quest_manager.is_active("Financer le voyage") and player.money >= 60 and not game.player.quest_manager.is_completed("Financer le voyage"):
                game.player.quest_manager.complete_objective("Gagner 60 écus", "Financer le voyage")
            if not game.player.quest_manager.is_active("Collecte de plantes"):
                game.player.quest_manager.activate_quest("Collecte de plantes")
            game.player.quest_manager.complete_objective("Récupérer plante", "Collecte de plantes")

        # --- Mini-quête : Obtenir le beamer ---
        if item_name == "beamer":
            print("\nVous avez obtenu le beamer magique !")
            print("Vous gagnez 30 écus.\n")
            player.money += 30
            # Vérifier si Financer le voyage peut être complétée
            if game.player.quest_manager.is_active("Financer le voyage") and player.money >= 60 and not game.player.quest_manager.is_completed("Financer le voyage"):
                game.player.quest_manager.complete_objective("Gagner 60 écus", "Financer le voyage")
            if not game.player.quest_manager.is_active("Obtenir le beamer"):
                game.player.quest_manager.activate_quest("Obtenir le beamer")
            game.player.quest_manager.complete_objective("Prendre beamer", "Obtenir le beamer")


        # --- Mini-quête : Souvenirs ---
        if item_name in ["pierre_gravée", "coquillage_bleu", "plume_dorée"]:
            if not game.player.quest_manager.is_active("Souvenirs du royaume"):
                game.player.quest_manager.activate_quest("Souvenirs du royaume")
            game.player.quest_manager.complete_objective(item_name, "Souvenirs du royaume")
            
            if game.player.quest_manager.is_completed("Souvenirs du royaume"):
                player.money += 30
                # Vérifier si Financer le voyage peut être complétée
                if game.player.quest_manager.is_active("Financer le voyage") and player.money >= 60 and not game.player.quest_manager.is_completed("Financer le voyage"):
                    game.player.quest_manager.complete_objective("Gagner 60 écus", "Financer le voyage")

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
        
    def start_sorcerer_battle(game, player):
        """
        Lance un combat interactif contre le sorcier Zeph avec système de tours et de chance de toucher.
        
        Args:
            game (Game): L'objet jeu
            player (Player): Le joueur
            
        Returns:
            bool: True si le joueur gagne, False s'il perd
        """
        # Initialisation des statistiques du sorcier
        sorcerer_hp = 80
        sorcerer_max_hp = 80
        player_accuracy = 0.70  
        sorcerer_accuracy = 0.55  
        player_min_damage = 8
        player_max_damage = 18
        sorcerer_min_damage = 10
        sorcerer_max_damage = 20
        
        # Réinitialiser les PV du joueur pour ce combat
        player.hp = player.max_hp
        
        print(f"\n{'='*50}")
        print(f"COMBAT - {player.name} vs Zeph le Sorcier")
        print(f"{'='*50}\n")
        print(f"🧙 Zeph : {sorcerer_hp}/{sorcerer_max_hp} PV")
        print(f"⚔️  Vous : {player.hp}/{player.max_hp} PV\n")
        
        turn = 0
        
        while player.hp > 0 and sorcerer_hp > 0:
            turn += 1
            print(f"\n--- Tour {turn} ---\n")
            
            # TOUR DU JOUEUR
            print("🎯 Votre tour !")
            player_action = input("Attaquer (a) ou Défendre (d) ? : ").lower().strip()
            
            if player_action == "d":
                # Défendre réduit les dégâts reçus
                defense_bonus = 0.5
                print("Vous vous préparez à la défense...\n")
            else:
                defense_bonus = 1.0
                # Attaquer
                if random.random() < player_accuracy:
                    damage = random.randint(player_min_damage, player_max_damage)
                    sorcerer_hp -= damage
                    print(f"✅ Coup critique ! Vous infligez {damage} dégâts au sorcier !")
                else:
                    print(f"❌ Manqué ! Le sorcier esquive votre attaque.")
            
            print(f"🧙 Zeph : {max(0, sorcerer_hp)}/{sorcerer_max_hp} PV")
            
            if sorcerer_hp <= 0:
                print(f"\n{'='*50}")
                print("🎉 VICTOIRE ! Vous avez vaincu Zeph !")
                print(f"{'='*50}\n")
                player.hp = max(1, player.hp)  # Assurer que le joueur a au moins 1 PV
                return True
            
            time.sleep(1)
            
            # TOUR DU SORCIER
            print(f"\n🧙 Tour du sorcier !\n")
            time.sleep(0.5)
            
            if random.random() < sorcerer_accuracy:
                damage = random.randint(sorcerer_min_damage, sorcerer_max_damage)
                damage = int(damage * defense_bonus)
                player.hp -= damage
                print(f"⚡ Le sorcier vous attaque ! {damage} dégâts reçus !")
            else:
                print(f"🛡️  Vous esquivez l'attaque du sorcier !")
            
            print(f"⚔️  Vous : {max(0, player.hp)}/{player.max_hp} PV")
            
            if player.hp <= 0:
                print(f"\n{'='*50}")
                print("💀 DÉFAITE ! Vous avez été vaincu...")
                print(f"{'='*50}\n")
                return False
            
            time.sleep(1)
        
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

        # Quête : Financer le voyage (acheter un bateau)
        if character.name == "Pêcheur":
            # Si la quête n'est pas encore active
            if not game.player.quest_manager.is_active("Financer le voyage"):
                print("\nPêcheur : Si tu veux prendre la mer, cela va coûter 60 écus.")
                print("Nouvelle quête activée : Financer le voyage.\n")
                game.player.quest_manager.activate_quest("Financer le voyage")
                return True
            
            # Si la quête est active mais pas assez d'argent
            if game.player.money < 60:
                print("\nPêcheur : Tu n'as pas encore assez d'écus.")
                return True

            # Si le joueur a assez d'argent → compléter la quête
            if not game.player.quest_manager.is_completed("Financer le voyage"):
                game.player.quest_manager.complete_objective("Gagner 60 écus", "Financer le voyage")
                print("\nPêcheur : Excellent ! Tu as assez d'écus. Bienvenue à bord moussaillon !")
                print("Vous avez maintenant accès au bateau.\n")
                return True
            
            # Si la quête est déjà complétée
            print("\nPêcheur : Bon voyage matelot !")
            return True

        # --- Quête : La Clé des Ruines --- (Esprit)
        if character.name == "Esprit":
            if not game.player.quest_manager.is_active("La Clé des Ruines"):
                print("\nL'esprit murmure : 'La porte ne s'ouvrira qu'avec trois fragments...'")
                print("Nouvelle quête activée : La Clé des Ruines.\n")
                game.player.quest_manager.activate_quest("La Clé des Ruines")
                return True
            
        # Si la quête est active, vérifier les fragments
            if game.player.quest_manager.is_active("La Clé des Ruines"):
                quest = game.player.quest_manager.get_quest_by_title("La Clé des Ruines")
                completed_count = len(quest.completed_objectives)
                total_count = len(quest.objectives)
                if completed_count < total_count:
                    missing = [obj for obj in quest.objectives if obj not in quest.completed_objectives]
                    print(f"\nL'esprit dit : 'Il te manque encore les fragments suivants : {', '.join(missing)}.'\n")
                    return True
                # Si tous les fragments sont collectés
                print("\nL'esprit sourit : 'Tu as rassemblé tous les fragments. La porte s'ouvre pour toi...'")
                print("Vous obtenez la Clé des Ruines !\n")
                game.player.inventory["clé_des_ruines"] = Item("clé_des_ruines", "Une clé ancienne ouvrant la porte des ruines.", 0.1)
                game.player.quest_manager.complete_quest("La Clé des Ruines")
                return True

        # --- Quête : Le Secret du Sorcier --- (Zeph)
        if character.name == "Zeph":
            if not game.player.quest_manager.is_active("Le Secret du Sorcier"):
                print("\nZeph vous regarde avec un sourire énigmatique...")
                print("Zeph : Ainsi, tu as trouvé mon repaire. Mais connais-tu vraiment mon secret ?\n")
                game.player.quest_manager.activate_quest("Le Secret du Sorcier")


        # --- Mini-quête : Parler à 5 PNJ ---
        if not hasattr(player, "talk_count"):
            player.talk_count = 0

        player.talk_count += 1
        if player.talk_count == 5:
            print("\nVous avez parlé à 5 personnes !")
            print("Vous gagnez 20 écus.\n")
            player.money += 20
            # Vérifier si Financer le voyage peut être complétée
            if game.player.quest_manager.is_active("Financer le voyage") and player.money >= 60 and not game.player.quest_manager.is_completed("Financer le voyage"):
                game.player.quest_manager.complete_objective("Gagner 60 écus", "Financer le voyage")
            game.player.quest_manager.complete_objective("Parler à 5 PNJ", "Rencontrer les habitants")


        # --- Combat contre le sorcier Zeph ---
        if character.name == "Zeph":
            print("\nLe sorcier vous fixe intensément...")
            print("Une aura sombre vous entoure... Le combat commence !\n")
            choix = input("Voulez-vous combattre (oui/non) : ").lower()
            # --- Victoire/Défaite au combat ---
            if choix == "oui":
                # Lancer le combat interactif
                player_won = Actions.start_sorcerer_battle(game, player)
                
                if player_won:
                    print("Vous avez découvert son secret : il cherchait à protéger le royaume des vraies menaces !")
                    
                    # Complete the sorcerer secret quest
                    game.player.quest_manager.complete_objective("Découvrir le secret de Zeph", "Le Secret du Sorcier")
                    
                    # Complete main quest objectives
                    game.player.quest_manager.complete_objective("Atteindre le repère du sorcier", "Vaincre le Sorcier")
                    game.player.quest_manager.complete_objective("Vaincre le sorcier", "Vaincre le Sorcier")
                    
                    # Check if main quest is completed and end game
                    if game.player.quest_manager.is_completed("Vaincre le Sorcier"):
                        print("\n 🎉 FÉLICITATIONS ! Vous avez vaincu le sorcier et sauvé le royaume !")
                        print("Vous êtes téléporté devant le château en héros...\n")
                        
                        # Find the Chateau room and teleport player there
                        for room in game.rooms:
                            if room.name == "Chateau":
                                game.player.current_room = room
                                break
                        
                        print("\n===== VICTOIRE ! =====\n")
                        game.finished = True
                else:
                    print("\n===== GAME OVER =====\n")
                    game.finished = True

            # --- Refus du combat ---
            else:
                print("\nVous refusez le combat...")
                print("Le sorcier lève sa main... Une explosion vous frappe de plein fouet !")
                print("\n===== GAME OVER =====\n")
                game.finished = True

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
        print(game.player.show_rewards())
        return True