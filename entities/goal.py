from ursina import Entity, color

class Goal(Entity):
    def __init__(self, position):
        super().__init__(
            model='cube',
            scale=(2, 2),
            color=color.green,
            position=position,
            collider='box'
        )

    def update(self):
    # Define goal-specific behavior here
        pass