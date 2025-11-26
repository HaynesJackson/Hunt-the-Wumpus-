from event import Event
from player import Player
# TODO Create EscapeRope class here

class EscapeRope(Event):
    def __init__(self) -> None:
        super().__init__(
                "Escape Rope", 
                "R", 
                "This place looks familiar...", 
                False
            )

    def encounter(self, p: Player) -> bool:
        if p.get_treasure():
            print("You have reached the rope and successfully escaped the wumpus!")
            p.die()
        return False # Does not go away

    def percept(self) -> str:
        return self._msg
        
    def get_symbol(self) -> str:
        return self._symbol

