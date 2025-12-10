from ursina import *
from src.core.engine import GameEngine
from src.ui.board_view import BoardView
from src.ui.hud import HUD
from src.ui.camera_controls import CameraControls
from src.ui.action_log import ActionLog
from src.core.dataclasses import DieFace, Pattern
from src.core.patterns_registry import PATTERNS
import random

def main():
    app = Ursina(title="Dungeon Dice Monsters MVP")
    
    # Initialize Core Engine
    engine = GameEngine()
    
    # UI Components
    action_log = ActionLog()
    
    # Initialize Board View
    board = BoardView(engine, action_log)
    
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

    def update_camera():
        # Board Center is roughly (6, 0, 9)
        # We want a high angle to see everything.
        
        if engine.current_player_id == 1:
            # Player 1 View
            camera.position = (6, 28, -22)
            camera.rotation = (55, 0, 0)
        else:
            # Player 2 View (Opposite)
            # Mirror across Z=9
            camera.position = (6, 28, 40)
            camera.rotation = (55, 180, 0)

    def on_end_turn():
        engine.next_turn()
        update_camera()
        print(f"Turn Ended. Now Player {engine.current_player_id}")

    # Initialize HUD with all callbacks
    hud = HUD(engine, on_roll, on_pattern_selected, on_end_turn)
    
    # Initialize Camera Controls
    cam_controls = CameraControls()
    
    # Initial Camera Setup
    update_camera()
    
    app.run()

if __name__ == "__main__":
    main()
