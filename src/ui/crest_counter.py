from ursina import *
from src.core.engine import GameEngine
from src.core.dataclasses import DieFace

class CrestCounter(Entity):
    def __init__(self, engine: GameEngine):
        super().__init__(parent=camera.ui)
        self.engine = engine
        
        # Track previous crest values to detect changes
        self.previous_crests = {}
        
        # Position below Action Log
        self.bg = Entity(
            parent=self,
            model='quad',
            color=color.black66,
            scale=(0.5, 0.2),
            position=(0.6, 0.05),
            z=1
        )
        
        self.title = Text(
            parent=self,
            text="Crest Bank",
            position=(0.38, 0.12),
            scale=1.0,
            color=color.gold,
            z=-1
        )
        
        # Create individual Text/Button entities for each crest line
        self.crest_texts = {}
        y_offset = 0.08
        line_height = 0.02
        
        # Player ID line
        self.player_text = Text(
            parent=self,
            text="",
            position=(0.38, y_offset),
            scale=0.8,
            color=color.white,
            origin=(-0.5, 0.5),
            z=-1
        )
        
        # Crest lines
        crest_pairs = [
            (DieFace.SUMMON, DieFace.MOVEMENT),
            (DieFace.ATTACK, DieFace.DEFENSE),
            (DieFace.MAGIC, DieFace.TRAP)
        ]
        
        for i, (left_crest, right_crest) in enumerate(crest_pairs):
            y_pos = y_offset - (i + 1) * line_height
            
            # All crests as simple text
            self.crest_texts[left_crest] = Text(
                parent=self,
                text="",
                position=(0.38, y_pos),
                scale=0.8,
                color=color.white,
                origin=(-0.5, 0.5),
                z=-1
            )
            
            self.crest_texts[right_crest] = Text(
                parent=self,
                text="",
                position=(0.56, y_pos),
                scale=0.8,
                color=color.white,
                origin=(-0.5, 0.5),
                z=-1
            )
        
        self.update_stats()

    def update_stats(self, new_crests=None):
        player = self.engine.get_current_player()
        crests = player.crests
        
        # Update player text
        self.player_text.text = f"Player {player.player_id}"
        
        # Update each crest text with highlighting
        for face in DieFace:
            count = crests.get(face, 0)
            is_new = new_crests and face in new_crests and new_crests[face] > 0
            
            if face in self.crest_texts:
                self.crest_texts[face].text = f"{face.value}: {count}"
                # Highlight if newly added
                self.crest_texts[face].color = color.gold if is_new else color.white
        
        # Reset highlighting after 2 seconds
        if new_crests:
            invoke(self.reset_colors, delay=2.0)
    
    def reset_colors(self):
        for text in self.crest_texts.values():
            text.color = color.white
