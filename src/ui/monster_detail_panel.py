from ursina import *

class MonsterDetailPanel(Entity):
    def __init__(self, monster, on_close_click):
        super().__init__(
            parent=camera.ui,
            scale=(0.6, 0.7), # Large centered panel
            model='quad',
            color=color.black90, # Dark background
            position=(0, 0, -3) # On top of everything (Menu is -2)
        )
        self.monster = monster
        
        # --- Header ---
        self.name_text = Text(
            parent=self,
            text=f"{monster.name} (Lvl {monster.level})",
            origin=(0, 0),
            y=0.4,
            scale=2.5,
            color=color.gold
        )
        self.type_text = Text(
            parent=self,
            text=f"Type: {monster.type}",
            origin=(0, 0),
            y=0.33,
            scale=1.5,
            color=color.light_gray
        )
        
        # --- Stats Row ---
        # HP
        self.hp_label = Text(parent=self, text="HP", position=(-0.3, 0.2), scale=2, color=color.azure)
        self.hp_val = Text(parent=self, text=f"{monster.hp}/{monster.hp}", position=(-0.3, 0.15), scale=3, color=color.white)
        
        # ATK
        self.atk_label = Text(parent=self, text="ATK", position=(0, 0.2), scale=2, color=color.red)
        self.atk_val = Text(parent=self, text=str(monster.atk), position=(0, 0.15), scale=3, color=color.white)
        
        # DEF
        self.def_label = Text(parent=self, text="DEF", position=(0.3, 0.2), scale=2, color=color.green)
        self.def_val = Text(parent=self, text=str(monster.defense), position=(0.3, 0.15), scale=3, color=color.white)
        
        # Horizontal Line
        self.line = Entity(parent=self, model='quad', scale=(0.9, 0.005), color=color.gray, y=0.05)
        
        # --- Effects & Abilities ---
        self.effects_label = Text(parent=self, text="Active Effects:", position=(-0.4, -0.05), scale=1.5, color=color.yellow)
        effects_str = "\n".join(monster.effects.keys()) if hasattr(monster, 'effects') and isinstance(monster.effects, dict) else "None"
        if isinstance(monster.effects, list):
             effects_str = ", ".join(monster.effects) if monster.effects else "None"
             
        self.effects_text = Text(
            parent=self, 
            text=effects_str, 
            position=(-0.4, -0.12), 
            scale=1.2, 
            color=color.white,
            wordwrap=30
        )
        
        self.desc_label = Text(parent=self, text="Description:", position=(-0.4, -0.25), scale=1.5, color=color.cyan)
        self.desc_text = Text(
            parent=self, 
            text=monster.description, 
            position=(-0.4, -0.32), 
            scale=1.0, 
            color=color.white,
            wordwrap=40
        )

        
        # Close Button
        self.close_btn = Button(
            parent=self,
            text='Close',
            scale=(0.2, 0.1),
            y=-0.42,
            color=color.red,
            on_click=on_close_click
        )

    def close(self):
        destroy(self)
