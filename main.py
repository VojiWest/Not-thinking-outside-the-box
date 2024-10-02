from ursina import *
import math
import time
import numpy as np
from random import uniform
from entities.platform import Platform
from entities.barrier import Barrier
from entities.barrier_agent import Barrier_Agent
from entity_creation.entity_creation import *
from utils.physical_utils import *
from utils.math_utils import *



# Initialize the Ursina application
app = Ursina()

window.borderless = False  # Make sure this is set
window.size = (960, 600)   # Example size
# Set up the camera for 2D view by enabling orthographic mode
camera.orthographic = True
camera.fov = 10  # Field of view to adjust the zoom level

# Define movement speed of agents
move_speed = 0.5
current_map = 1

# Set up timer
start_time = time.time()
time_limit = 60

random_walk_directions = {}

""" CREATE ENTITIES """ # I should probably do this in a better way, but for now this is what I have


platform = Platform()


""" CREATE MAPS """

barriers = []
agents = []
barrier_agents = []


# Function to create maps
def create_map(map_id):
    global circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, goal, square, barrier

    # Clear existing entities (if needed)
    for entity in scene.entities:
        if entity != platform:  # Keep the platform persistent
            entity.disable()

    if map_id == 0:
        # Map 0: Initial configuration that we had from before
        barrier = Barrier(position=(-2, -2, -0.01), direction=1)
        barriers.append(barrier)

        circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, goal, square = create_agents_goal_and_payload(barriers)

    elif map_id == 1:
        # Map 1: One barrier in the middle moving side to side
        barrier = Barrier(position=(0, 0, -0.01), scale=(4, 0.5, 0.2), direction=1)
        barriers.append(barrier)

        circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, goal, square = create_agents_goal_and_payload(barriers)

    elif map_id == 2:
        # Map 2: Two vertical barriers moving in opposite directions
        barrier1 = Barrier(position=(0, 4, -0.01), scale=(0.5, 4, 0.5), direction=1)
        barrier2 = Barrier(position=(0, -4, -0.01), scale=(0.5, 4, 0.5), direction=-1)

        barriers.append(barrier1)
        barriers.append(barrier2)

        circle, circle1, circle2, circle3, circle4, circle5,circle6, circle7, circle8, circle9, goal, square = create_agents_goal_and_payload(barriers)

    elif map_id == 3:
        # Map 3: Two horizontal barriers, one higher than the other, moving in opposite directions
        barrier1 = Barrier(position=(-2, 1, -0.01), scale=(4, 0.5, 0.5), direction=1)
        barrier2 = Barrier(position=(2, -2, -0.01), scale=(4, 0.5, 0.5), direction=-1)

        barriers.append(barrier1)
        barriers.append(barrier2)

        circle, circle1, circle2, circle3, circle4, circle5,circle6, circle7, circle8, circle9, goal, square = create_agents_goal_and_payload(barriers)


    elif map_id == 4:
        # Map 4: Barriers appear as agents doing a random walk        
        # Initialize 10 barrier agents with random positions
        for i in range(10):
            # Generate random positions within a specific range
            x = uniform(-5, 5)  # Random x position between -5 and 5
            y = uniform(-3, 3)  # Random y position between -3 and 3
            z = -0.01 #uniform(-5, 5)  # Random z position between -5 and 5
            position = Vec3(x, y, z)
            
            agent = Barrier_Agent(position=position, scale=1)
            barrier_agents.append(agent)

        circle, circle1, circle2, circle3, circle4, circle5,circle6, circle7, circle8, circle9, goal, square = create_agents_goal_and_payload(barriers)

    
    agents.append(circle)
    agents.append(circle1)
    agents.append(circle2)
    agents.append(circle3)
    agents.append(circle4)
    agents.append(circle5)
    agents.append(circle6)
    agents.append(circle7)
    agents.append(circle8)
    agents.append(circle9)

#### ENTER THE INDEX OF MAP YOU WANT HERE, AND IF YOU WANT MOVING BARRIERS ####

create_map(2)
moving_barriers = False


############################################################################################

def prevent_illegal_agent_movements(agents, square):

    # Get the bounds of the square and the platform
    top_platform = platform.y + platform.scale_y / 2
    bottom_platform = platform.y - platform.scale_y / 2
    right_platform = platform.x + platform.scale_x / 2
    left_platform = platform.x - platform.scale_x / 2

    top_square = square.y + square.scale_y / 2
    bottom_square = square.y - square.scale_y / 2
    right_square = square.x + square.scale_x / 2
    left_square = square.x - square.scale_x / 2

    # Compute the horizontal and vertical distances between the box and the wall (platform)
    horizontal_distance_right = right_platform - right_square
    horizontal_distance_left = left_square - left_platform 
    vertical_distance_top = bottom_square - bottom_platform
    vertical_distance_bottom = top_platform - top_square

    for agent in agents:
        top_agent = agent.y + agent.scale_y / 2
        bottom_agent = agent.y - agent.scale_y / 2
        right_agent = agent.x + agent.scale_x / 2
        left_agent = agent.x - agent.scale_x / 2

    # Buffer distance to prevent agents from going too close to illegal gaps (when gap too small for them to fit)
    buffer_distance = 0.01  # keep this value small

    for agent in agents:
        top_agent = agent.y + agent.scale_y / 2
        bottom_agent = agent.y - agent.scale_y / 2
        right_agent = agent.x + agent.scale_x / 2
        left_agent = agent.x - agent.scale_x / 2

        # Compute the horizontal and vertical distances correctly
        horizontal_distance_right = right_platform - right_square
        horizontal_distance_left = left_square - left_platform
        vertical_distance_top = top_square - top_platform
        vertical_distance_bottom = bottom_square - bottom_platform

        # Illegal Horizontal gaps
        if horizontal_distance_right < agent.scale_x:
            if right_agent > left_platform:
                # Move the agent slightly left to avoid the gap
                new_x = left_platform - agent.scale_x / 2 - buffer_distance
                agent.x = max(new_x, agent.x)  # Only move if needed to avoid a gap
                keep_in_bounds(agents, square)
                avoid_overlaps(agents, square, barriers)
        if horizontal_distance_left < agent.scale_x:
            if left_agent < right_platform:
                # Move the agent slightly right to avoid the gap
                new_x = right_platform + agent.scale_x / 2 + buffer_distance
                agent.x = min(new_x, agent.x)  # Only move if needed to avoid a gap
                keep_in_bounds(agents, square)
                avoid_overlaps(agents, square, barriers)

        # Illegal Vertical gaps
        if vertical_distance_top < agent.scale_y:
            if top_agent > bottom_platform:
                # Move the agent slightly down to avoid the gap
                new_y = bottom_platform - agent.scale_y / 2 - buffer_distance
                agent.y = max(new_y, agent.y)  # Only move if needed
                keep_in_bounds(agents, square)
                avoid_overlaps(agents, square, barriers)
        if vertical_distance_bottom < agent.scale_y:
            if bottom_agent < top_platform:
                # Move the agent slightly up to avoid the gap
                new_y = top_platform + agent.scale_y / 2 + buffer_distance
                agent.y = min(new_y, agent.y)  # Only move if needed
                keep_in_bounds(agents, square)
                avoid_overlaps(agents, square, barriers)


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

def avoid_overlaps(agents, box, barriers):
    ### This function prevents agents, payloads, and barriers from overlapping each other ###

    for agent in agents:
        # Check for collision with the box
        if agent.intersects(box).hit:  # If agent and box overlap
            # Calculate the direction to push them away from each other
            direction = Vec3(agent.x - box.x, agent.y - box.y, 0).normalized()
            # Push agent away from the box
            agent.position += direction * time.dt * 0.5  # Adjust the 0.5 to control push strength

        # Check for collision between agents
        for other_agent in agents:
            if agent != other_agent and agent.intersects(other_agent).hit:  # If agents overlap
                # Calculate the direction to push them away from each other
                direction = Vec3(agent.x - other_agent.x, agent.y - other_agent.y, 0).normalized()
                # Push them away
                agent.position += direction * time.dt * 0.5  # Adjust the 0.5 to control push strength

        # Check for collision with barriers
        for barrier in barriers:
            if agent.intersects(barrier).hit:  # If agent overlaps with a barrier
                # print("Agent hit")
                # Calculate the distance between the agent and the barrier
                direction = Vec3(agent.x - barrier.x, agent.y - barrier.y, 0).normalized()
                # Push agent away from the box
                agent.position += direction * time.dt * 0.5  # Adjust the 0.5 to control push strength

                # TO DO: take into account how the direction of the barrier affects how the collision is being handled 

        for barrier_agent in barrier_agents:
            if agent.intersects(barrier_agent).hit:  # If agent overlaps with a barrier
                # print("Agent hit")
                # Calculate the distance between the agent and the barrier
                direction = Vec3(agent.x - barrier_agent.x, agent.y - barrier_agent.y, 0).normalized()
                # Push agent away from the barrier_agent
                agent.position += direction * time.dt * 0.5  # Adjust the 0.5 to control push strength

            if box.intersects(barrier_agent).hit:
                # Calculate the direction to push them away from each other
                direction = Vec3(box.x - barrier_agent.x, box.y - barrier_agent.y, 0).normalized()
                # Push the barrier away from the box
                box.position += direction * time.dt * 0.5  # Adjust the 0.5 to control push strength

            # if goal.intersects(barrier_agent).hit:
            #     # Calculate the direction to push them away from each other
            #     direction = Vec3(goal.x - barrier_agent.x, goal.y - barrier_agent.y, 0).normalized()
            #     # Push the barrier away from the box
            #     goal.position += direction * time.dt * 0.5  # Adjust the 0.5 to control push strength

            for other_barrier_agent in barrier_agents:
                if barrier_agent != other_barrier_agent and barrier_agent.intersects(other_barrier_agent).hit:  # If agents overlap
                    # Calculate the direction to push them away from each other
                    direction = Vec3(barrier_agent.x - other_barrier_agent.x, barrier_agent.y - other_barrier_agent.y, 0).normalized()
                    # Push them away
                    barrier_agent.position += direction * time.dt * 0.5  # Adjust the 0.5 to control push strength





    # Check for collision between the barriers and the box
    # for barrier in barriers:
    #     if barrier.intersects(box).hit:  # If barrier and box overlap
    #         # Calculate the direction to push them away from each other
    #         direction = Vec3(barrier.x - box.x, barrier.y - box.y, 0).normalized()
    #         # Push the barrier away from the box
    #         barrier.position += direction * time.dt * 0.5  # Adjust the 0.5 to control push strength


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
                agent.color = hsv(190, 0.9, 1)
            detected = True
            return detected
    if not detected:
        agent.color = color.red
        # rotate the agent 5 degrees
        new_rotation = (agent.rotation_z + 5) % 360 # keep the rotation within 0-360
        agent.rotation_z = new_rotation
        return detected

def search_for_entity(agent, target):
    # Check for target within cone of vision
    cone_angle = 40
    cone_length = 50
    found = search_cone(agent, target, cone_angle, cone_length)

    return found

def slide_barrier(barrier, barrier_speed, reverse=False):
    # Slide barrier side to side
    barrier_speed = 0.5
    if barrier.position.x > 3:
        barrier.update_direction()
    elif barrier.position.x < -3:
        barrier.update_direction()

    barrier_direction = barrier.direction
    if reverse:
        barrier.position -= Vec3(time.dt * barrier_speed * barrier_direction, 0, 0)
    else:
        barrier.position += Vec3(time.dt * barrier_speed * barrier_direction, 0, 0)

def move_agent_to_payload(agent, square, barriers):
    square_direction = Vec3(square.x - agent.x, square.y - agent.y, 0)  # Calculate the direction vector to the payload
    agent.position += square_direction.normalized() * time.dt * move_speed  # Move the agent towards the payload
    movement = square_direction.normalized() * time.dt * move_speed  # Calculate the movement vector

    # Check if the agent intersects with the payload
    if agent.intersects(square).hit:
        max_square_direction = get_main_direction(square_direction)  # Calculate the push direction based on the movement vector

        # Move the payload
        square.position += max_square_direction * time.dt * move_speed

        # Check for intersections with all barriers
        for barrier in barriers:
            if square.intersects(barrier).hit:  # If the payload intersects with a barrier after moving, move it back
                square.position -= max_square_direction * time.dt * move_speed
                break  # Stop checking further barriers once one collision is found

        # Check for collision again to prevent overlapping
        if agent.intersects(square).hit:  # If the agent intersects with the payload after moving, move it back
            agent.position -= movement

        return movement

def not_ideal_get_closest_entities(agent, full=False):
    # Cast ray in direction of goal not in direction of agent facing
    origin = agent.world_position
    origin.z = -0.1
    finds = []
    closest_colors = []
    search_list = [goal, circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9]
    search_list.remove(agent)

    for other_entity in search_list:
        if other_entity.color == (0,1,0,1):
            buffer_value = 0.1
            top_right = (other_entity.x + other_entity.scale_x/2 - buffer_value, other_entity.y + other_entity.scale_y/2 - buffer_value)
            top_left = (other_entity.x - other_entity.scale_x/2 + buffer_value, other_entity.y + other_entity.scale_y/2 - buffer_value)
            bottom_right = (other_entity.x + other_entity.scale_x/2 - buffer_value, other_entity.y - other_entity.scale_y/2+ buffer_value)
            bottom_left = (other_entity.x - other_entity.scale_x/2+ buffer_value, other_entity.y - other_entity.scale_y/2+ buffer_value)
            corners = [top_right, top_left, bottom_right, bottom_left]
            for corner in corners:
                # direction_goal = Vec3(other_entity.x - agent.x, other_entity.y - agent.y, 0).normalized()
                direction_goal = Vec3(corner[0] - agent.x, corner[1] - agent.y, 0).normalized()
                to_ignore = [agent]
                ray = raycast(origin, direction_goal, distance=50, ignore=to_ignore, debug=False)


                # Check if the raycast hit an entity
                found_entity = ray.entity
                if found_entity:  # Ensure found_entity is not None
                    closest_colors.append(found_entity.color)
                else:
                    # Handle case where no entity was found, if needed
                    continue  # Skip to the next corner

                found_entity = ray.entity
                closest_colors.append(found_entity.color)

    if full:
        return closest_colors

    if (0,1,0,1) in closest_colors:
        return "goal"
    else:
        return None

def move_in_barrier_direction(agent):
    barrier_speed = 0.5
    barrier_direction = barrier.direction
    move_distance = time.dt * barrier_speed * barrier_direction
    old_position = barrier.position - Vec3(time.dt * barrier_speed * barrier_direction, 0, 0)
    
    # Move the agent in the direction of the barrier
    agent.position += Vec3(move_distance, 0, 0)

    # Check for collision again to prevent overlapping
    if agent.intersects(barrier).hit:  # If agent and box overlap
        old_distance = get_distance_between_two_3D_points(old_position, agent.position)
        curr_distance = get_distance_between_two_3D_points(barrier.position, agent.position)
        # print("Old Distance: ", old_distance, "Current Distance: ", curr_distance)
        if old_distance > 1.02*curr_distance:

            # Calculate the direction to push them away from each other
            direction = Vec3(agent.position.x - barrier.position.x, agent.position.y - barrier.position.y, 0).normalized()
            
            # Push the agent and the box away from each other
            agent.position += direction * time.dt * 0.5  # Push agent away
            # barrier.position -= direction * time.dt * 0.5    # Push box away

def reposition(agent, obj):
    # Assume we have some functions that give us the agent's direction to object and goal
    object_direction = get_direction_to(agent, obj)  # Direction from agent to object
    goal_direction = get_direction_to(agent, goal)      # Direction from agent to goal
    
    # Calculate difference between the object's direction and goal's direction
    diff = object_direction - goal_direction
    diff = (diff + 2 * math.pi) % (2 * math.pi)  # Normalize angle difference to [0, 2*pi)
    
    # Determine whether to move clockwise or counterclockwise
    clockwise = diff >= math.pi
    
    # Parameters for movement vector
    min_dist = 0.1  # Minimum distance from object
    max_dist = 0.25  # Maximum distance from object
    
    # Get the current distance of the agent from the object
    object_distance = get_distance(agent, obj)
    
    # Force field around the object (we move perpendicular to the object vector)
    object_vec = np.array([math.cos(object_direction), math.sin(object_direction)])  # Convert object direction to a vector
    move_vec = np.array([-object_vec[1], object_vec[0]])  # Perpendicular vector for moving around
    if clockwise:
        move_vec *= -1  # Reverse direction if moving clockwise
    
    move_vec += object_vec  # Move towards the object if too far away

    # Apply movement to the agent
    # Normalize the movement vector if it's not already
    move_vec = move_vec / np.linalg.norm(move_vec)
    
    # Should move around another agent if it is in its way
    for other_agent in agents:
        if agent != other_agent:  
            other_agent_direction = get_direction_to(agent, other_agent)
            other_agent_vec = np.array([math.cos(other_agent_direction), math.sin(other_agent_direction)])
            norm_other_agent_vec = other_agent_vec / np.linalg.norm(other_agent_vec)
            rounded_other_agent_vec = (norm_other_agent_vec*100).astype(int)
            rounded_move_vec = (move_vec*100).astype(int)
            comparison = rounded_other_agent_vec == rounded_move_vec
            equal_arrays = comparison.all()
            if equal_arrays:
                print("object:", rounded_other_agent_vec)
                print("target:", rounded_move_vec)
                print("object in the way")
                move_vec = np.array([-other_agent_vec[1], -other_agent_vec[0]])

    move_vec = move_vec / np.linalg.norm(move_vec)
    move_vec += object_vec  # Move towards the object if too far away

    if clockwise:
        move_vec *= -1  # Reverse direction if moving clockwise

    agent.position += move_vec * time.dt * move_speed  # Move the agent towards the payload

    #face object
    object_direction = get_direction_to(agent, obj)  # Direction from agent to object
    angle_to_object = math.degrees(object_direction)
    agent.rotation_y += angle_to_object



# Dictionary to track how long each agent has reached the payload
reach_timers = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
reach_threshold = 10  # 10 seconds threshold
random_walk_states = {0: False, 1: False, 2: False, 3: False, 4: False}  # Track if an agent is in random walk mode

# Global variable to store the current random direction for each agent
random_walk_directions = {}

def random_walk(agent, agent_id, move_speed=1.0, change_direction_interval=1.0):
    """
    Move the agent in a random direction, and periodically change the direction.
    
    Args:
        agent: The agent object.
        agent_id: The unique ID of the agent (used to track direction).
        move_speed: Speed at which the agent moves.
        change_direction_interval: How often (in seconds) the agent should change direction.
    """
    # Check if the agent has a stored random direction
    if agent_id not in random_walk_directions:
        # Initialize with a random direction if not already present
        random_angle = random.uniform(0, 2 * math.pi)
        random_walk_directions[agent_id] = Vec3(math.cos(random_angle), math.sin(random_angle), 0)

    # Move the agent in the current random direction
    direction = random_walk_directions[agent_id]
    agent.position += direction.normalized() * time.dt * move_speed

    # Periodically change direction after the specified interval
    if time.time() % change_direction_interval < time.dt:
        random_angle = random.uniform(0, 2 * math.pi)
        random_walk_directions[agent_id] = Vec3(math.cos(random_angle), math.sin(random_angle), 0)

    avoid_overlaps([agent], square, barriers)
    keep_in_bounds(barrier_agents, square)

def move_barriers():
    # Slide barrier side to side
    barrier_speed = 0.5
    for barrier in barriers:  # Loop through all barriers in the list
        old_position = barrier.position
        slide_barrier(barrier, barrier_speed)
        
        for entity in [circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, square]:
            if entity.intersects(barrier).hit and check_entity_at_barrier_level(entity, barrier):
                old_distance = get_distance_between_two_3D_points(old_position, entity.position)
                curr_distance = get_distance_between_two_3D_points(barrier.position, entity.position)
                
                if old_distance > 1.02 * curr_distance:
                    # print("Agent hit")
                    # move_in_barrier_direction(entity)
                    slide_barrier(barrier, barrier_speed, reverse=True)
                    break  # Stop further checks once one barrier interaction occurs

def check_if_agent_turn_goal(agent, distance_threshold = 1):
    closest_entity_color = not_ideal_get_closest_entities(agent)
    if get_distance_between_two_3D_points(square.position, agent.position) > distance_threshold:
        if closest_entity_color != "goal" and agent.saw_goal_previous == True : # Agent can't see a goal
            print("Agent turned into a sub-goal")
            agent.color = color.green

    ### Still have to check if angle is greater than 90 between payload and goal

def check_if_goal_turn_agent(agent, distance_threshold = 1):
    if not_ideal_get_closest_entities(agent) == "goal": # Agent sees a goal
        agent.color = hsv(190, 0.9, 1) # Light blue
    elif get_distance_between_two_3D_points(square.position, agent.position) < distance_threshold:
        agent.color = hsv(190, 0.9, 1) # Light blue

    ### Still have to implement timeout

def at_payload(agent, distance_threshold = 0.01):
    # print(get_distance_between_two_3D_points(agent.position, square.position))
    if get_distance_between_two_3D_points(agent.position, square.position) < distance_threshold:
        return True
    return False

# Update function called every frame
def update():
    MacRae = False
    # Check if the square (payload) has reached the goal
    time_elapsed = time.time() - start_time
    # print("Time Elapsed: ", round(time_elapsed, 2))

    if square.intersects(goal).hit:
        print("Success! Payload reached the goal in", round(time_elapsed, 2), "seconds.")
        exit()

    if time_elapsed > time_limit:
        print("Time limit reached. Payload did not reach the goal.")
        exit()
    
    agent_targets = {}

    for index, agent in enumerate([circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9]):
        potential_new_state = None
       
        if agent.state == "Search":
            random_walk(agent, "agent"+str(index))

        # McRae stuff
        if MacRae:
            if not reach_payload(agent, square):
                if agent.color != color.green:
                    check_if_agent_turn_goal(agent)
                else:
                    check_if_goal_turn_agent(agent)

        # Check if the agent is not a sub-goal
        if agent.color != color.green:

            found_entity = not_ideal_get_closest_entities(agent)
            if found_entity == "goal":
                agent.saw_goal_previous = True

            potential_new_state = "Search"
            can_see_payload = search_for_entity(agent, square)
            if can_see_payload: # Check if the agent has can see the payload within its cone of vision

                random_walk_states[index] = False

                potential_new_state = "Approach"
                reached = reach_payload(agent, square) # Check if agent reached near the payload
                if reached:
                    found_entity = not_ideal_get_closest_entities(agent)
                    if found_entity != "goal" and at_payload(agent, distance_threshold=0.8) and agent.state_time < 600: # Goal is occluded
                        if agent.state == "Reposition":
                            print("switching to push")
                        potential_new_state = "Push"
                        movement = move_agent_to_payload(agent, square, barriers)
                        agent.saw_goal_previous = False
                    else:
                        if not found_entity:
                            print(f"Agent {index} repositioning due to: found entity")
                        if not at_payload(agent, distance_threshold=0.8):
                            print(f"Agent {index} repositioning due to: at payload")
                        if agent.state_time > 600:
                            print(f"Agent {index} repositioning due to: state timer")
                        potential_new_state = "Reposition"
                        # If agent hasn't reached the payload, reset its timer
                        # reach_timers[index] = 0

                        # move around the the payload (code below is a placeholder) - still working on this
                        reposition(agent, square)
                        agent.color = hsv(56, 1, 1)

                    if found_entity == "goal":
                        agent.saw_goal_previous = True
                        
                else:  
                    movement = move_agent_to_payload(agent, square, barriers)
        else:
            if MacRae:
                potential_new_state = "Sub-goal"

        if potential_new_state != agent.state:
            print(f"Agent {index} transitioning from {agent.state} to {potential_new_state} -- {agent.state_time}")
            agent.state = potential_new_state
            agent.state_time = 0
        else:
            agent.state_time += 1

     # Apply random walk to barrier agents
    for barrier_id, barrier_agent in enumerate(barrier_agents):
        random_walk(barrier_agent, barrier_id)
    
    keep_in_bounds(agents, square)
    prevent_illegal_agent_movements(agents, square)
    avoid_overlaps(agents, square, barriers)

    if moving_barriers == True: 
        move_barriers()

# Run the Ursina application
app.run()