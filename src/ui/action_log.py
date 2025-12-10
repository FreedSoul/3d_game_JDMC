from ursina import *

class ActionLog(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        
        # Background Panel (Top Right)
        self.bg = Entity(
            parent=self,
            model='quad',
            color=color.black66,
            scale=(0.5, 0.3),
            position=(0.6, 0.35),
            z=1  # Push to back
        )
        
        # Title
        self.title = Text(
            parent=self,
            text="Combat Log",
            position=(0.38, 0.48),
            scale=1.0,
            color=color.orange,
            z=-1 # Pull to front
        )
        
        # Log Text Content
        self.log_text = Text(
            parent=self,
            text="",
            position=(0.36, 0.45), # Start below title
            scale=0.8,
            color=color.white,
            origin=(-0.5, 0.5), # Top-Left anchor
            z=-1 # Pull to front
        )
        
        self.messages = []
        self.max_messages = 6
        
        self.log("Action Log Ready")
        
    def log(self, message: str):
        print(f"DEBUG UI LOG: {message}")
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0) # Remove oldest
            
        # Rebuild text
        full_text = "\n".join(self.messages)
        self.log_text.text = full_text
