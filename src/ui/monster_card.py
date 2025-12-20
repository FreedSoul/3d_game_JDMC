from ursina import *
from src.core.dataclasses import Monster
from src.core.effects import get_effect

class MonsterCard(Entity):
    def __init__(self, monster: Monster, position=(0,0), on_click=None, on_summon_request=None, **kwargs):
        # Determine texture
        card_texture = 'white_cube'
        if monster.texture_path:
            card_texture = monster.texture_path

        super().__init__(
            parent=camera.ui,
            model='quad',
            texture=card_texture, 
            scale=(0.18, 0.28), # Aspect ratio ~ card
            position=position,
            color=color.dark_gray if not monster.texture_path else color.white, # Tint if no texture
            collider='box'
        )
        self.monster = monster
        self.on_click_callback = on_click
        self.on_summon_request = on_summon_request
        
        # --- Options Overlay ---
        self.options_menu = Entity(parent=self, scale=1, enabled=False, z=-1)
        self.summon_btn = Button(
            parent=self.options_menu,
            text="SUMMON",
            scale=(0.8, 0.2),
            y=0.3,
            color=color.green,
            on_click=self.request_summon
        )
        
        # --- Visuals ---
        
        # If we have a texture, we might want to hide the text or overlay it nicely.
        # For MVP, let's keep text visible but maybe smaller or positioned better if texture is used.
        # But user asked to use the card image, which likely already has art.
        # However, for stats, we still need to render them if the card image is just art and not the full pre-baked card.
        # Assuming the PNG is just the art/full card. If it's the full card, we might not need text overlaid.
        # But the user said "extract stats... use it on the hand", implying the image IS the card visual.
        # If the image is the *full card*, we shouldn't overlay text.
        # If the image is just the *art*, we need the frame.
        # User said "assets/cards/crystal_golem_1.png". Let's assume it replaces the background.
        
        # Helper to check if we should show debug text
        # User requested to hide text overlap if texture is present
        show_debug_text = False
        if not monster.texture_path or "white_cube" in monster.texture_path:
            show_debug_text = True
            
        if show_debug_text:
            # Name
            Text(parent=self, text=monster.name, position=(0, 0.45), origin=(0, 0), scale=4, color=color.gold)
            
            # Stats Block
            stats_text = f"LVL: {monster.level}\nHP: {monster.hp}\nATK: {monster.atk}\nDEF: {monster.defense}\nTYPE: {monster.type}"
            Text(parent=self, text=stats_text, position=(-0.45, 0.2), origin=(-0.5, 0.5), scale=3)
            
            # Description (Combine flavor text + Effects)
            full_desc = monster.description
            if monster.effects:
                effect_obj = get_effect(monster.effects[0])
                if effect_obj:
                    full_desc += f"\n[{effect_obj.description}]"
            
            # Note: Removing wordwrap to avoid Ursina Text error for now. 
            # Manually breaking lines or relying on simple display.
            Text(parent=self, text=full_desc, position=(0, -0.3), origin=(0, 0), scale=0.8, color=color.light_gray)

    def request_summon(self):
        print(f"Summon Requested for {self.monster.name} at {self.position}")
        if self.on_summon_request:
            # Pass monster AND card position (Vec3, but for UI we mostly care about x, y)
            self.on_summon_request(self.monster, self.position)

    def update(self):
        # Hover Logic for Options
        if self.hovered:
            self.options_menu.enabled = True
        else:
            # Only disable if mouse is NOT over the options menu buttons
            # But the buttons are children of self, so hovering them might count as hovering self?
            # In Ursina, if you hover a child, you don't necessarily hover the parent collider unless it's set up that way.
            # But wait, button has its own collider.
            # Let's keep it simple: if mouse.hovered_entity is self or one of options.
            if mouse.hovered_entity == self or mouse.hovered_entity in self.options_menu.children:
                self.options_menu.enabled = True
            else:
                self.options_menu.enabled = False

    def input(self, key):
        if self.hovered and key == 'left mouse down':
            # Check if we clicked the summon button?
            # The button's on_click handles itself.
            # But if we click the card background, we want details.
            # If mouse is hovering the button, button gets click.
            # If mouse is hovering the card but NOT the button, card gets click.
            # Ursina input propogation... if button handles it, great.
            if mouse.hovered_entity == self:
                if self.on_click_callback:
                    self.on_click_callback(self.monster)
                
                # Simple click visual feedback
                self.animate_scale(self.scale * 1.1, duration=0.1)
                invoke(self.animate_scale, self.scale, duration=0.1, delay=0.1)

    def set_summonable(self, can_summon: bool):
        if can_summon:
            self.summon_btn.color = color.green
            self.summon_btn.text_color = color.white
        else:
            self.summon_btn.color = color.gray
            self.summon_btn.text_color = color.light_gray
