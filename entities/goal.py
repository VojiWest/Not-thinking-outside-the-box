from ursina import Entity, color

class Goal(Entity):
    def __init__(self, position, scale):
        super().__init__(
            model='cube',
            scale=scale,
            color=color.green,
            position=position,
            collider='box'
        )

    def update(self):
    # Define goal-specific behavior here
        pass