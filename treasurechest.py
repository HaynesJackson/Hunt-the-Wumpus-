from event import Event
from player import Player

# TODO Create TreasureChest class here.

class TreasureChest(Event):
    def __init__(self) -> None:
        super().__init__(
                "Treasure Chest", 
                "T",
                "You see something shimmer in the distance",
                True
            )

    def encounter(self, p: Player) -> bool:
        print("You have picked up the treasure chest!")
        p.set_treasure()
        return True # Remove the chest from game board

    def percept(self) -> str:
        return self._msg
    
    def get_symbol(self) -> str:
        return self._symbol
