from ursina import *

# Initialize the Ursina application
app = Ursina()

# Set up the camera for 2D view by enabling orthographic mode
camera.orthographic = True
camera.fov = 10  # Field of view to adjust the zoom level

# Create a flat 2D platform (background)
platform = Entity(
    model='quad',  # Use a 2D quad
    scale=(10, 10),
    color=color.pink,
    position=(0, 0),  # Flat on the x-y plane
    texture='white_cube',
    collider='box'  # Add a box collider to the platform
)

# Create a square on the platform (using quad as a 2D square)
square = Entity(
    model='quad',
    color=color.black,
    scale=1,
    position=(2, 2),  # Slightly raised to prevent z-fighting
    collider='box'  # Add a box collider to the square
)

# Create a circle on the platform
circle = Entity(
    model='circle',
    color=color.white,
    scale=0.2,
    position=(2, 5),  # Slightly raised to prevent z-fighting
    collider='sphere'  # Add a box collider to the square
)

# Create another circle on the platform
circle2 = Entity(
    model='circle',
    color=color.white,
    scale=0.2,
    position=(2, 8),  # Slightly raised to prevent z-fighting
    collider='sphere'  # Add a box collider to the square
)

# Define movement speed
move_speed = 2

def keep_in_bounds(circle, circle2, square):
    top_circle = circle.y + circle.scale_y / 2
    bottom_circle = circle.y - circle.scale_y / 2
    right_circle = circle.x + circle.scale_x / 2
    left_circle = circle.x - circle.scale_x / 2

    top_circle2 = circle2.y + circle2.scale_y / 2
    bottom_circle2 = circle2.y - circle2.scale_y / 2
    right_circle2 = circle2.x + circle2.scale_x / 2
    left_circle2 = circle2.x - circle2.scale_x / 2

    top_square = square.y + square.scale_y / 2
    bottom_square = square.y - square.scale_y / 2
    right_square = square.x + square.scale_x / 2
    left_square = square.x - square.scale_x / 2

    top_platform = platform.y + platform.scale_y / 2
    bottom_platform = platform.y - platform.scale_y / 2
    right_platform = platform.x + platform.scale_x / 2
    left_platform = platform.x - platform.scale_x / 2

    # Check if the circle is outside the platform
    if top_circle > top_platform:
        circle.y = top_platform - circle.scale_y / 2
    elif bottom_circle < bottom_platform:
        circle.y = bottom_platform + circle.scale_y / 2
    if right_circle > right_platform:
        circle.x = right_platform - circle.scale_x / 2
    elif left_circle < left_platform:
        circle.x = left_platform + circle.scale_x / 2

    if top_circle2 > top_platform:
        circle2.y = top_platform - circle2.scale_y / 2
    elif bottom_circle2 < bottom_platform:
        circle2.y = bottom_platform + circle2.scale_y / 2
    if right_circle2 > right_platform:
        circle2.x = right_platform - circle2.scale_x / 2
    elif left_circle2 < left_platform:
        circle2.x = left_platform + circle2.scale_x / 2

    # Check if the square is outside the platform
    if top_square > top_platform:
        square.y = top_platform - square.scale_y / 2
    elif bottom_square < bottom_platform:
        square.y = bottom_platform + square.scale_y / 2
    if right_square > right_platform:
        square.x = right_platform - square.scale_x / 2
    elif left_square < left_platform:
        square.x = left_platform + square.scale_x / 2

# Update function to move the circle with WASD keys
def update():
    # Move the circle with WASD keys
    move = Vec3(0, 0, 0)  # Initial movement vector
    move2 = Vec3(0, 0, 0)  # Initial movement vector
    keys_clicked = []
    if held_keys['a']:  # Move left
        move.x = -time.dt * move_speed
        keys_clicked.append("a")
    if held_keys['d']:  # Move right
        move.x = time.dt * move_speed
        keys_clicked.append("d")
    if held_keys['w']:  # Move up
        move.y = time.dt * move_speed
        keys_clicked.append("w")
    if held_keys['s']:  # Move down
        move.y = -time.dt * move_speed
        keys_clicked.append("s")

    if held_keys['j']:  # Move left
        move2.x = -time.dt * move_speed
        keys_clicked.append("j")
    if held_keys['l']:  # Move right
        move2.x = time.dt * move_speed
        keys_clicked.append("l")
    if held_keys['i']:  # Move up
        move2.y = time.dt * move_speed
        keys_clicked.append("i")
    if held_keys['k']:  # Move down
        move2.y = -time.dt * move_speed
        keys_clicked.append("k")

    # Update the circle position
    circle.position += move
    circle2.position += move2
    moves = [move, move2]

    # Check for collision with the square and push the square away
    for index, agent in enumerate([circle, circle2]):
        if agent.intersects(square).hit:
            square_direction = Vec3(square.x - agent.x, square.y - agent.y, 0)
            max_square_direction = Vec3(0, 0, 0)
            if abs(square_direction.x) > abs(square_direction.y):
                max_square_direction.x = square_direction.x
            else:
                max_square_direction.y = square_direction.y

            # Calculate the push direction based on the movement vector
            push_direction = move.normalized()  # Use the direction of movement
            square.position += max_square_direction * time.dt * move_speed

            # Check for collision again to prevent overlapping
            if agent.intersects(square).hit:
                # print('Overlapping detected!')
                # set circle position to the edge of the square
                agent.position -= moves[index]

    # Keep the circle and square within the platform bounds
    keep_in_bounds(circle, circle2, square)


# Run the Ursina application
app.run()