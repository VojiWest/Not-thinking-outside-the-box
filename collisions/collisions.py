from ursina import Vec3, time
import math

def prevent_illegal_agent_movements(agents, square, platform, barriers, barrier_agents):

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
                keep_in_bounds(agents, square, platform)
                avoid_overlaps(agents, square, barriers, barrier_agents)
        if horizontal_distance_left < agent.scale_x:
            if left_agent < right_platform:
                # Move the agent slightly right to avoid the gap
                new_x = right_platform + agent.scale_x / 2 + buffer_distance
                agent.x = min(new_x, agent.x)  # Only move if needed to avoid a gap
                keep_in_bounds(agents, square, platform)
                avoid_overlaps(agents, square, barriers, barrier_agents)

        # Illegal Vertical gaps
        if vertical_distance_top < agent.scale_y:
            if top_agent > bottom_platform:
                # Move the agent slightly down to avoid the gap
                new_y = bottom_platform - agent.scale_y / 2 - buffer_distance
                agent.y = max(new_y, agent.y)  # Only move if needed
                keep_in_bounds(agents, square, platform)
                avoid_overlaps(agents, square, barriers, barrier_agents)
        if vertical_distance_bottom < agent.scale_y:
            if bottom_agent < top_platform:
                # Move the agent slightly up to avoid the gap
                new_y = top_platform + agent.scale_y / 2 + buffer_distance
                agent.y = min(new_y, agent.y)  # Only move if needed
                keep_in_bounds(agents, square, platform)
                avoid_overlaps(agents, square, barriers, barrier_agents)

def get_rotated_corners(square):
    # Get the half-size of the square (for scaling purposes)
    half_width = square.scale_x / 2
    half_height = square.scale_y / 2
    
    # Get the square's rotation in radians
    angle = math.radians(square.rotation_z)  # Assuming rotation_z is in degrees
    
    # Calculate the offsets for each corner (relative to the square's center)
    corners = [
        Vec3(-half_width, -half_height, 0),  # Bottom-left
        Vec3(half_width, -half_height, 0),   # Bottom-right
        Vec3(half_width, half_height, 0),    # Top-right
        Vec3(-half_width, half_height, 0),   # Top-left
    ]
    
    # Apply rotation to each corner
    rotated_corners = []
    for corner in corners:
        rotated_x = corner.x * math.cos(angle) - corner.y * math.sin(angle)
        rotated_y = corner.x * math.sin(angle) + corner.y * math.cos(angle)
        rotated_corners.append(Vec3(rotated_x + square.x, rotated_y + square.y, 0))
    
    return rotated_corners

def keep_in_bounds(agents, square, platform):
    ### Used to keep the agents and square within the platform bounds ###
    ### Given list of agents and square, check if they are within the platform bounds and push them back in if they are outside ###

    # Get the bounds of the square and the platform

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

    # Get rotated corners of the square
    corners = get_rotated_corners(square)
    
    # Check each corner for out-of-bounds and adjust the square position
    for corner in corners:
        if corner.y > top_platform:
            square.y -= (corner.y - top_platform)
        elif corner.y < bottom_platform:
            square.y += (bottom_platform - corner.y)
        if corner.x > right_platform:
            square.x -= (corner.x - right_platform)
        elif corner.x < left_platform:
            square.x += (left_platform - corner.x)

def keep_not_overlapping(square, barrier):
    # Get the barrier's bounds
    top_barrier = barrier.y + barrier.scale_y / 2
    bottom_barrier = barrier.y - barrier.scale_y / 2
    right_barrier = barrier.x + barrier.scale_x / 2
    left_barrier = barrier.x - barrier.scale_x / 2

    # Get the corners of the rotated square
    corners = get_rotated_corners(square)
    print("Checking for overlap")
    
    # Check each corner if it overlaps with the barrier and adjust the square position
    for corner in corners:
        # get closest point on the barrier to the corner
        dist_to_top = abs(top_barrier - corner.y)
        dist_to_bottom = abs(bottom_barrier - corner.y)
        dist_to_left = abs(left_barrier - corner.x)
        dist_to_right = abs(right_barrier - corner.x)


def move_agent_to_barrier_edge(barrier, agent):
    # Get the bounds of the barrier and the agent
    top_barrier = barrier.y + barrier.scale_y / 2
    bottom_barrier = barrier.y - barrier.scale_y / 2
    right_barrier = barrier.x + barrier.scale_x / 2
    left_barrier = barrier.x - barrier.scale_x / 2

    top_agent = agent.y + agent.scale_y / 2
    bottom_agent = agent.y - agent.scale_y / 2
    right_agent = agent.x + agent.scale_x / 2
    left_agent = agent.x - agent.scale_x / 2

    # Check if the agent intersects with the barrier
    if not (right_agent < left_barrier or left_agent > right_barrier or
            top_agent < bottom_barrier or bottom_agent > top_barrier):

        # Calculate distances to the nearest edge of the barrier
        dist_to_top = abs(top_barrier - bottom_agent)
        dist_to_bottom = abs(bottom_barrier - top_agent)
        dist_to_left = abs(left_barrier - right_agent)
        dist_to_right = abs(right_barrier - left_agent)

        # Find the nearest edge by comparing distances
        nearest_edge = min(dist_to_top, dist_to_bottom, dist_to_left, dist_to_right)

        # Move the agent to the nearest edge
        if nearest_edge == dist_to_top:
            # Move the agent just below the top of the barrier
            agent.y = top_barrier + agent.scale_y / 2
        elif nearest_edge == dist_to_bottom:
            # Move the agent just above the bottom of the barrier
            agent.y = bottom_barrier - agent.scale_y / 2
        elif nearest_edge == dist_to_left:
            # Move the agent just to the right of the left side of the barrier
            agent.x = left_barrier - agent.scale_x / 2
        elif nearest_edge == dist_to_right:
            # Move the agent just to the left of the right side of the barrier
            agent.x = right_barrier + agent.scale_x / 2

        return True  # The agent was moved
    return False  # No intersection, so no movement needed
    

def avoid_overlaps(agents, box, barriers, barrier_agents):
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
                # Calculate the distance between the agent and the barrier
                move_agent_to_barrier_edge(barrier, agent)

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
