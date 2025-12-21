from ursina import *

class MonsterContextMenu(Entity):
    def __init__(self, monster, position, on_move_click, on_stats_click, on_cancel_click):
        # Ensure Z is -2 to appear above everything else
        pos_vec = Vec3(position[0], position[1], -2)
        
        super().__init__(
            parent=camera.ui,
            position=pos_vec,
            scale=(0.15, 0.2), # Width, Height
            model='quad',
            color=color.rgba(0, 0, 0, 0.8), # Semi-transparent black background
        )
        self.monster = monster
        
        # Title (Monster Name)
        self.title_text = Text(
            text=monster.name,
            parent=self,
            scale=5,
            origin=(0, 0),
            y=0.4,
            color=color.gold
        )
        
        # Button: Move
        self.move_btn = Button(
            parent=self,
            text='Move',
            scale=(0.9, 0.25),
            y=0.15,
            color=color.azure,
            on_click=on_move_click
        )
        
        # Button: Stats
        self.stats_btn = Button(
            parent=self,
            text='Stats',
            scale=(0.9, 0.25),
            y=-0.15,
            color=color.orange,
            on_click=on_stats_click
        )
        
        # Button: Cancel
        self.cancel_btn = Button(
            parent=self,
            text='Cancel',
            scale=(0.9, 0.25),
            y=-0.45,
            color=color.gray,
            on_click=on_cancel_click
        )
        
    def close(self):
        destroy(self)
