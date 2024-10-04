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
from utils.other_utils import *

from collisions.collisions import *



# Initialize the Ursina application
app = Ursina()

window.borderless = False  # Make sure this is set
window.size = (800, 800)   # Example size
# Set up the camera for 2D view by enabling orthographic mode
camera.orthographic = True
camera.fov = 10  # Field of view to adjust the zoom level

# Define movement speed of agents
move_speed = 0.5
current_map = 0

# Set up timer
start_time = time.time()
time_limit = 600

random_walk_directions = {}

platform = Platform()

""" CREATE MAPS """

barriers = []
agents = []
barrier_agents = []

modes = ["CEPtors", "McRae", "Chen"]
mode = modes[0]


# Function to create maps and entities
def create_map(map_id):
    global circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, circle10, circle11, circle12, circle13, circle14, circle15, circle16, circle17, circle18, circle19
    global goal, square, barrier

    # Clear existing entities (if needed)
    for entity in scene.entities:
        if entity != platform:  # Keep the platform persistent
            entity.disable()

    if map_id == 0:
        # Map 0: Initial configuration that we had from before
        barrier = Barrier(position=(-2.5, 0, -0.01), scale=(5, 1, 0.2), direction=1)
        barriers.append(barrier)

        agent_list, goal, square = create_agents_goal_and_payload(barriers, map_id)

    elif map_id == 1:
        # Map 1: One barrier in the middle moving side to side
        barrier = Barrier(position=(0, 0, -0.01), scale=(4, 0.5, 0.2), direction=1)
        barriers.append(barrier)

        agent_list, goal, square = create_agents_goal_and_payload(barriers, map_id)

    elif map_id == 2:
        # Map 2: Two vertical barriers moving in opposite directions
        barrier1 = Barrier(position=(0, 4, -0.01), scale=(0.5, 4, 0.5), direction=1)
        barrier2 = Barrier(position=(0, -4, -0.01), scale=(0.5, 4, 0.5), direction=-1)

        barriers.append(barrier1)
        barriers.append(barrier2)

        agent_list, goal, square = create_agents_goal_and_payload(barriers, map_id)

    elif map_id == 3:
        # Map 3: Two horizontal barriers, one higher than the other, moving in opposite directions
        barrier1 = Barrier(position=(-1.5, 1, -0.01), scale=(7, 1, 0.5), direction=1)
        barrier2 = Barrier(position=(1.5, -2, -0.01), scale=(7, 1, 0.5), direction=-1)

        barriers.append(barrier1)
        barriers.append(barrier2)

        agent_list, goal, square = create_agents_goal_and_payload(barriers, map_id)

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

        agent_list, goal, square = create_agents_goal_and_payload(barriers, map_id)

    circle = agent_list[0]
    circle1 = agent_list[1]
    circle2 = agent_list[2]
    circle3 = agent_list[3]
    circle4 = agent_list[4]
    circle5 = agent_list[5]
    circle6 = agent_list[6]
    circle7 = agent_list[7]
    circle8 = agent_list[8]
    circle9 = agent_list[9]
    circle10 = agent_list[10]
    circle11 = agent_list[11]
    circle12 = agent_list[12]
    circle13 = agent_list[13]
    circle14 = agent_list[14]
    circle15 = agent_list[15]
    circle16 = agent_list[16]
    circle17 = agent_list[17]
    circle18 = agent_list[18]
    circle19 = agent_list[19]

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
    agents.append(circle10)
    agents.append(circle11)
    agents.append(circle12)
    agents.append(circle13)
    agents.append(circle14)
    agents.append(circle15)
    agents.append(circle16)
    agents.append(circle17)
    agents.append(circle18)
    agents.append(circle19)

#### ENTER THE INDEX OF MAP YOU WANT HERE, AND IF YOU WANT MOVING BARRIERS ####

create_map(4)
moving_barriers = True


############################################################################################


def slide_barrier(barrier, barrier_speed, reverse=False):
    # Slide barrier side to side
    barrier_speed = 0.5
    barrier.time_in_direction += 1
    if barrier.position.x + barrier.scale_x/2 > platform.scale_x/2 and barrier.time_in_direction > 25:
        barrier.update_direction()
        barrier.time_in_direction = 0
    elif barrier.position.x - barrier.scale_x/2 < -platform.scale_x/2 and barrier.time_in_direction > 25:
        barrier.update_direction()
        barrier.time_in_direction = 0

    barrier_direction = barrier.direction
    if reverse:
        barrier.position -= Vec3(time.dt * barrier_speed * barrier_direction, 0, 0)
    else:
        barrier.position += Vec3(time.dt * barrier_speed * barrier_direction, 0, 0)

def move_agent_to_payload(agent, square, barriers):
    square_direction = Vec3(square.x - agent.x, square.y - agent.y, 0)  # Direction to the payload
    movement = square_direction.normalized() * time.dt * move_speed  # Calculate the movement vector

    agent.position += movement  # Move the agent towards the payload

    # Check if the agent intersects with the payload
    if agent.intersects(square).hit:
        max_square_direction = get_main_direction(square_direction)  # Calculate the push direction

        # Move the square
        square_movement = max_square_direction * time.dt * move_speed
        square.position += square_movement

        # Calculate the position difference between agent and square
        relative_position = Vec3(agent.x - square.x, agent.y - square.y, 0)

        # Rotation effect based on push location
        push_distance = relative_position.length()
        max_rotation_angle = 5  # Max rotation angle in radians
        rotation_angle = max_rotation_angle * (relative_position.normalized().dot(max_square_direction)) / push_distance

        # Apply rotation to the square
        square.rotation_z += rotation_angle

        # Collision check with barriers
        for barrier in barriers:
            if check_if_entities_intersect(square, barrier):
                # Reverse the position and rotation
                square.position -= square_movement
                square.rotation_z -= rotation_angle

                # Calculate movement not towards the barrier
                movement_not_on_barrier = remove_movement_towards_barrier(square, square_movement, barrier)
                square.position += movement_not_on_barrier

                # Move square away from the barrier to prevent sticking
                reverse_direction = Vec3(square.x - barrier.x, square.y - barrier.y, 0).normalized()
                square.position += reverse_direction * time.dt * move_speed

                # If still intersecting, move it slightly further out
                if check_if_entities_intersect(square, barrier):
                    square.position += reverse_direction * 0.2  # Fine-tuning to prevent overlap

        # Check again for agent-square collision
        if agent.intersects(square).hit:
            agent.position -= movement  # If agent intersects after moving, move it back

        return movement


def not_ideal_get_closest_entities(agent, entity_check="goal", full=False):
    # Cast ray in direction of goal not in direction of agent facing
    origin = agent.world_position
    origin.z = -0.1
    positions = []
    closest_colors = []
    search_list = [goal, circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, circle10, 
                   circle11, circle12, circle13, circle14, circle15, circle16, circle17, circle18, circle19, square]
    search_list.remove(agent)

    for other_entity in search_list:
        if other_entity.color == (0,1,0,1) or other_entity.color == (0,0,1,1):
            buffer_value = 0.1
            top_right = (other_entity.x + other_entity.scale_x/2 - buffer_value, other_entity.y + other_entity.scale_y/2 - buffer_value)
            top_left = (other_entity.x - other_entity.scale_x/2 + buffer_value, other_entity.y + other_entity.scale_y/2 - buffer_value)
            bottom_right = (other_entity.x + other_entity.scale_x/2 - buffer_value, other_entity.y - other_entity.scale_y/2 + buffer_value)
            bottom_left = (other_entity.x - other_entity.scale_x/2 + buffer_value, other_entity.y - other_entity.scale_y/2 + buffer_value)
            corners = [top_right, top_left, bottom_right, bottom_left]
            for corner in corners:
                if other_entity.scale_y < 0.3 and other_entity.scale_x < 0.3:
                    direction_goal = Vec3(other_entity.x - agent.x, other_entity.y - agent.y, 0).normalized()
                else:
                    direction_goal = Vec3(corner[0] - agent.x, corner[1] - agent.y, 0).normalized()
                to_ignore = [agent]
                ray = raycast(origin, direction_goal, distance=50, ignore=to_ignore, debug=False)

                # Check if the raycast hit an entity
                found_entity = ray.entity
                if found_entity:  # Ensure found_entity is not None
                    closest_colors.append(found_entity.color)
                    if found_entity.color == (0,1,0,1):
                        positions.append(found_entity.position)
                else:
                    # Handle case where no entity was found, if needed
                    continue  # Skip to the next corner

                # found_entity = ray.entity
                # closest_colors.append(found_entity.color)

    if full :
        if len(positions) > 0:
            return ("goal", positions[0])
        else:
            return (None, None)
        
    if entity_check == "goal":
        if (0,1,0,1) in closest_colors:
            return "goal"
        else:
            return None
        
    if entity_check == "payload":
        if (0,0,1,1) in closest_colors:
            return "payload"
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
        if old_distance > 1.02*curr_distance:

            # Calculate the direction to push them away from each other
            direction = Vec3(agent.position.x - barrier.position.x, agent.position.y - barrier.position.y, 0).normalized()
            
            # Push the agent and the box away from each other
            agent.position += direction * time.dt * 0.5  # Push agent away
            # barrier.position -= direction * time.dt * 0.5    # Push box away

def detect_color_in_front(agent, direction):
    # Cast a ray in the direction the agent is facing (self.forward)
    hit_info = raycast(agent.position, direction, distance=10)

    if hit_info.hit:
        return True
    else:
        return False

def reposition(agent, obj):
    speed = move_speed
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
    
    # Keep distance from object
    if object_distance > 2:
        move_vec += object_vec  # Move towards the object if too far away

    # Apply movement to the agent
    # Normalize the movement vector if it's not already
    move_vec = move_vec / np.linalg.norm(move_vec)
    # if detect_color_in_front(agent, move_vec):
    #     og = move_vec
    #     move_vec = np.array([math.cos(object_direction), -math.sin(object_direction)])
    #     move_vec += og
    #     if clockwise:
    #         move_vec *= -1  # Reverse direction if moving clockwise
        
    #     # Keep distance from object
    #     if object_distance > 2:
    #         move_vec += og  # Move towards the object if too far away

    # Apply movement vector scaled by speed
    agent.position += move_vec * time.dt * speed

    push_factor = 0.5
    for entity in [circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, circle10,
                   circle11, circle12, circle13, circle14, circle15, circle16, circle17, circle18, circle19]:
        if entity.intersects(agent).hit:
            # push the agent away from the entity based on the direction
            direction = (agent.position - entity.position).normalized()
            agent.position += direction * time.dt * speed * push_factor

        


# Dictionary to track how long each agent has reached the payload
reach_timers = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
reach_threshold = 10  # 10 seconds threshold
random_walk_states = {0: False, 1: False, 2: False, 3: False, 4: False}  # Track if an agent is in random walk mode

# Global variable to store the current random direction for each agent
random_walk_directions = {}

def random_walk(agent, agent_id, move_speed=1, change_direction_interval=2.0):
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

    avoid_overlaps([agent], square, barriers, barrier_agents)
    keep_in_bounds(barrier_agents, square, platform)


def move_barriers():
    # Slide barrier side to side
    barrier_speed = 0.5
    for barrier in barriers:  # Loop through all barriers in the list
        old_position = barrier.position
        slide_barrier(barrier, barrier_speed)
        moved_back = False
        
        for entity in [circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, circle10, 
                   circle11, circle12, circle13, circle14, circle15, circle16, circle17, circle18, circle19]:
            if entity.intersects(barrier).hit:
                if check_entity_at_barrier_level(entity, barrier):
                    old_distance = get_distance_between_two_3D_points(old_position, entity.position)
                    curr_distance = get_distance_between_two_3D_points(barrier.position, entity.position)
                    
                    if old_distance > 1.01 * curr_distance:
                        # move_in_barrier_direction(entity)
                        slide_barrier(barrier, barrier_speed, reverse=True)
                        moved_back = True
                        break  # Stop further checks once one barrier interaction occurs
        
        # print("Intersecting with barrier: ", check_if_entities_intersect(square, barrier))
        if not moved_back and check_if_entities_intersect(square, barrier):
            old_distance = get_distance_between_two_3D_points(old_position, entity.position)
            curr_distance = get_distance_between_two_3D_points(barrier.position, entity.position)
            
            # if old_distance > 1.01 * curr_distance:
            #     # move_in_barrier_direction(entity)
            #     print("Moving back")
            slide_barrier(barrier, barrier_speed, reverse=True)



def check_if_agent_turn_goal(agent):
    # if agent.state == "Search": # or agent.state == "Approach":
    closest_entity = not_ideal_get_closest_entities(agent)

    if mode == "CEPtors":
        if closest_entity == "goal":
            agent.time_since_last_seen_goal = 0
        else:
            agent.time_since_last_seen_goal += 1

        angle_condition = False
        if agent.last_goal_payload_angle is None or agent.last_goal_payload_angle > 70:
            angle_condition = True
        if agent.saw_goal_previous == True and angle_condition and closest_entity != "goal":
            agent.color = color.green

    if mode == "McRae":
        angle_condition = False
        if agent.last_goal_payload_angle > 90:
            angle_condition = True
        if agent.saw_goal_previous == True and angle_condition and closest_entity != "goal":
            agent.color = color.green

def check_if_goal_turn_agent(agent, distance_threshold = 1.25):
    closest_entity = not_ideal_get_closest_entities(agent)
    closest_entity_payload = not_ideal_get_closest_entities(agent, entity_check="payload")

    if mode == "CEPtors":
        if closest_entity_payload == "payload":
            agent.time_since_last_seen_payload = 0
        else:
            agent.time_since_last_seen_payload += 1

        if closest_entity == "goal":
            agent.time_since_last_seen_goal += 1
        else:
            agent.time_since_last_seen_goal = 0

        if agent.time_since_last_seen_goal > 5:
            agent.color = hsv(190, 0.9, 1) # Light blue
        elif get_distance_between_two_3D_points(square.position, agent.position) < distance_threshold and agent.time_since_last_seen_payload < 50:
            agent.color = hsv(190, 0.9, 1) # Light blue
        elif agent.state_time > 600:
            agent.color = hsv(190, 0.9, 1) # Light blue

    if mode == "McRae":
        if closest_entity == "goal":
            agent.color = hsv(190, 0.9, 1) # Light blue
        elif get_distance_between_two_3D_points(square.position, agent.position) < distance_threshold:
            agent.color = hsv(190, 0.9, 1) # Light blue
        elif agent.state_time > 600:
            agent.color = hsv(190, 0.9, 1) # Light blue


def at_payload(agent, distance_threshold = 0.05):
    if get_distance_between_two_3D_points(agent.position, square.position) < distance_threshold:
        return True
    return False

# Update function called every frame
def update():
    # Check if the square (payload) has reached the goal
    update_timing(start_time, time_limit, square, goal)
    
    agent_targets = {}

    for index, agent in enumerate([circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, circle10, 
                   circle11, circle12, circle13, circle14, circle15, circle16, circle17, circle18, circle19]):
        potential_new_state = None
         # If the agent is in random walk mode, make it do random walk
        # if random_walk_states[index]:
        #     random_walk(agent, index)  # Call your random walk function here
            # continue  # Skip the rest of the loop if the agent is in random walk mode

        # McRae stuff
        if mode == "McRae" or mode == "CEPtors":
            if agent.color != color.green:
                check_if_agent_turn_goal(agent)
            else:
                check_if_goal_turn_agent(agent)

        # Check if the agent is not a sub-goal
        if agent.color != color.green:

            found_entity, found_entity_position = not_ideal_get_closest_entities(agent, full=True)
            found_payloads = not_ideal_get_closest_entities(agent, entity_check="payload")
            if found_entity == "goal":
                agent.saw_goal_previous = True
                if found_payloads == "payload":
                    agent.last_goal_payload_angle = get_angle_between_two_points(agent.position, square.position, found_entity_position) 
            else:
                agent.saw_goal_previous = False
                # if agent.time_since_last_seen_payload > 5:
                agent.last_goal_payload_angle = -1               

            potential_new_state = "Search"
            can_see_payload = not_ideal_get_closest_entities(agent, entity_check="payload")
            if can_see_payload == "payload" and (agent.saw_goal_previous == True or agent.state == "Approach" or agent.state == "Reposition" or agent.state == "Push"): # Check if the agent can see the payload
                agent.color = hsv(190, 0.9, 1) # Light blue

                random_walk_states[index] = False

                potential_new_state = "Approach"
                reached = reach_payload(agent, square) # Check if agent reached near the payload
                if reached:
                    # Increment the timer for the agent if it's at the payload
                    # reach_timers[index] += time.dt  # Increment by delta time (time between frames)
                    
                    # if reach_timers[index] >= reach_threshold:
                    #     print(f"Agent {index} is starting random walk after 10 seconds at the payload.")
                    #     random_walk_states[index] = True  # Set random walk mode
                    #     continue  # Skip the rest of the loop for this agent

                    found_entity = not_ideal_get_closest_entities(agent)
                    recently_repositioned = False # (agent.state == "Reposition" and agent.state_time < 50)
                    if found_entity != "goal" and at_payload(agent, distance_threshold=9) and agent.state_time < 600 and not recently_repositioned: # Goal is occluded
                        potential_new_state = "Push"
                        movement = move_agent_to_payload(agent, square, barriers)
                        agent.saw_goal_previous = False
                    else:
                        potential_new_state = "Reposition"
                        # If agent hasn't reached the payload, reset its timer
                        # reach_timers[index] = 0
                        # print("Agent ", index, " repositioning for ", agent.state_time)

                        # move around the the payload (code below is a placeholder) - still working on this
                        reposition(agent, square)
                        agent.color = hsv(56, 1, 1) # Yellow
                        
                else:  
                    # If agent can't see the payload, reset its timer
                    # reach_timers[index] = 0
                    # Agent has not reached the payload yet so move towards it 
                    ### Move the agent towards the payload ###
                    movement = move_agent_to_payload(agent, square, barriers)
            else: # Random walk to find payload since can't see it
                agent.color = color.white
                random_walk(agent, index)
        else:
            potential_new_state = "Sub-goal"

        if potential_new_state != agent.state:
            # print(f"Agent {index} transitioning from {agent.state} to {potential_new_state} -- {agent.state_time}")
            agent.state = potential_new_state
            agent.state_time = 0
        else:
            agent.state_time += 1

    # Apply random walk to barrier agents
    if moving_barriers == True: 
        for barrier_id, barrier_agent in enumerate(barrier_agents):
            random_walk(barrier_agent, barrier_id)
    
    keep_in_bounds(agents, square, platform)
    prevent_illegal_agent_movements(agents, square, platform, barriers, barrier_agents)
    avoid_overlaps(agents, square, barriers, barrier_agents)

    if moving_barriers == True: 
        move_barriers()

# Run the Ursina application
app.run()