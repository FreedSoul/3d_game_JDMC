from ursina import *
from src.core.engine import GameEngine

from src.core.patterns_registry import PATTERNS

class HUD(Entity):
    def __init__(self, engine: GameEngine, on_roll_callback, on_pattern_selected_callback, on_end_turn_callback):
        super().__init__(parent=camera.ui)
        self.engine = engine
        self.on_roll_callback = on_roll_callback
        self.on_pattern_selected_callback = on_pattern_selected_callback
        self.on_end_turn_callback = on_end_turn_callback
        
        
        # Roll Button (Bottom Left, Top of Stack)
        self.roll_button = Button(
            text='Roll Dice',
            scale=(0.2, 0.08),
            position=(-0.7, -0.35),
            color=color.azure,
            on_click=self.roll_dice
        )
        
        # End Turn Button (Bottom Right)
        self.end_turn_button = Button(
            text='End Turn',
            scale=(0.2, 0.08),
            position=(0.7, -0.4),
            color=color.red,
            on_click=self.end_turn
        )
        
        self.pattern_buttons = []
        
    def roll_dice(self):
        self.on_roll_callback()
    
    def show_summon_patterns(self, monster=None):
        """Show pattern selection if enough summon crests"""
        self.pending_monster = monster  # Store the monster being summoned
        
        player = self.engine.get_current_player()
        total_summons = player.crests.get('SUMMON', 0)
        
        if total_summons < 2:
            print(f"Not enough SUMMON crests: {total_summons} < 2")
            return
        
        self.show_pattern_selection()

    def update(self):
        # Update logic if needed
        pass

    def end_turn(self):
        self.on_end_turn_callback()

    def end_turn(self):
        self.on_end_turn_callback()

    def show_pattern_selection(self):
        # Clear existing buttons if any
        self.hide_pattern_selection()
        
        y_pos = 0.3
        for name in PATTERNS.keys():
            btn = Button(
                text=name,
                scale=(0.2, 0.05),
                position=(0.7, y_pos),
                color=color.orange,
                parent=camera.ui
            )
            # Use closure to capture loop variable
            btn.on_click = Func(self.select_pattern, name)
            self.pattern_buttons.append(btn)
            y_pos -= 0.06

    def hide_pattern_selection(self):
        for btn in self.pattern_buttons:
            destroy(btn)
        self.pattern_buttons.clear()

    def select_pattern(self, pattern_name):
        print(f"HUD Selected: {pattern_name} for {self.pending_monster.name if self.pending_monster else 'Unknown'}")
        
        # Pass both pattern name and the pending monster
        self.on_pattern_selected_callback(pattern_name, self.pending_monster)
        
        self.hide_pattern_selection()
        self.pending_monster = None # Reset
