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
        
        # Text Info (Top Left)
        self.info_text = Text(
            text="Welcome to DDM MVP",
            position=(-0.85, 0.45),
            scale=1.2,
            origin=(-0.5, 0.5), # Anchor Top-Left
            color=color.black
        )
        
        # Roll Button (Bottom Left)
        self.roll_button = Button(
            text='Roll Dice',
            scale=(0.2, 0.08),
            position=(-0.7, -0.4),
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
        self.update_stats()

    def end_turn(self):
        self.on_end_turn_callback()
        self.update_stats()

    def update_stats(self):
        player = self.engine.get_current_player()
        stats = f"PLAYER {player.player_id} | Turn: {self.engine.turn_count}\n"
        stats += "-" * 20 + "\n"
        for face, amount in player.crests.items():
            if amount > 0:
                stats += f"{face.value}: {amount}\n"
        self.info_text.text = stats

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
        print(f"HUD Selected: {pattern_name}")
        self.on_pattern_selected_callback(pattern_name)
        self.hide_pattern_selection()
