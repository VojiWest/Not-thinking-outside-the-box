from ursina import *

# Initialize the Ursina application
app = Ursina()

# Set up the camera for 2D view by enabling orthographic mode
camera.orthographic = True
camera.fov = 10  # Field of view to adjust the zoom level

# Define movement speed of agents
move_speed = 1

""" CREATE ENTITIES """ # I should probably do this in a better way, but for now this is what I have

# Create a flat 2D platform (background)
platform = Entity(
    model='quad',  # Use a 2D quad
    scale=(10, 10),
    color=color.pink,
    position=(0, 0, 1),  # Flat on the x-y plane at z=1 (which is further away from the camera) to prevent z-fighting or overlapping with other entities
    texture='white_cube',
    collider='box'  # Add a box collider to the platform to detect collisions
)

# create a barrier
barrier = Entity(
    model='quad',
    scale=(6.0, 0.75, 0.5), # added z scale (0.5) for testing
    color=color.black,
    position=(-2, -2, -0.01),  # Slightly raised to prevent z-fighting
    collider='box'  # Add a box collider to the square
)

# Create goal
goal = Entity(
    model='circle',
    scale=(1, 1),
    color=color.green,
    position=(-3, -3.5, -0.01),  # Slightly raised to prevent z-fighting
    collider='box'  # Add a box collider to the square
)

# Create a square (payload) on the platform (using quad as a 2D square)
square = Entity(
    model='quad',
    color=color.blue,
    scale=1,
    position=(2, 2, -0.01),  # Slightly raised to prevent z-fighting
    collider='box'  # Add a box collider to the square
)

### Create Agents ###

# Create a circle on the platform
circle = Entity(
    model='cube',
    color=color.white,
    scale=0.2,
    position=(-2, 3, -0.01),  # Slightly raised to prevent z-fighting
    collider='sphere'  # Add a box collider to the square
)

# Create another circle on the platform
circle1 = Entity(
    model='cube',
    color=color.white,
    scale=0.2,
    position=(-3, 4, -0.01),  # Slightly raised to prevent z-fighting
    collider='sphere'  # Add a box collider to the square
)

# Create another circle on the platform
circle2 = Entity(
    model='cube',
    color=color.white,
    scale=0.2,
    position=(-2, 4, -0.01),  # Slightly raised to prevent z-fighting
    collider='sphere'  # Add a box collider to the square
)

# Create another circle on the platform
circle3 = Entity(
    model='cube',
    color=color.white,
    scale=0.2,
    position=(3, 4, -0.01),  # Slightly raised to prevent z-fighting
    collider='sphere'  # Add a box collider to the square
)

# Create another circle on the platform
circle4 = Entity(
    model='cube',
    color=color.white,
    scale=0.2,
    position=(1, 4, -0.01),  # Slightly raised to prevent z-fighting
    collider='sphere'  # Add a box collider to the square
)


class Barrier():
    def __init__(self, direction):
        self.direction = direction

    def update(self):
        # Reverse the direction of the barrier
        self.direction = self.direction * -1

# Initialize the barrier
barrier_object = Barrier(0.5)

def keep_in_bounds(agents, square):
    ### Used to keep the agents and square within the platform bounds ###
    ### Given list of agents and square, check if they are within the platform bounds and push them back in if they are outside ###

    # Get the bounds of the square and the platform
    top_square = square.y + square.scale_y / 2
    bottom_square = square.y - square.scale_y / 2
    right_square = square.x + square.scale_x / 2
    left_square = square.x - square.scale_x / 2

    top_platform = platform.y + platform.scale_y / 2
    bottom_platform = platform.y - platform.scale_y / 2
    right_platform = platform.x + platform.scale_x / 2
    left_platform = platform.x - platform.scale_x / 2

    # Keep the agents within the platform bounds
    for agent in agents:
        top_agent = agent.y + agent.scale_y / 2
        bottom_agent = agent.y - agent.scale_y / 2
        right_agent = agent.x + agent.scale_x / 2
        left_agent = agent.x - agent.scale_x / 2

        if top_agent > top_platform:
            agent.y = top_platform - agent.scale_y / 2
        elif bottom_agent < bottom_platform:
            agent.y = bottom_platform + agent.scale_y / 2
        if right_agent > right_platform:
            agent.x = right_platform - agent.scale_x / 2
        elif left_agent < left_platform:
            agent.x = left_platform + agent.scale_x / 2

    # Check if the square is outside the platform, if so, push it back in
    if top_square > top_platform:
        square.y = top_platform - square.scale_y / 2
    elif bottom_square < bottom_platform:
        square.y = bottom_platform + square.scale_y / 2
    if right_square > right_platform:
        square.x = right_platform - square.scale_x / 2
    elif left_square < left_platform:
        square.x = left_platform + square.scale_x / 2

def get_angle_between_two_lines(line1, line2):
    # Line 1 vector (from point1 to point2)
    v1 = [line1[1].x - line1[0].x, line1[1].y - line1[0].y]
    
    # Line 2 vector (from point1 to point2)
    v2 = [line2[1].x - line2[0].x, line2[1].y - line2[0].y]
    
    # Dot product of v1 and v2
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    
    # Magnitudes of v1 and v2
    mag_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
    # Cosine of the angle between v1 and v2
    cos_angle = dot_product / (mag_v1 * mag_v2)
    
    # Clamp the value to avoid floating-point errors beyond [-1, 1]
    cos_angle = max(-1, min(1, cos_angle))
    
    # Get the angle in radians and convert it to degrees
    angle = math.degrees(math.acos(cos_angle))

    return angle

def get_facing_vector(agent, length):
    ### Get a vector pointing in the direction the agent is facing ###
    ### Given an agent and a length, return a vector pointing in the direction the agent is facing with the given length ###

    facing_direction = agent.transform[1]
    z_angle = facing_direction[2]
    dx = length * math.cos(math.radians(z_angle))
    dy = length * math.sin(math.radians(z_angle))
    return Vec3(dx, dy, -0.2).normalized() # Normalize the vector to get a unit vector and set z to -0.2 to prevent z-fighting

def get_face_and_target_lines(agent, target, cone_length):
    ### Get the lines representing the facing direction of the agent and the line to the target (payload) ###
    ### Given an agent, target, and cone length, return the lines representing the facing direction of the agent and the line to the target ###

    facing_direction = agent.transform[1]

    # line of facing direction
    face_line_1 = agent.position
    z_angle = facing_direction[2]
    dx = cone_length * math.cos(math.radians(z_angle))
    dy = cone_length * math.sin(math.radians(z_angle))
    x_new = agent.x + dx
    y_new = agent.y + dy
    face_line_2 = Vec3(x_new, y_new, z_angle)
    face_line = [face_line_1, face_line_2]

    # line to square
    target_line_1 = agent.position
    target_line_2 = Vec3(target.x, target.y, 0)
    target_line = [target_line_1, target_line_2]

    return face_line, target_line

def search_cone(agent, target, cone_angle, cone_length, payload=True):
    ### For a given agent, check if the target is within the cone of vision ###
    ### Given an agent, target, cone angle, and cone length, return True if the target is within the cone of vision, False otherwise ###

    distance = Vec3(target.x - agent.x, target.y - agent.y, 0).length()
    detected = False

    if distance < cone_length:
        # get the lines for the face and the target
        face_line, target_line = get_face_and_target_lines(agent, target, cone_length)
        # calculate angle between two lines
        angle = get_angle_between_two_lines(face_line, target_line)
        if angle < cone_angle:
            if payload == True:
                agent.color = color.green
            detected = True
            return detected
    if not detected:
        agent.color = color.red
        # rotate the agent 5 degrees
        new_rotation = (agent.rotation_z + 5) % 360 # keep the rotation within 0-360
        agent.rotation_z = new_rotation
        return detected

def search_for_box(agent, square):
    # Check for square within cone of vision
    cone_angle = 40
    cone_length = 50
    found = search_cone(agent, square, cone_angle, cone_length)

    return found

def reach_payload(agent, payload, threshold = 2.5):
    ### Check if the agent has reached the payload ###
    ### Given an agent, payload, and threshold, return True if the agent has reached the payload within the threshold distance, False otherwise ###

    distance = Vec3(payload.x - agent.x, payload.y - agent.y, 0).length()
    if distance < threshold:
        return True
    return False

def get_main_direction(square_direction):
    # Check which component of the direction vector is larger and set the max_square_direction to that
    # This prevents the sticky behavior when the agent reaches the payload

    max_square_direction = Vec3(0, 0, 0)
    if abs(square_direction.x) > abs(square_direction.y):
        max_square_direction.x = square_direction.x
    else:
        max_square_direction.y = square_direction.y

    return max_square_direction

def move_agent_to_payload(agent, square, barrier):
    ### Move the agent towards the payload ###
    square_direction = Vec3(square.x - agent.x, square.y - agent.y, 0) # Calculate the direction vector to the payload
    agent.position += square_direction.normalized() * time.dt * move_speed # Move the agent towards the payload
    movement = square_direction.normalized() * time.dt * move_speed # Calculate the movement vector (for later use if we need to move back since we hit an obstacle)

    # Check if the agent intersects with the payload
    if agent.intersects(square).hit:
        max_square_direction = get_main_direction(square_direction) # Calculate the push direction based on the movement vector (to prevent sticky behavior)

        # Calculate the push direction based on the movement vector
        square.position += max_square_direction * time.dt * move_speed
        if square.intersects(barrier).hit: # If the payload intersects with the barrier after moving, move it back
            square.position -= max_square_direction * time.dt * move_speed

        # Check for collision again to prevent overlapping
        if agent.intersects(square).hit: # If the agent intersects with the payload after moving, move it back
            agent.position -= movement

    return movement

# Update function called every frame
def update():

    # Check if the square (payload) has reached the goal
    if square.intersects(goal).hit:
        print("Success")

    for index, agent in enumerate([circle, circle1, circle2, circle3, circle4]):
        # Check if the agent has can see the payload within its cone of vision
        can_see_payload = search_for_box(agent, square)

        # Raycast to detect obstacles (can ignore this for now, i'm just testing)
        origin = agent.world_position
        origin.z = 0.5
        direction = get_facing_vector(agent, 40)
        ray = raycast(origin, direction, distance=200, debug=True)
        # print(agent.transform)
        # print("Agent", index, "ray", ray.entity, "direction", direction)

        if can_see_payload:
            # Check if agent reached the payload
            reached = reach_payload(agent, square)
            if reached:
                # Check if goal is occluded (still working on this)
                # clear = search_cone(agent, goal, 360, 50, False)
                clear = True
                if clear:
                    movement = move_agent_to_payload(agent, square, barrier)
                else:
                    # move around the the payload (code below is a placeholder) - still working on this
                    square.position += Vec3(0, 0, 0)
            else:  
                # Agent has not reached the payload yet so move towards it 
                ### Move the agent towards the payload ###
                movement = move_agent_to_payload(agent, square, barrier)

        # Check for if agent is colliding with the barrier
        if agent.intersects(barrier).hit: # If the agent intersects with the barrier, move it back
            agent.position -= movement

    # Keep the agents and square within the platform bounds
    keep_in_bounds([circle, circle1, circle2, circle3, circle4], square)


    # Slide barrier side to side
    barrier_speed = 0.5
    if barrier.position.x > 2:
        barrier_object.update()
    elif barrier.position.x < -2:
        barrier_object.update()
    barrier_direction = barrier_object.direction
    barrier.position += Vec3(time.dt * barrier_speed * barrier_direction, 0, 0)


# Run the Ursina application
app.run()