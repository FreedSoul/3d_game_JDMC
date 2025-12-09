from ursina import *
from src.core.engine import GameEngine
from src.core.constants import BOARD_WIDTH, BOARD_HEIGHT
from src.core.dataclasses import Pattern

class BoardView(Entity):
    def __init__(self, engine: GameEngine):
        super().__init__()
        self.engine = engine
        self.cells = {} # Map (x, y) -> Entity
        self.create_grid()
        self.update_visuals()
        
        # Placement State
        self.is_placing = False
        self.current_pattern: Pattern = None
        self.current_rotation = 0
        self.ghost_entities = []

    def create_grid(self):
        # Create the 13x19 grid
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                # Create a visual cell
                cell = Entity(
                    parent=self,
                    model='quad',
                    texture='white_cube',
                    color=color.gray,
                    scale=0.9,
                    position=(x, 0, y), 
                    rotation_x=90,
                    collider='box'
                )
                self.cells[(x, y)] = cell
                # cell.on_click is handled by global input or mouse.hovered_entity check

    def input(self, key):
        if not self.is_placing:
            return
            
        if key == 'r':
            self.current_rotation = (self.current_rotation + 1) % 4
            self.refresh_ghost()
            
        if key == 'left mouse down':
            if mouse.hovered_entity in self.cells.values():
                # Get the cell coordinates
                # We can deduce x,y from position since we mapped it 1:1
                x = int(mouse.hovered_entity.x)
                y = int(mouse.hovered_entity.z)
                self.try_place(x, y)

    def update(self):
        if self.is_placing:
            if mouse.hovered_entity and mouse.hovered_entity in self.cells.values():
                x = int(mouse.hovered_entity.x)
                y = int(mouse.hovered_entity.z)
                self.highlight_ghost(x, y)
            else:
                self.clear_ghost()

    def start_placement(self, pattern: Pattern):
        self.is_placing = True
        self.current_pattern = pattern
        self.current_rotation = 0

    def refresh_ghost(self):
        # Triggered on rotation, re-highlight current position if mouse is hovering
        if mouse.hovered_entity:
            x = int(mouse.hovered_entity.x)
            y = int(mouse.hovered_entity.z)
            self.highlight_ghost(x, y)

    def highlight_ghost(self, origin_x, origin_y):
        self.clear_ghost()
        
        # Get rotated shape
        shape = self.engine.grid.rotate_pattern(self.current_pattern, self.current_rotation)
        
        # Validate first to decide color
        is_valid = self.engine.grid.validate_dimension(
            self.engine.current_player_id,
            self.current_pattern,
            origin_x,
            origin_y,
            self.current_rotation
        )
        if is_valid:
            ghost_color = color.rgba(color.green.r, color.green.g, color.green.b, 0.3)
        else:
            ghost_color = color.rgba(color.red.r, color.red.g, color.red.b, 0.3)

        for dx, dy in shape:
            abs_x = origin_x + dx
            abs_y = origin_y + dy
            
            if (abs_x, abs_y) in self.cells:
                # Create a temporary ghost entity overlay
                ghost = Entity(
                    parent=self,
                    model='quad',
                    color=ghost_color,
                    scale=0.9,
                    position=(abs_x, 0.1, abs_y), # Slightly above grid
                    rotation_x=90,
                    always_on_top=True
                )
                self.ghost_entities.append(ghost)

    def clear_ghost(self):
        for e in self.ghost_entities:
            destroy(e)
        self.ghost_entities.clear()

    def try_place(self, origin_x, origin_y):
        if self.engine.grid.validate_dimension(
            self.engine.current_player_id, 
            self.current_pattern, 
            origin_x, 
            origin_y, 
            self.current_rotation
        ):
            # Apply to Core
            self.engine.grid.apply_dimension(
                self.engine.current_player_id, 
                self.current_pattern, 
                origin_x, 
                origin_y, 
                self.current_rotation
            )
            # Finish placement
            self.is_placing = False
            self.clear_ghost()
            self.update_visuals()
            print("Placement Successful!")
        else:
            print("Invalid Placement!")

    def on_cell_click(self, x, y):
        print(f"Clicked cell: {x}, {y}")

    def update_visuals(self):
        # Sync visual state with engine state
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                cell_data = self.engine.grid.get_cell(x, y)
                visual_cell = self.cells.get((x, y))
                
                if cell_data and visual_cell:
                    if cell_data.owner_id == 1:
                        visual_cell.color = color.red
                    elif cell_data.owner_id == 2:
                        visual_cell.color = color.blue
                    else:
                        visual_cell.color = color.gray
                    
                    if cell_data.is_dungeon_master:
                        visual_cell.color = color.gold
