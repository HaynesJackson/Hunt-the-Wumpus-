from event import Event
from player import Player

# TODO Create Wumpus class here.

class Wumpus(Event):
    
    def __init__(self) -> None:
        super().__init__("Wumpus", "W", "A stench permeates the air.", False)


    def encounter(self, p: Player) -> bool:
        print("The Wumpus has eaten you!")
        p.die()
        return False

    def percept(self) -> str:
        return self._msg
    
    def get_symbol(self) -> str:
        return self._symbol
