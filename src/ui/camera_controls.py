from ursina import *

class CameraControls(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        
        # Position Controls (Bottom Left, above Stats)
        self.bg = Entity(
            parent=self,
            model='quad',
            color=color.black66,
            scale=(0.15, 0.15),
            position=(-0.7, -0.2)
        )
        
        self.btn_up = Button(
            parent=self,
            text='U',
            scale=(0.06, 0.06),
            position=(-0.7, -0.15),
            on_click=Func(self.move_camera, 0, 0, 1)
        )
        self.btn_down = Button(
            parent=self,
            text='D',
            scale=(0.06, 0.06),
            position=(-0.7, -0.25),
            on_click=Func(self.move_camera, 0, 0, -1)
        )
        self.btn_left = Button(
            parent=self,
            text='L',
            scale=(0.06, 0.06),
            position=(-0.78, -0.2),
            on_click=Func(self.move_camera, -1, 0, 0)
        )
        self.btn_right = Button(
            parent=self,
            text='R',
            scale=(0.06, 0.06),
            position=(-0.62, -0.2),
            on_click=Func(self.move_camera, 1, 0, 0)
        )
        
        # Zoom Controls
        self.btn_zoom_in = Button(
            parent=self,
            text='+',
            scale=(0.05, 0.05),
            position=(-0.55, -0.15),
            on_click=Func(self.zoom_camera, -1)
        )
        self.btn_zoom_out = Button(
            parent=self,
            text='-',
            scale=(0.05, 0.05),
            position=(-0.55, -0.25),
            on_click=Func(self.zoom_camera, 1)
        )
        
        self.zoom_step = 2
        self.move_step = 2

    def move_camera(self, dx, dy, dz):
        # Move relative to camera rotation would be nicer, but world axis is safer for constraints
        # Actually user expects "Up" to go "Forward" on screen.
        # Since camera is rotated ~45-55 deg X, and potentially 180 Y.
        
        # We need to adjust dx/dz based on player view (camera.rotation.y)
        # If rotation.y is 180 (Player 2), Left is Right, Up is Down (World Z)
        
        # Simple fix: Check camera.position or engine.current_player (but we avoid engine dep if possible, use camera.rotation)
        
        forward_factor = 1
        right_factor = 1
        
        # Rough check for P2 view
        if abs(camera.rotation_y) > 90:
            forward_factor = -1
            right_factor = -1
            
        real_dx = dx * self.move_step * right_factor
        real_dz = dz * self.move_step * forward_factor
        
        camera.x = clamp(camera.x + real_dx, -5, 20)
        camera.z = clamp(camera.z + real_dz, -20, 50)
        
    def zoom_camera(self, dir):
        # Zoom affects Y and slight Z to keep center
        # dir -1 = In (Lower Y), 1 = Out (Higher Y)
        
        new_y = clamp(camera.y + (dir * self.zoom_step), 5, 50)
        
        # Simple Z adjustment to maintain angle not strictly necessary if LookAt, but we use fixed rotation.
        # Let's just move Y for simplicity of "Height".
        camera.y = new_y
