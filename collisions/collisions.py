from ursina import Vec3, time

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


def keep_in_bounds(agents, square, platform):
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
