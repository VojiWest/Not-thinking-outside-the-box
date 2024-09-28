from ursina import Entity, color

class Payload(Entity):
    def __init__(self, position, scale):
        super().__init__(
            model='cube',
            color=color.blue,
            scale=scale,
            position=position,
            collider='box'
        )

    def update(self):
        # Define any behaviors for the payload here
        pass