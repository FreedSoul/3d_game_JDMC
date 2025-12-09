from ursina import *
from src.ui.board_view import BoardView
from src.core.engine import GameEngine
from src.ui.hud import HUD
from src.core.dataclasses import DieFace, Pattern
from src.core.patterns_registry import PATTERNS
import random

def main():
    app = Ursina(title="Dungeon Dice Monsters MVP")
    
    # Initialize Core Engine
    engine = GameEngine()
    
    # Initialize Board View
    board = BoardView(engine)
    
    # Define callback for when a pattern is clicked in HUD
    def on_pattern_selected(pattern_name):
        if pattern_name in PATTERNS:
            selected_pattern = PATTERNS[pattern_name]
            board.start_placement(selected_pattern)
            
    def on_roll():
        results = engine.roll_dice()
        print(f"Rolled: {results}")
        
        # If we get SUMMON crests, show pattern selection UI
        if results.get(DieFace.SUMMON, 0) >= 2:
            print("Summons rolled! Choose a pattern.")
            hud.show_pattern_selection()

    # Initialize HUD with both callbacks
    hud = HUD(engine, on_roll, on_pattern_selected)
    
    # Camera Setup
    camera.position = (6, 15, -15)
    camera.rotation_x = 45
    
    app.run()

if __name__ == "__main__":
    main()
