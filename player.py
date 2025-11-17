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
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    