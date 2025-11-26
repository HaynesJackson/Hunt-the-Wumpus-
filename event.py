# TODO Create abstract Event class here. Remember to inherit from ABC and
# decorate abstract methods with @abstractmethod

from abc import ABC, abstractmethod
from player import Player

class Event(ABC):

    _name: str
    _symbol: str
    _msg: str
    _removable: bool

    def __init__(self, name: str, symbol: str, msg: str, removable: bool):
        self._name = name
        self._symbol = symbol
        self._msg = msg
        self._removable = removable

    @abstractmethod
    def encounter(self, p: Player) -> bool:
        pass

    @abstractmethod
    def percept(self) -> str:
        pass
    
    def get_symbol(self) -> str:
        return self._symbol
