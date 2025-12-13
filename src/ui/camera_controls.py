from ursina import *

class CameraControls(Entity):
    def __init__(self, parent_entity=None):
        super().__init__(parent=parent_entity if parent_entity else camera.ui)
        
        # Title
        Text(
            parent=self,
            text="Camera",
            position=(0, 0.6),
            scale=1.0,
            color=color.white,
            origin=(0, 0)
        )
        
        # Position Controls (arranged in cross pattern)
        base_x = 0
        base_y = 0.4
        
        self.btn_up = Button(
            parent=self,
            text='↑',
            scale=(0.06, 0.06),
            position=(base_x, base_y + 0.08),
            on_click=Func(self.move_camera, 0, 0, 1)
        )
        self.btn_down = Button(
            parent=self,
            text='↓',
            scale=(0.06, 0.06),
            position=(base_x, base_y - 0.08),
            on_click=Func(self.move_camera, 0, 0, -1)
        )
        self.btn_left = Button(
            parent=self,
            text='←',
            scale=(0.06, 0.06),
            position=(base_x - 0.08, base_y),
            on_click=Func(self.move_camera, -1, 0, 0)
        )
        self.btn_right = Button(
            parent=self,
            text='→',
            scale=(0.06, 0.06),
            position=(base_x + 0.08, base_y),
            on_click=Func(self.move_camera, 1, 0, 0)
        )
        
        # Zoom Controls
        Text(
            parent=self,
            text="Zoom",
            position=(0, 0.2),
            scale=0.8,
            color=color.white,
            origin=(0, 0)
        )
        
        self.btn_zoom_in = Button(
            parent=self,
            text='+',
            scale=(0.08, 0.06),
            position=(-0.05, 0.1),
            on_click=Func(self.zoom_camera, -1)
        )
        self.btn_zoom_out = Button(
            parent=self,
            text='-',
            scale=(0.08, 0.06),
            position=(0.05, 0.1),
            on_click=Func(self.zoom_camera, 1)
        )
        
        self.zoom_step = 2
        self.move_step = 2

    def move_camera(self, dx, dy, dz):
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
        new_y = clamp(camera.y + (dir * self.zoom_step), 5, 50)
        camera.y = new_y
