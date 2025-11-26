from event import Event
from player import Player

# TODO Create BatSwarm class here.

class BatSwarm(Event):

    def __init__(self) -> None:
        super().__init__("Bat Swarm", "B", "You hear wings flapping.", False) 

    def encounter(self, p: Player) -> bool:
        print("You have become confused!")
        p.set_confused_turns(5)
        return False

    def percept(self) -> str:
        return self._msg
    
    def get_symbol(self) -> str:
        return self._symbol
