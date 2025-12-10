from typing import List, Tuple, Optional
from src.core.constants import BOARD_WIDTH, BOARD_HEIGHT
from src.core.dataclasses import Pattern

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.owner_id: Optional[int] = None
        self.monster_id: Optional[str] = None # ID of the monster occupying this cell
        self.monster_owner_id: Optional[int] = None # Player ID who owns the monster
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

    def is_walkable(self, x: int, y: int, player_id: int) -> bool:
        """
        A cell is walkable if:
        1. It is within bounds.
        2. It has an owner (is part of the dungeon).
           NOTE: In DDM, you can walk on enemy terrain.
        3. It is NOT occupied by an ENEMY monster.
        """
        cell = self.get_cell(x, y)
        if not cell:
            return False
        if cell.owner_id is None:
            return False # Not part of dungeon
        
        # Check occupancy
        if cell.monster_id:
             # TODO: Need to know if monster is friendly or enemy. 
             # For Grid level, we might just store owner_id of the monster or need a way to look it up.
             # For now, let's assume we can pass if it's NOT an enemy.
             # We need to pass the monster logic or store owner in cell.
             # Let's add 'monster_owner_id' to Cell for easier checking.
             if cell.monster_owner_id != player_id:
                 return False # Enemy blocks
        
        return True

    def get_valid_moves(self, start_x: int, start_y: int, max_steps: int, player_id: int) -> List[Tuple[int, int]]:
        """
        Returns all reachable (x, y) coordinates within max_steps.
        BFS implementation.
        """
        valid_destinations = []
        queue = [(start_x, start_y, 0)] # (x, y, dist)
        visited = set([(start_x, start_y)])
        
        while queue:
            cx, cy, dist = queue.pop(0)
            
            # If we have moves left, explore neighbors
            if dist < max_steps:
                neighbors = [
                    (cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)
                ]
                for nx, ny in neighbors:
                    if (nx, ny) in visited:
                        continue
                    
                    if self.is_walkable(nx, ny, player_id):
                        visited.add((nx, ny))
                        queue.append((nx, ny, dist + 1))
                        
                        # Can we STOP here?
                        # Cannot stop on ANY monster (friend or foe)
                        n_cell = self.get_cell(nx, ny)
                        if n_cell and n_cell.monster_id is None:
                            valid_destinations.append((nx, ny))
                            
        return valid_destinations
    
    def move_monster(self, from_x: int, from_y: int, to_x: int, to_y: int):
        source = self.get_cell(from_x, from_y)
        dest = self.get_cell(to_x, to_y)
        
        if source and dest:
            dest.monster_id = source.monster_id
            dest.monster_owner_id = source.monster_owner_id
            
            source.monster_id = None
            source.monster_owner_id = None
