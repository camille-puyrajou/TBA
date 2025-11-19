# Define the Room class.

class Room:
    """
    Represents a location in the game world.

    A Room has a name, a description, and a set of exits that connect it to other rooms. Exits are stored in a dictionary mapping directions
    (e.g., "north", "east") to other Room instances.

    Attributes :
    name (str) : The name of the room.
    description (str) : A textual description of the room, used to inform the player of their surroundings.
    exits (dict[str, Room]) : A dictionary mapping directions to the connected rooms. A direction with value None indicates that no room exists in that direction.

    Methods : 
    get_exit(direction): Returns the room connected in the given direction, or None if no exit exists.
    
    get_exit_string(): Returns a formatted string listing the available exits in this room.
    
    get_long_description(): Returns a full description of the room, including its text description and the list of exits.
    """
    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
