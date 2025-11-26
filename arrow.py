from event import Event
from player import Player

# TODO Create Arrow class here

class Arrow(Event):
    def __init__(self) -> None:
        super().__init__(
                "Arrow",
                "A",
                "You step on something sharp. Ouch!",
                True
            )

    def encounter(self, p: Player) -> bool:
        print("You found an arrow")
        p.add_arrow()
        return True

    def percept(self) -> str:
        return self._msg
    
    def get_symbol(self) -> str:
        return self._symbol
