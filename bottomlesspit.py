from event import Event
from player import Player
import random

# TODO Create BottomlessPit class here.

class BottomlessPit(Event):
    def __init__(self) -> None:
        super().__init__("Bottomless Pit", "P", "You feel a breeze.", False)

    def encounter(self, p: Player) -> bool:
        if self._fall():
            print("You fell in to the bottomless pit and died!")
            p.die()
        else:
            print("You almost fell in to the bottomless pit, but survived!")
        return False  # event stays in room

    def percept(self) -> str:
        return self._msg
    
    def _fall(self) -> bool:
        return random.random() < 0.5

    def get_symbol(self) -> str:
        return self._symbol
