from typing import List, Tuple, Optional
from src.core.constants import BOARD_WIDTH, BOARD_HEIGHT
from src.core.dataclasses import Pattern

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.owner_id: Optional[int] = None
        self.monster_id: Optional[str] = None # ID of the monster occupying this cell
        self.is_dungeon_master: bool = False

class Grid:
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.cells: List[List[Cell]] = [
            [Cell(x, y) for y in range(self.height)]
            for x in range(self.width)
        ]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x][y]
        return None

    def set_owner(self, x: int, y: int, player_id: int):
        cell = self.get_cell(x, y)
        if cell:
            cell.owner_id = player_id

    def rotate_pattern(self, pattern: Pattern, rotations: int = 0) -> List[Tuple[int, int]]:
        """
        Rotates the pattern 90 degrees clockwise 'rotations' times.
        """
        coords = pattern.shape
        for _ in range(rotations % 4):
            # Rotate 90 degrees clockwise: (x, y) -> (y, -x)
            coords = [(y, -x) for x, y in coords]
        return coords

    def validate_dimension(self, 
                         player_id: int, 
                         pattern: Pattern, 
                         origin_x: int, 
                         origin_y: int,
                         rotations: int = 0) -> bool:
        """
        Validates if a pattern can be placed at the given origin.
        """
        rotated_shape = self.rotate_pattern(pattern, rotations)
        
        # Calculate absolute coordinates
        abs_coords = []
        for dx, dy in rotated_shape:
            abs_x = origin_x + dx
            abs_y = origin_y + dy
            abs_coords.append((abs_x, abs_y))

        # 1. Check Boundaries & Collisions
        for x, y in abs_coords:
            cell = self.get_cell(x, y)
            if not cell:
                return False # Out of bounds
            if cell.owner_id is not None:
                return False # Already occupied

        # 2. Check Adjacency (Must touch own territory)
        # For the very first turn, special rules might apply (touching DM), 
        # but generally it must touch a cell owned by player_id.
        has_adjacency = False
        for x, y in abs_coords:
            neighbors = [
                (x+1, y), (x-1, y), (x, y+1), (x, y-1)
            ]
            for nx, ny in neighbors:
                n_cell = self.get_cell(nx, ny)
                if n_cell and n_cell.owner_id == player_id:
                    has_adjacency = True
                    break
            if has_adjacency:
                break
        
        return has_adjacency

    def apply_dimension(self, player_id: int, pattern: Pattern, origin_x: int, origin_y: int, rotations: int = 0):
        """
        Applies the pattern to the grid, setting ownership.
        Assumes validation has already passed.
        """
        rotated_shape = self.rotate_pattern(pattern, rotations)
        for dx, dy in rotated_shape:
            self.set_owner(origin_x + dx, origin_y + dy, player_id)
