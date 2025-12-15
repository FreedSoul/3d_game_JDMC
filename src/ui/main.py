from ursina import *
from src.core.engine import GameEngine
from src.ui.board_view import BoardView
from src.ui.hud import HUD
from src.ui.camera_controls import CameraControls
from src.ui.action_log import ActionLog
from src.ui.crest_counter import CrestCounter
from src.ui.dice_roller import DiceRoller
from src.ui.settings_panel import SettingsPanel
from src.core.dataclasses import DieFace, Pattern
from src.core.patterns_registry import PATTERNS
import random

def main():
    app = Ursina()
    
    # Initialize Core Engine
    engine = GameEngine()
    
    # UI Components
    action_log = ActionLog()
    crest_counter = CrestCounter(engine)
    dice_roller = DiceRoller()
    
    # Settings Panel with Camera Controls
    settings_panel = SettingsPanel()
    cam_controls = CameraControls(parent_entity=settings_panel.content_container)
    settings_panel.add_content(cam_controls, (0.05, 0))
    
    # Initialize Hand View
    from src.ui.hand_view import HandView
    hand_view = HandView()
    
    # Initialize Board View
    board = BoardView(engine, action_log)
    board.crest_counter = crest_counter  # Pass reference for updates
    
    # Define callback for when a pattern is clicked in HUD
    def on_roll():
        results = engine.roll_dice()
        print(f"Rolled: {results}")
        
        # Animate Dice (no pattern selection)
        dice_roller.roll(results, engine=engine)
        
        # Log the roll results
        roll_msg = "Rolled: " + ", ".join([f"{count}x {face.value}" for face, count in results.items()])
        action_log.add_message(roll_msg)
        
        # Update UI Stats with highlighting for new crests
        crest_counter.update_stats(new_crests=results)
    
    def on_pattern_selected(pattern_name):
        if pattern_name in PATTERNS:
            selected_pattern = PATTERNS[pattern_name]
            board.start_placement(selected_pattern)

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
    
    # Connect roll button to settings panel for z-index control
    settings_panel.set_roll_button(hud.roll_button)
    
    # Initial Camera Setup
    update_camera()
    crest_counter.update_stats()
    
    app.run()

if __name__ == "__main__":
    main()
