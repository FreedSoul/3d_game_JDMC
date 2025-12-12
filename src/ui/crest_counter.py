from ursina import *
from src.core.engine import GameEngine
from src.core.dataclasses import DieFace

class CrestCounter(Entity):
    def __init__(self, engine: GameEngine):
        super().__init__(parent=camera.ui)
        self.engine = engine
        
        # Position below Action Log (which is roughly Top Right)
        # ActionLog bg is at (0.6, 0.35) with scale (0.5, 0.3). Bottom edge ~ 0.2
        # So we place this at y=0.0 to -0.1 range.
        
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
        
        # Create Text entities for each Crest Type
        self.stats_text = Text(
            parent=self,
            text="",
            position=(0.38, 0.08),
            scale=0.8,
            color=color.white,
            origin=(-0.5, 0.5),
            z=-1
        )
        
        self.update_stats()

    def update_stats(self):
        player = self.engine.get_current_player()
        
        # Build string
        # Maybe 2 columns?
        # SUMMON: X  MOVEMENT: Y
        # ATTACK: Z  DEFENSE: W
        # MAGIC:  A  TRAP:    B
        
        crests = player.crests
        
        txt = f"Player {player.player_id}\n"
        txt += f"SUMMON: {crests.get(DieFace.SUMMON, 0)}   MOVEMENT: {crests.get(DieFace.MOVEMENT, 0)}\n"
        txt += f"ATTACK: {crests.get(DieFace.ATTACK, 0)}   DEFENSE: {crests.get(DieFace.DEFENSE, 0)}\n"
        txt += f"MAGIC:  {crests.get(DieFace.MAGIC, 0)}   TRAP:    {crests.get(DieFace.TRAP, 0)}\n"
        
        self.stats_text.text = txt
