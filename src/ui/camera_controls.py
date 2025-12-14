from ursina import *

class CameraControls(Entity):
    def __init__(self, parent_entity=None):
        super().__init__(parent=parent_entity if parent_entity else camera.ui)
        
        # Title
        Text(
            parent=self,
            text="Camera Controls",
            position=(0, 0.1),
            scale=0.9,
            color=color.white,
            origin=(0, 0),
            z=-2
        )
        
        # Position Controls (arranged in cross pattern)
        base_x = 0
        base_y = -0.1
        spacing = 0.08
        btn_size = 0.07
        
        self.btn_up = Button(
            parent=self,
            text='UP',
            scale=(btn_size, btn_size),
            position=(base_x, base_y + spacing),
            on_click=Func(self.move_camera, 0, 0, 1),
            color=color.azure,
            z=-2
        )
        self.btn_down = Button(
            parent=self,
            text='DN',
            scale=(btn_size, btn_size),
            position=(base_x, base_y - spacing),
            on_click=Func(self.move_camera, 0, 0, -1),
            color=color.azure,
            z=-2
        )
        self.btn_left = Button(
            parent=self,
            text='LT',
            scale=(btn_size, btn_size),
            position=(base_x - spacing, base_y),
            on_click=Func(self.move_camera, -1, 0, 0),
            color=color.azure,
            z=-2
        )
        self.btn_right = Button(
            parent=self,
            text='RT',
            scale=(btn_size, btn_size),
            position=(base_x + spacing, base_y),
            on_click=Func(self.move_camera, 1, 0, 0),
            color=color.azure,
            z=-2
        )
        
        # Zoom Controls
        Text(
            parent=self,
            text="Zoom",
            position=(0, -0.3),
            scale=0.7,
            color=color.white,
            origin=(0, 0),
            z=-2
        )
        
        self.btn_zoom_in = Button(
            parent=self,
            text='+',
            scale=(0.08, 0.065),
            position=(-0.055, -0.4),
            on_click=Func(self.zoom_camera, -1),
            color=color.green,
            z=-2
        )
        self.btn_zoom_out = Button(
            parent=self,
            text='-',
            scale=(0.08, 0.065),
            position=(0.055, -0.4),
            on_click=Func(self.zoom_camera, 1),
            color=color.red,
            z=-2
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
