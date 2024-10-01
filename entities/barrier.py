from ursina import Entity, color, Vec3, time


class Barrier(Entity):
    def __init__(self, position, scale=(4.0, 0.75, 0.2), color=color.black, direction=1):
        # Initialize the parent Entity with visual attributes
        super().__init__(
            model='cube',
            scale=scale,
            color=color,
            position=position,
            collider='box'
        )
        self.direction = direction

    def update_direction(self):
        # Reverse the direction of the barrier when the update is called
        self.direction = self.direction * -1

    