from ursina import *
from src.core.engine import GameEngine
from src.ui.board_view import BoardView
from src.ui.hud import HUD
from src.ui.camera_controls import CameraControls
from src.ui.action_log import ActionLog
from src.ui.crest_counter import CrestCounter
from src.ui.dice_roller import DiceRoller
from src.core.dataclasses import DieFace, Pattern
from src.core.patterns_registry import PATTERNS
import random

def main():
    app = Ursina(title="Dungeon Dice Monsters MVP")
    
    # Initialize Core Engine
    engine = GameEngine()
    
    # UI Components
    action_log = ActionLog()
    crest_counter = CrestCounter(engine)
    dice_roller = DiceRoller()
    
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
        
        # Animate Dice
        dice_roller.roll(results)
        
        # Update UI Stats
        crest_counter.update_stats()
        
        # If we get SUMMON crests, show pattern selection UI
        # Check against result dict (Since engine populates it with counts)
        # We need to verify which crest type to check.
        # Since logic is random now, we should only open menu if Summon >= 2.
        # But wait, logic says "Summon Level 1 monster requires 2 invocations".
        
        if results.get(DieFace.SUMMON, 0) >= 2:
            print("Summons rolled! Choose a pattern.")
            hud.show_pattern_selection()

    def update_camera():
        # Board Center is roughly (6, 0, 9)
        # We want to center the view on the board.
        
        if engine.current_player_id == 1:
            # Player 1 View
            # Positioned back and up, looking at center
            camera.position = (6, 38, -24)
            camera.rotation = (52, 0, 0)
        else:
            # Player 2 View (Opposite)
            # Mirrored across Z=9
            # Z = 9 + (9 - (-24)) = 9 + 33 = 42
            camera.position = (6, 38, 42)
            camera.rotation = (52, 180, 0)

    def on_end_turn():
        engine.next_turn()
        update_camera()
        crest_counter.update_stats()
        print(f"Turn Ended. Now Player {engine.current_player_id}")

    # Initialize HUD with all callbacks
    hud = HUD(engine, on_roll, on_pattern_selected, on_end_turn)
    
    # Initialize Camera Controls
    cam_controls = CameraControls()
    
    # Initial Camera Setup
    update_camera()
    crest_counter.update_stats()
    
    app.run()

if __name__ == "__main__":
    main()
