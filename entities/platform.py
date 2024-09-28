from ursina import Entity, color


class Platform(Entity):
    def __init__(self):
        super().__init__(
            model='quad',
            scale=(10, 10),
            color=color.pink,
            position=(0, 0, 1),
            texture='white_cube',
            collider='box'
        )