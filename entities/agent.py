from ursina import Entity, color, Vec3, time

class Agent(Entity):
    def __init__(self, position, scale):
        super().__init__(
            model='sphere',
            color=color.white,
            scale=scale,
            position=position,
            collider='sphere'
        )
        self.previous_position = self.position  # Initialize previous_position

    def update(self):
        self.update_position()  # Update previous position before any movement

    def update_position(self):
        self.previous_position = self.position  # Update previous position to current before moving


    def handle_collision(self, other):
        # Handle collisions with other entities (like barriers)
        if self.intersects(other).hit:
            # Calculate the direction to push the agent away from the barrier
            direction = (self.position - other.position).normalized()
            # Push the agent away from the barrier
            self.position += direction * time.dt * 0.5  # Adjust 0.5 to control push strength