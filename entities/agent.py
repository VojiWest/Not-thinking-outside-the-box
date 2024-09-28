from ursina import Entity, color

class Agent(Entity):
    def __init__(self, position, scale):
        super().__init__(
            model='sphere',
            color=color.white,
            scale=scale,
            position=position,
            collider='sphere'
        )

    def update(self):
        # Define agent-specific behavior here
        pass