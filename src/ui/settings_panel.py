from ursina import *

class SettingsPanel(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        
        # Panel dimensions
        self.panel_width = 0.4
        self.hidden_x = -1.0  # Off-screen left
        self.visible_x = -0.7  # Visible from left
        
        # Background panel
        self.panel = Entity(
            parent=self,
            model='quad',
            color=color.rgba(30, 30, 30, 230),
            scale=(self.panel_width, 1.8),
            position=(self.hidden_x, 0),
            z=1
        )
        
        # Title
        self.title = Text(
            parent=self,
            text="Settings",
            position=(self.hidden_x + self.panel_width/2 - 0.05, 0.8),
            scale=1.2,
            color=color.orange,
            z=0
        )
        
        # Toggle button (always visible on LEFT edge)
        self.toggle_button = Button(
            text='MENU',
            parent=camera.ui,
            position=(-0.85, 0.4),
            scale=(0.12, 0.08),
            color=color.orange,
            text_color=color.white,
            on_click=self.toggle
        )
        
        # Container for settings content
        self.content_container = Entity(parent=self)
        
        # State
        self.is_visible = False
        
    def toggle(self):
        """Toggle panel visibility with slide animation"""
        if self.is_visible:
            self.hide()
        else:
            self.show()
    
    def show(self):
        """Slide panel in from left"""
        self.is_visible = True
        self.panel.animate_x(self.visible_x, duration=0.3, curve=curve.out_expo)
        self.title.animate_x(self.visible_x + self.panel_width/2 - 0.05, duration=0.3, curve=curve.out_expo)
        
        # Animate content
        for child in self.content_container.children:
            if hasattr(child, 'x'):
                target_x = child.original_x if hasattr(child, 'original_x') else child.x
                child.animate_x(target_x + (self.visible_x - self.hidden_x), duration=0.3, curve=curve.out_expo)
    
    def hide(self):
        """Slide panel out to left"""
        self.is_visible = False
        self.panel.animate_x(self.hidden_x, duration=0.3, curve=curve.out_expo)
        self.title.animate_x(self.hidden_x + self.panel_width/2 - 0.05, duration=0.3, curve=curve.out_expo)
        
        # Animate content
        for child in self.content_container.children:
            if hasattr(child, 'x'):
                child.animate_x(self.hidden_x + (child.x - self.visible_x), duration=0.3, curve=curve.out_expo)
    
    def add_content(self, entity, relative_pos):
        """Add content to the panel with relative positioning"""
        entity.parent = self.content_container
        entity.original_x = self.hidden_x + relative_pos[0]
        entity.x = entity.original_x
        entity.y = relative_pos[1]
        entity.z = 0
        return entity
