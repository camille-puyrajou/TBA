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
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        
    def log_history(self):
        try:
            room = self.current_room
        except Exception:
            room = None
        self.history.append(room)

    def get_history(self):
        if not self.history:
            return "Vous n'avez encore visité aucune pièce."
        
        lines = ["Vous avez déjà visité les pièces suivantes :"]
        for n in self.history:
            room = n if n is not None else 'Inconnu'
            lines.append(f"    - {room.name}")
        return "\n".join(lines)
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nCe chemin n'est pas accessible !\n")
            return False
        else:
            # perform move
            self.current_room = next_room
            try:
                print(self.current_room.get_long_description())
            except Exception:
                pass

             # afficher l'inventaire de la pièce actuelle
            try:
                print(self.current_room.get_inventory())
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

            try:
                print("\n"+self.get_inventory())
            except Exception:
                pass

            return True
        
    def inventory(self):
        self.inventory = {}

    def get_inventory(self):
        """ 
        Retourne l'inventaire du joueur.
        """
        if not self.inventory:
            return "Votre inventaire est vide."
        
        else :
            lines = ["Vous disposez des items suivants :"]
            for n in self.inventory:
                item = n if n is not None else 'Inconnu'
                lines.append(f"    - {item.name} : {item.description}, ({item.weight} kg)")
            return "\n".join(lines)