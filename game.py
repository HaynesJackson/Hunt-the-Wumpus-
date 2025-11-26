from event import Event
from wumpus import Wumpus
from bottomlesspit import BottomlessPit
from batswarm import BatSwarm
from escaperope import EscapeRope
from treasurechest import TreasureChest
from arrow import Arrow

from player import Player
from room import Room

from typing import Optional, List, Type

import os
import random

class Game:
    _rows: int
    _cols: int
    _debug: int
    _cave: list[list[Room]]
    _player: Player
    _game_over: bool

    def __init__(self) -> None:
        clear_terminal()
        self._rows = self._ask_dimension("How many rows should the cave have? ")
        self._cols = self._ask_dimension("How many columns should the cave have? ")
        self._debug = self._ask_debug()
        self._cave = self._create_cave(self._rows, self._cols)
        rope_coords = self._place_event(EscapeRope, 1)
        rope_r = rope_coords[0]
        rope_c = rope_coords[1]
        self._player = Player(rope_r, rope_c)
        self._place_event(Wumpus, 1)
        self._place_event(TreasureChest, 1)
        self._place_event(BottomlessPit, 2)
        self._place_event(BatSwarm, 2)
        self._place_event(Arrow, 3)
        self._game_over = False
        self._play()

    def _place_event(self, event: Optional[Type[Event]], count: int) -> List[int]:
        coords = [0, 0]
        for x in range(count):
            r, c = self._find_empty_room(self._cave)
            if event is not None:
                self._cave[r][c].set_event(event()) # type: ignore
            else:
                self._cave[r][c].set_event(None)
            coords = [r, c]

        return coords

    def end_game(self) -> None:
        self._game_over = False

    def _find_empty_room(self, cave: list[list[Room]]) -> list[int]:
        while True:
            random_row = random.randint(0, len(cave) - 1)
            random_col = random.randint(0, len(cave[0]) - 1)
            if cave[random_row][random_col].is_empty():
                return [random_row, random_col]

    def _play(self) -> None:
        while not self._game_check():
            self._game_check()
            self._print_map()
            self._move_player()
            if self._game_check():
                break
            self._check_percept()
            self._check_encounter()
            clear_terminal()
        print('Thank you for playing.')
    
    def _check_encounter(self) -> None:
        r = self._player.get_row()
        c = self._player.get_col()
        event = self._cave[r][c].get_event()
        if event is None:
            return
        else:
            clear_terminal()
            self._print_map()
            removable = event.encounter(self._player)
            if removable:
                self._cave[r][c].set_event(None)
            self._continue_input('x')

    def _check_percept(self) -> bool:
        percepts: list[str] = []
        clear_terminal()
        self._print_map()
        r = self._player.get_row()
        c = self._player.get_col()
        direction_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x in direction_list:
            new_row = r + x[0]
            new_col = c + x[1]
            if new_row >= 0 and new_row < self._rows:
                if new_col >= 0 and new_col < self._cols:
                    event = self._cave[new_row][new_col].get_event()
                    if event is not None:
                        percepts.append(event.percept())
        if len(percepts) > 0:
            for y in range(len(percepts)):
                print(percepts[y])
            self._continue_input('x')
            return True
        else: return False

    def _ask_direction(self) -> str:
        valid_inputs = ['w', 'd', 's','a']
        valid = False
        while not valid:
            if self._player.get_arrow() != 0:
                player_move = input('Next move? WASD - Up, Down, Left, Right or F - Shoot Arrow: ').lower()
                if player_move in valid_inputs or player_move == 'f':
                    valid = True
                else:
                    print('Please enter a valid character!')

            else:
                player_move = input('Next move? WASD - Up, Down, Left, Right: ').lower()
                if player_move in valid_inputs:
                    valid = True
                else:
                    if player_move == 'f':
                        print("You don't have any arrows! Please re-enter a valid input.")
                    else:
                        print('Please enter a valid character!')
        return player_move
            

    def _continue_input(self, d: str) -> None:
        if d != 'x':
            print('Invalid input! ' + d)
        input('Press enter to continue...')
        
    def _ask_direction(self) -> str:
        valid_inputs = ['w', 'd', 's','a']
        valid = False
        while not valid:
            player_move = input('Next move? WASD - Up, Down, Left, Right: ').lower()
            valid = True if player_move in valid_inputs else False
        return player_move
            
    def _move_player(self) -> None:
        action = self._ask_direction()
        if action == 'w': direction = 'up'
        elif action == 's': direction = 'down'
        elif action == 'a': direction = 'left'
        elif action == 'd': direction = 'right'
        if self._player.can_move(direction):
            self._player.move(direction)
        else:
            self._continue_input('You cannot move in that direction!')

    def _ask_shooting_direction(self) -> str:
        valid_inputs = ['w', 'd', 's', 'a']
        valid = False
        while not valid:
            shoot_direction = input('Which direction to shoot the arrow? WASD - Up, Down, Left, Right: ').lower()
            if shoot_direction in valid_inputs:
                valid = True
            else:
                print('Please enter a valid character')

        return shoot_direction


    def _shoot_arrow(self) -> None:
        row = self._player.get_row()
        col = self._player.get_col()
        direction = self._ask_shooting_direction()

        # Find the direction of the arrow to shoot to
        if direction == 'w': dr = -1; dc = 0; leng = min(3, row) 
        elif direction == 's': dr = 1; dc = 0; leng = min(3, self._rows - 1 - row)
        elif direction == 'd': dr = 0; dc = 1; leng = min(3, self._cols - 1 - col)
        elif direction == 'a': dr = 0; dc = -1; leng = min(3, col)
        for x in range(1, leng + 1): 
            r = row + dr * x
            c = col + dc * x
            event = self._cave[r][c].get_event()
            if isinstance(event, Wumpus):
                self._shot_wumpus()
                return
        self._player.lose_arrow()
        if self._player.get_arrow() == 0:
            print('You have run out of arrows!')
            self._continue_input('x')


    def _game_check(self) -> bool:
        if not self._player.has_won():
            self._game_over = True
        return self._game_over

    def _shot_wumpus(self) -> None:
        print('The wumpus is defeated.')
        self._continue_input('x')
        self._game_over = True
        
    def _create_cave(self, rows: int, cols: int) -> list[list[Room]]:
        cave: list[list[Room]] = []
        for row in range(rows):
            row_list = []
            for col in range(cols):
                row_list.append(Room())
            cave.append(row_list)
        return cave

    def _ask_debug(self) -> int:
        valid = False
        while not valid:
            try:
                user_input = int(input("Debug mode? (0 - No, 1 - Yes) "))
                if user_input == 0 or user_input == 1:
                    valid = True
                else:
                    print('Please enter a 0 or 1!')
            except ValueError:
                print("That's not even a number! Try again.")
        return user_input

    def _ask_dimension(self, prompt: str) -> int:
        valid = False
        while not valid:
            try:
                user_input = int(input(prompt))
                if 4 <= user_input <= 20:
                    valid = True
                else:
                    print("Please enter a number between 4 and 20!")
               
            except ValueError:
                print("That's not even a number! Please try again")
        return user_input
    
    def _print_map(self) -> None:
        rows = self._rows
        cols = self._cols

        horizontal = "-" * ((cols * 3) + 1)
        for r in range(rows):
            print(horizontal)
            row_str = ""
            for c in range(cols):
                event = self._cave[r][c].get_event()
            
                if self._player._row == r and self._player._col == c:
                    if self._debug == 1:
                        if event is None:
                            row_str += "|* "
                        else:
                            row_str += f'|*{event.get_symbol()}'
                    else:
                        row_str += "|* "
                else:
                    if self._debug == 1:
                        if event is None:
                            row_str += "|  "
                        else:
                            row_str += f'| {event.get_symbol()}'
                    else:
                        row_str += "|  "
        
            row_str += "|"
            print(row_str)
        print(horizontal)

def clear_terminal() -> None:
    if os.name == 'nt': # Copied from snake game assignment
        os.system('cls')
    else:
        os.system('clear')
