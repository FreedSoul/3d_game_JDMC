from ursina import *
from src.core.engine import GameEngine
from src.core.patterns_registry import PATTERNS
from src.core.constants import Phase

class HUD(Entity):
    def __init__(self, engine: GameEngine, on_roll_callback, on_pattern_selected_callback, on_end_turn_callback, on_next_phase_callback):
        super().__init__(parent=camera.ui)
        self.engine = engine
        self.on_roll_callback = on_roll_callback
        self.on_pattern_selected_callback = on_pattern_selected_callback
        self.on_end_turn_callback = on_end_turn_callback
        self.on_next_phase_callback = on_next_phase_callback
        
        # Roll Button (Bottom Left)
        self.roll_button = Button(
            text='Roll',
            icon='../assets/hud/diceroll.png',
            scale=(0.2, 0.08),
            position=(-0.7, -0.4), # Align with End Turn Y-level
            color=color.azure,
            on_click=self.roll_dice
        )
        if self.roll_button.icon:
             # Button is (0.2, 0.08). Aspect ratio 2.5:1
             # We want icon square-ish on the left.
             # Relative to height (0.08), width is 2.5x
             
             # Make icon smaller relative to button
             self.roll_button.icon.scale = (0.25, 0.7) 
             self.roll_button.icon.x = -0.3
             
             # Text adjustments
             self.roll_button.text_origin = (0, 0)
             self.roll_button.text_entity.x = 0.01
             self.roll_button.text_entity.scale = 8.0
        
        # Next Phase Button (Bottom Right - Inner)
        self.next_phase_button = Button(
            text='Next Phase',
            scale=(0.2, 0.08),
            position=(0.7, -0.3), # Stacked above End Turn
            color=color.orange,
            on_click=self.next_phase
        )

        # End Turn Button (Bottom Right - Outer)
        self.end_turn_button = Button(
            text='End Turn',
            scale=(0.2, 0.08),
            position=(0.7, -0.4),
            color=color.gray, # Start gray
            on_click=self.end_turn,
            disabled=True
        )
        
        # Phase Text Display
        self.phase_text = Text(
            text=self.engine.current_phase.value,
            scale=2,
            origin=(0, 0),
            position=(0, 0.45),
            color=color.white
        )
        
        # Turn Notification Text (Big Overlay)
        self.turn_notification_text = Text(
            text='',
            scale=5,
            origin=(0, 0),
            position=(0, 0),
            color=color.gold,
            enabled=False
        )

        self.pattern_buttons = []
        
    def roll_dice(self):
        self.on_roll_callback()
    
    def show_summon_patterns(self, monster=None, card_position=None):
        """Show pattern selection if enough summon crests"""
        self.pending_monster = monster  # Store the monster being summoned
        
        player = self.engine.get_current_player()
        total_summons = player.crests.get('SUMMON', 0)
        
        if total_summons < 2:
            print(f"Not enough SUMMON crests: {total_summons} < 2")
            return
        
        self.show_pattern_selection(card_position)

    def next_phase(self):
        self.on_next_phase_callback()

    def update_phase_state(self, phase):
        self.phase_text.text = phase.value
        
        if phase == Phase.END:
            self.end_turn_button.disabled = False
            self.end_turn_button.color = color.red
            self.next_phase_button.disabled = True
            self.next_phase_button.color = color.gray
        else:
            self.end_turn_button.disabled = True
            self.end_turn_button.color = color.gray
            self.next_phase_button.disabled = False
            self.next_phase_button.color = color.orange

    def end_turn(self):
        self.on_end_turn_callback()

    def end_turn(self):
        self.on_end_turn_callback()

    def show_pattern_selection(self, origin_pos=None):
        # Clear existing buttons if any
        self.hide_pattern_selection()
        
        # Default to right side if no position provided (fallback)
        base_x = 0.7
        base_y = 0.3
        
        if origin_pos:
            # Position above the card
            # Card is roughly (-0.5 to 0.5) X
            # Card Y is -0.38
            # We want buttons above it.
            base_x = origin_pos.x
            base_y = origin_pos.y + 0.2 # Start 0.3 units above the card center
            
        y_pos = base_y
        for name in PATTERNS.keys():
            btn = Button(
                text=name,
                scale=(0.2, 0.05),
                position=(base_x, y_pos),
                color=color.orange,
                parent=camera.ui
            )
            # Use closure to capture loop variable
            btn.on_click = Func(self.select_pattern, name)
            self.pattern_buttons.append(btn)
            y_pos += 0.06 # Stack upwards away from card if using card pos? 
            # Or stack downwards? 
            # If we start above, maybe stack up? Or stack down but ensure we don't cover card.
            # Let's stack UPWARDS from the base_y.
            
        # If we were using default right side, we usually stack down.
        # Let's check logic:
        # Original: y_pos = 0.3, y_pos -= 0.06 (Stacked Down)
        # New Dynamic: Let's Stack UP.
    def show_turn_notification(self, player_id):
        self.turn_notification_text.text = f"PLAYER {player_id} TURN"
        self.turn_notification_text.enabled = True
        self.turn_notification_text.scale = 0.5 # Start small
        self.turn_notification_text.animate_scale(5, duration=0.5, curve=curve.out_bounce)
        
        # Hide after 2 seconds
        invoke(self.hide_turn_notification, delay=2)
        
    def hide_turn_notification(self):
        self.turn_notification_text.enabled = False

    def hide_pattern_selection(self):
        for btn in self.pattern_buttons:
            destroy(btn)
        self.pattern_buttons.clear()

    def select_pattern(self, pattern_name):
        print(f"HUD Selected: {pattern_name} for {self.pending_monster.name if self.pending_monster else 'Unknown'}")
        
        # Pass both pattern name and the pending monster
        self.on_pattern_selected_callback(pattern_name, self.pending_monster)
        
        self.hide_pattern_selection()
        self.pending_monster = None # Reset
