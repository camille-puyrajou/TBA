DEBUG = False

# Define the Player class.
class Player():

    """
    Represents the player in the game.

    This class manages the player's name, their current position in the game
    world (the room they are in), and their movements between rooms.

    Attributes :
        name (str) : The player's name.
        current_room (Room or None) : The room the player is currently in. It is None until the player is placed in a starting room.

    Methods :
        __init__(self, name) : The constructor.
        move(direction) : Moves the player in the given direction if an exit exists. Updates the current room and prints its full description. Returns True if the movement is successful, False otherwise.
    
    Examples:

    >>> player = Player("Alice")
    >>> player.current_room = room1
    >>> success = player.move("north")
    >>> if success:
    >>>     print("The player successfully moved!")
    >>> else:
    >>>     print("Movement failed!")
    The player successfully moved!
    """
    
    # Define the constructor.
    def __init__(self, name, max_weight=3.0):
        self.name = name
        self.current_room = None
         # In-memory history of rooms visited (initially empty)
        self.history = []
        # Inventory of items (initially empty). Structure: dict mapping item.name -> Item
        self.inventory = {}
        self.max_weight = max_weight
        self.quest_manager = QuestManager(self)


    # Define the log_history method.
    def log_history(self):
        try:
            room = self.current_room
        except Exception:
            room = None
        self.history.append(room)    
    
    def get_history(self):
        """
        Retourne une chaîne représentant l'historique des pièces visitées par le joueur.
        Exemple : '-Chambre 
                   -Couloir 
                   -Cuisine'
        """
        # Filtre les None éventuels et remplace par un token lisible
        if not self.history:
            return "Vous n'avez encore visité aucune pièce."

        lines = ["Vous avez déjà visité les pièces suivantes:"]
        for entry in self.history:
            if entry is None:
                label = 'Inconnu'
            else:
                # entry may be a Room instance or already a string
                try:
                    label = entry.name
                except Exception:
                    label = str(entry)
            lines.append(f"    - {label}")
        return "\n".join(lines)

    def get_inventory(self):
        """Retourne une chaîne représentant l'inventaire du joueur."""
        if not self.inventory: 
            return "Votre inventaire est vide."
        
        lines = ["Vous disposez des items suivants :"]
        for item in self.inventory.values():
            try:
                lines.append(f"    - {item.name} : {item.description} ({item.weight} kg)")
            except Exception:
                lines.append(f"    - {str(item)}")
        return "\n".join(lines)   


    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            try:
                from game import DEBUG
            except Exception:
                DEBUG = False
            if DEBUG:
                try:
                    print(f"DEBUG: move blocked (direction={direction})")
                except Exception:
                    pass
            print("\nCe chemin n'est pas accessible !\n")
            return False
        else:
            # perform move
            self.current_room = next_room
            
            print(f"DEBUG: moved to {next_room.name}")
            try:
                # Après un déplacement, n'affiche que la description courte (sans la liste d'objets).
                print(self.current_room.get_short_description())
            except Exception:
                pass


            # record movement (in-memory)
            try:
                self.log_history()
            except Exception:
                pass

            # afficher l'historique mis à jour après chaque déplacement
            try:
                print(self.get_history())
            except Exception:
                pass
            # L'inventaire du joueur n'est plus affiché automatiquement après un déplacement.
            # Il sera affiché uniquement via la commande 'look' ou 'inventory' explicite.
            return True
        
    def current_weight(self):
        """Calcule le poids total des objets dans l'inventaire du joueur."""
        total_weight = 0.0
        for item in self.inventory.values():
            try:
                total_weight += item.weight
            except Exception:
                pass
        return total_weight