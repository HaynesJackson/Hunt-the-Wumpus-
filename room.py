from typing import Optional
from event import Event

class Room:
    _event: Optional[Event]

    def __init__(self, event: Optional[Event] = None) -> None:
        self._event = event

    def get_event(self) -> Optional[Event]:
        return self._event

    def set_event(self, event: Optional[Event]) -> None:
        self._event = event

    def is_empty(self) -> bool:
        return self._event is None
