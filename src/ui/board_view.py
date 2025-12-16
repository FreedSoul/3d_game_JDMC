from ursina import *
from src.core.engine import GameEngine
from src.core.constants import BOARD_WIDTH, BOARD_HEIGHT
from src.core.dataclasses import Pattern

class BoardView(Entity):
    def __init__(self, engine: GameEngine, action_log, on_summon_success_callback=None):
        super().__init__()
        self.engine = engine
        self.action_log = action_log
        self.on_summon_success_callback = on_summon_success_callback
        
        self.cells = {} # (x,y) -> Entity
        self.grid_width = 13
        self.grid_height = 19
        
        self.create_grid()
        self.update_visuals()
        
        # Placement State
        self.construction_mode = False
        self.current_pattern = None
        self.current_pattern_shape = [] # List of tuples
        self.current_rotation = 0
        self.ghost_entities = []
        self.pending_monster = None # Monster being summoned
        
        # Movement State
        self.move_highlights = []
        
        self.crest_counter = None # Will be set from main

    # ... (create_grid, input, update remain same) ...

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
            
            # Spawn a placeholder monster for testing immediately after placing!
            self.engine.summon_monster(self.engine.current_player_id, "TestMonster", origin_x, origin_y)
            
            # Finish placement
            self.construction_mode = False
            self.clear_ghost()
            self.update_visuals()
            
            # Deduct Summon Crests
            self.engine.deduct_summon_cost(cost=2)
            if self.crest_counter:
                self.crest_counter.update_stats()
            
            self.action_log.log(f"P{self.engine.current_player_id} Summoned Monster!")
            print("Placement Successful!")
            
            # Trigger Success Callback
            if self.on_summon_success_callback and self.pending_monster:
                self.on_summon_success_callback(self.pending_monster)
            
            self.pending_monster = None
        else:
            self.action_log.log("Invalid Placement!")
            print("Invalid Placement!")

    def on_cell_click(self, x, y):
        print(f"Clicked cell: {x}, {y}")
        
        # Movement / Selection Logic
        cell_data = self.engine.grid.get_cell(x, y)
        current_player = self.engine.get_current_player()
        print(f"DEBUG: Checking Selection... Cell Owner: {cell_data.monster_owner_id}, Current Player: {current_player.player_id}")
        
        # 1. Select Unit (Own Monster)
        if cell_data and cell_data.monster_id and cell_data.monster_owner_id == current_player.player_id:
            print(f"Selected Monster at {x}, {y}")
            self.selected_monster_pos = (x, y)
            
            # Highlight valid moves
            from src.core.dataclasses import DieFace
            move_power = current_player.crests.get(DieFace.MOVEMENT, 0)
            
            self.valid_moves = self.engine.grid.get_valid_moves(x, y, move_power, current_player.player_id)
            print(f"Valid Moves: {self.valid_moves}")
            self.highlight_valid_moves()
            return

        # 2. Action (Move or Attack)
        print(f"DEBUG: Checking Action. Selected: {getattr(self, 'selected_monster_pos', None)}")
        if hasattr(self, 'selected_monster_pos') and self.selected_monster_pos:
            print("DEBUG: Inside Action Block")
            sx, sy = self.selected_monster_pos
            
            # A. Attack?
            if cell_data.monster_id and cell_data.monster_owner_id != current_player.player_id:
                # Check Adjacency
                dist = abs(sx - x) + abs(sy - y)
                if dist == 1:
                    print(f"Attempting to attack {x}, {y}...")
                    success, msg = self.engine.execute_attack(sx, sy, x, y)
                    
                    if msg:
                        self.action_log.log(msg)
                        
                    if success:
                        print("Attack Successful!")
                        self.update_visuals()
                        if hasattr(self, 'crest_counter'):
                            self.crest_counter.update_stats()
                    else:
                        print("Attack Failed")
                        
                    # Deselect after attack attempt
                    self.selected_monster_pos = None
                    self.clear_highlights()
                    return

            # B. Move?
            if (x, y) in self.valid_moves:
                print(f"Moving to {x}, {y}")
                success = self.engine.execute_move(sx, sy, x, y)
                if success:
                    self.selected_monster_pos = None
                    self.valid_moves = []
                    self.clear_highlights()
                    self.update_visuals()
                    if hasattr(self, 'crest_counter'):
                        self.crest_counter.update_stats()
                else:
                    print("Move failed (cost issue?)")
            else:
                print("Invalid Move Destination or Action")
                self.selected_monster_pos = None
                self.clear_highlights()

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

    def input(self, key):
        if key == 'left mouse down':
            hit_entity = mouse.hovered_entity
            target_cell = None
            
            # 1. Did we hit a cell directly?
            if hit_entity in self.cells.values():
                target_cell = hit_entity
            # 2. Did we hit a child (like the monster sphere or highlight)?
            elif hit_entity and hit_entity.parent in self.cells.values():
                target_cell = hit_entity.parent
                
            if target_cell:
                x = int(target_cell.x)
                y = int(target_cell.z)
                
                if self.construction_mode:
                    self.try_place(x, y)
                else:
                    self.on_cell_click(x, y)
                    
        if self.construction_mode and key == 'r':
            self.current_rotation = (self.current_rotation + 1) % 4
            self.refresh_ghost()

    def update(self):
        if self.construction_mode:
            if mouse.hovered_entity and mouse.hovered_entity in self.cells.values():
                x = int(mouse.hovered_entity.x)
                y = int(mouse.hovered_entity.z)
                self.highlight_ghost(x, y)
            else:
                self.clear_ghost()

    # ... (start_placement, refresh_ghost, highlight_ghost, clear_ghost, try_place remain similar, skip to save tokens if possible, but replace needs context)
    # I will target the highlight methods specifically in a separate replacement or include them if range allows. 
    # Since I cannot skip valid code in replacement, I will assume the previous chunks are preserved and target specific methods if I split.
    # But I need to replace `input` which is early in file.
    
    # Let's do `input` and `__init__` first.


    def start_placement(self, pattern: Pattern, monster=None):
        self.construction_mode = True
        self.current_pattern = pattern
        self.current_rotation = 0
        self.pending_monster = monster
        print(f"Construction Mode ON: {pattern} for {monster}")

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



    def highlight_valid_moves(self):
        self.clear_highlights()
        for mx, my in self.valid_moves:
            if (mx, my) in self.cells:
                # Create highlight indicator (small sphere or quad)
                hl = Entity(
                    parent=self.cells[(mx, my)],
                    model='sphere',
                    color=color.azure,
                    scale=0.4,
                    position=(0, 0.1, -0.5), # Slightly above centered
                    always_on_top=True
                )
                self.move_highlights.append(hl)

    def clear_highlights(self):
        for hl in self.move_highlights:
            destroy(hl)
        self.move_highlights.clear()

    def update_visuals(self):
        # Sync visual state with engine state
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                cell_data = self.engine.grid.get_cell(x, y)
                visual_cell = self.cells.get((x, y))
                
                if cell_data and visual_cell:
                    # Reset base color
                    base_color = color.gray
                    if cell_data.owner_id == 1:
                        base_color = color.red
                    elif cell_data.owner_id == 2:
                        base_color = color.blue
                        
                    if cell_data.is_dungeon_master:
                        base_color = color.gold
                        
                    visual_cell.color = base_color
                    
                    # Monster Visuals (Simple Cube on top)
                    # For MVP we just tint the cell darker or add a child entity if not exists
                    # Let's interact with a child entity 'piece'
                    if not hasattr(visual_cell, 'piece'):
                        visual_cell.piece = None
                        
                    if cell_data.monster_id:
                        if not visual_cell.piece:
                            visual_cell.piece = Entity(parent=visual_cell, model='sphere', color=color.white, scale=0.5, position=(0,0,-0.5))
                        
                        # Color piece by owner
                        if cell_data.monster_owner_id == 1:
                            visual_cell.piece.color = color.pink
                        else:
                            visual_cell.piece.color = color.cyan
                    else:
                        if visual_cell.piece:
                            destroy(visual_cell.piece)
                            visual_cell.piece = None
