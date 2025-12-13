from ursina import *
from src.core.dataclasses import DieFace
import random

class Die(Entity):
    def __init__(self, position, scale=1.0):
        super().__init__(position=position, scale=scale)
        
        # We construct a cube from 6 quads
        
        self.faces = {}
        
        # 1. Front (SUMMON)
        self.faces[DieFace.SUMMON] = Entity(parent=self, model='quad', texture='../../assets/crests/SUMMON.png', z=-0.5, color=color.white, double_sided=True, unlit=True)
        
        # 2. Back (TRAP) - Rotated 180 Y
        self.faces[DieFace.TRAP] = Entity(parent=self, model='quad', texture='../../assets/crests/TRAP.png', z=0.5, rotation_y=180, color=color.white, double_sided=True, unlit=True)
        
        # 3. Right (MOVEMENT) - Rotated 90 Y
        self.faces[DieFace.MOVEMENT] = Entity(parent=self, model='quad', texture='../../assets/crests/MOVEMENT.png', x=0.5, rotation_y=90, color=color.white, double_sided=True, unlit=True)
        
        # 4. Left (DEFENSE) - Rotated -90 Y
        self.faces[DieFace.DEFENSE] = Entity(parent=self, model='quad', texture='../../assets/crests/DEFENSE.png', x=-0.5, rotation_y=-90, color=color.white, double_sided=True, unlit=True)
        
        # 5. Top (ATTACK) - Rotated 90 X
        self.faces[DieFace.ATTACK] = Entity(parent=self, model='quad', texture='../../assets/crests/ATTACK.png', y=0.5, rotation_x=90, color=color.white, double_sided=True, unlit=True)
        
        # 6. Bottom (MAGIC) - Rotated -90 X
        self.faces[DieFace.MAGIC] = Entity(parent=self, model='quad', texture='../../assets/crests/MAGIC.png', y=-0.5, rotation_x=-90, color=color.white, double_sided=True, unlit=True)

        # Target rotations to show each face (Same as before)
        self.target_rotations = {
            DieFace.SUMMON: Vec3(0, 0, 0),
            DieFace.TRAP: Vec3(0, 180, 0),
            DieFace.MOVEMENT: Vec3(0, -90, 0), 
            DieFace.DEFENSE: Vec3(0, 90, 0),
            DieFace.ATTACK: Vec3(90, 0, 0),
            DieFace.MAGIC: Vec3(-90, 0, 0)
        }

    def roll(self, result_face: DieFace, duration=1.0):
        # Random spin
        self.animate('rotation', self.rotation + Vec3(360, 360, 360), duration=duration/2, curve=curve.linear)
        
        # Final snap
        target = self.target_rotations.get(result_face, Vec3(0,0,0))
        # Add a full rotation to make it look intentional
        final_rot = target + Vec3(360, 360, 0) 
        
        invoke(self.animate, 'rotation', final_rot, duration=duration/2, curve=curve.out_cubic, delay=duration/2)

class DiceRoller(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        
        # Create background panel/window
        self.panel = Entity(
            parent=self,
            model='quad',
            scale=(1.0, 0.6),
            color=color.rgba(0, 0, 0, 200),  # Semi-transparent black
            z=1
        )
        
        # Position dice in center of panel
        self.dice = []
        for i in range(3):
            # Spread X: -0.25, 0, 0.25
            d = Die(position=((i-1)*0.25, 0, 0), scale=0.15) 
            d.parent = self
            d.z = 0  # In front of panel
            self.dice.append(d)
        
        # Add close button in top-right of panel
        self.close_button = Button(
            text='✕',
            parent=self,
            position=(0.45, 0.25),
            scale=(0.06, 0.06),
            color=color.red,
            text_color=color.white,
            on_click=self.hide_animation,
            z=0
        )
        
        # Pattern selection buttons (hidden initially)
        self.pattern_buttons = []
        self.on_pattern_callback = None
        
        # Start hidden
        self.visible = False
            
    def hide_animation(self):
        self.visible = False
        self.hide_patterns()
        
    def roll(self, results: dict, engine=None, on_pattern_selected=None):
        # Show the dice animation
        self.visible = True
        self.on_pattern_callback = on_pattern_selected
        
        # Hide any existing pattern buttons
        self.hide_patterns()
        
        # Results is a Dict[DieFace, int] (Counts)
        # We need to flatten it to list of 3 faces
        faces = []
        for face, count in results.items():
            faces.extend([face] * count)
        
        # Don't shuffle - show actual results in order
        print(f"Animating Roll: {faces}")
        
        for i, die in enumerate(self.dice):
            if i < len(faces):
                die.roll(faces[i])
        
        # Show pattern selection if TOTAL summon crests in bank >= 2
        from src.core.dataclasses import DieFace
        if engine:
            player = engine.get_current_player()
            total_summons = player.crests.get(DieFace.SUMMON, 0)
            print(f"DEBUG: Total SUMMON in bank = {total_summons}, threshold = 2")
            if total_summons >= 2:
                print("DEBUG: Showing pattern selection in 1.5s")
                invoke(self.show_patterns, delay=1.5)  # Show after dice settle
            else:
                print(f"DEBUG: Not enough summons in bank ({total_summons} < 2)")
        else:
            # Fallback to old behavior if no engine passed
            summon_count = results.get(DieFace.SUMMON, 0)
            print(f"DEBUG: SUMMON count = {summon_count}, threshold = 2")
            if summon_count >= 2:
                print("DEBUG: Showing pattern selection in 1.5s")
                invoke(self.show_patterns, delay=1.5)
            else:
                print(f"DEBUG: Not enough summons ({summon_count} < 2)")
    
    def show_patterns(self):
        from src.core.patterns_registry import PATTERNS
        
        # Clear existing
        self.hide_patterns()
        
        # Adjust dice position up to make room for patterns
        for die in self.dice:
            die.y = 0.2
        
        # Create pattern selection buttons below dice
        # Adjusted for better visibility
        y_start = -0.1
        x_start = -0.4
        button_width = 0.18
        button_spacing = 0.2
        
        pattern_names = list(PATTERNS.keys())
        
        for i, name in enumerate(pattern_names):
            x_pos = x_start + (i % 4) * button_spacing
            y_pos = y_start - (i // 4) * 0.1
            
            btn = Button(
                text=name,
                parent=self,
                position=(x_pos, y_pos),
                scale=(button_width, 0.08),
                color=color.orange,
                text_color=color.white,
                z=-2,  # In front of everything
                enabled=True,
                visible=True
            )
            btn.on_click = Func(self.select_pattern, name)
            self.pattern_buttons.append(btn)
    
    def select_pattern(self, pattern_name):
        print(f"Selected pattern: {pattern_name}")
        if self.on_pattern_callback:
            self.on_pattern_callback(pattern_name)
        self.hide_animation()  # Close the panel
    
    def hide_patterns(self):
        # Reset dice position
        for die in self.dice:
            die.y = 0
        
        for btn in self.pattern_buttons:
            destroy(btn)
        self.pattern_buttons = []
