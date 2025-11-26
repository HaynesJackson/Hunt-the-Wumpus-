class Player:
    _row: int
    _col: int
    _alive: bool
    _has_treasure: bool
    _arrows: int
    _confused_turns: int

    def __init__(self, row: int, col: int) -> None:
        self._row = row
        self._col = col
        self._alive = True
        self._has_treasure = False
        self._arrows = 0
        self._confused_turns = 0

    def get_row(self) -> int:
        return self._row

    def set_row(self, new_row: int) -> None: 
        self._row = new_row

    def get_col(self) -> int:
        return self._col

    def set_col(self, new_col: int) -> None:
        self._col = new_col

    def die(self) -> None:
        self._alive = False
        # Game._end_game()

    def is_alive(self) -> bool:
        return self._alive

    def add_arrow(self) -> None:
        self._arrows += 1
    
    def get_arrow(self) -> int:
        return self._arrows
    
    def lose_arrow(self) -> None:
        self._arrows += -1

    def set_confused_turns(self, turns: int) -> None:
        self._confused_turns = turns

    def get_confused_turns(self) -> int:
        return self._confused_turns

    def set_treasure(self) -> None:
        self._has_treasure = True

    def get_treasure(self) -> bool:
        return self._has_treasure
    
    def reduce_confusion(self) -> None:
        if self._confused_turns > 0:
            self._confused_turns -= 1





