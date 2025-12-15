from ursina import *
from src.core.dataclasses import Monster
from src.core.effects import get_effect
import textwrap

class CardDetailModal(Entity):
    def __init__(self, monster: Monster):
        super().__init__(parent=camera.ui, z=-100)
        self.monster = monster
        
        # 1. Dark Overlay (Click to close)
        self.bg = Button(
            parent=self,
            model='quad',
            scale=(2, 2),
            color=color.rgba(0, 0, 0, 0.85),
            highlight_color=color.rgba(0, 0, 0, 0.85),
            on_click=self.close
        )
        
        # 2. Main Container
        self.container = Entity(parent=self, scale=1)
        
        # --- LEFT SIDE: IMAGE ---
        # Card Aspect Ratio ~ 0.64 (e.g. 64x100)
        self.card_visual = Entity(
            parent=self.container,
            model='quad',
            texture=monster.texture_path if monster.texture_path else 'white_cube',
            scale=(0.35, 0.55),
            position=(-0.3, 0),
            color=color.white if monster.texture_path else color.gray
        )
        
        # --- RIGHT SIDE: DETAILS ---
        text_x = 0.05
        
        # Title
        Text(parent=self.container, text=monster.name, x=text_x, y=0.25, scale=2, color=color.gold)
        
        # Type & Level
        Text(parent=self.container, text=f"{monster.type} | Level {monster.level}", x=text_x, y=0.18, scale=1.2, color=color.light_gray)
        
        # Stats
        stats_str = f"HP: {monster.hp}   ATK: {monster.atk}   DEF: {monster.defense}"
        Text(parent=self.container, text=stats_str, x=text_x, y=0.10, scale=1.5, color=color.white)
        
        # Description
        # Combine description + effect
        full_text = monster.description
        if monster.effects:
            effect = get_effect(monster.effects[0])
            if effect:
                full_text += f"\n\n[Effect: {effect.description}]"

        # Safe Word Wrap
        wrapped_text = textwrap.fill(full_text, width=35)
        
        Text(parent=self.container, text=wrapped_text, x=text_x, y=0.0, scale=1.1, color=color.white)
        
        # Close Hint
        Text(parent=self.container, text="(Click anywhere to close)", y=-0.4, scale=1, color=color.gray, origin=(0, 0))

    def input(self, key):
        if key == 'escape':
            self.close()

    def close(self):
        destroy(self)
