from ursina import *
from src.core.engine import GameEngine

from src.core.patterns_registry import PATTERNS

class HUD(Entity):
    def __init__(self, engine: GameEngine, on_roll_callback, on_pattern_selected_callback):
        super().__init__(parent=camera.ui)
        self.engine = engine
        self.on_roll_callback = on_roll_callback # Called when dice are rolled
        self.on_pattern_selected_callback = on_pattern_selected_callback # Called when pattern is chosen
        
        self.roll_button = Button(
            text='Roll Dice',
            scale=(0.2, 0.1),
            position=(-0.7, 0.4),
            color=color.azure,
            on_click=self.roll_dice
        )
        
        self.info_text = Text(
            text="Welcome to DDM MVP",
            position=(-0.8, -0.4),
            scale=1.5,
            origin=(0, 0)
        )
        
        self.pattern_buttons = []
        
    def roll_dice(self):
        self.on_roll_callback()
        self.update_stats()

    def update_stats(self):
        player = self.engine.get_current_player()
        stats = f"P{player.player_id} | Turn: {self.engine.turn_count}\n"
        for face, amount in player.crests.items():
            if amount > 0:
                stats += f"{face.value}: {amount}  "
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
