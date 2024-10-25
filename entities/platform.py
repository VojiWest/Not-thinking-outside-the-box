from ursina import Entity, color, hsv


class Platform(Entity):
    def __init__(self):
        super().__init__(
            model='quad',
            scale=(10, 10),
            color=hsv(343, 0.40, 1),
            position=(0, 0, 1),
            texture='white_cube',
            collider='box'
        )