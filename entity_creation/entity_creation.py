from ursina import Vec3
import random

from entities.agent import Agent
from entities.goal import Goal
from entities.payload import Payload

def in_bounds(point, obstacle, threshold=0.1):
    # Check if the point is not within the obstacle

    # check if obstacle has a scale_z attribute
    if hasattr(obstacle, 'scale_x'):
        if (point.x < obstacle.x - obstacle.scale_x / 2 - threshold) or (point.x > obstacle.x + obstacle.scale_x / 2 + threshold) or \
                (point.y < obstacle.y - obstacle.scale_y / 2 - threshold) or (point.y > obstacle.y + obstacle.scale_y / 2 + threshold):
            return False
    else:
        if (point.x < obstacle.x - 0.15) or (point.x > obstacle.x + 0.15) or \
                (point.y < obstacle.y - 0.15) or (point.y > obstacle.y + 0.15):
            return False
        
    return True

def create_positions(barriers, goal, square, grid_size=10, grid_resolution=0.5):
    positions = []
    obstacles = [goal, square] + barriers

    # Create a grid for efficient spatial checking
    grid = {}
    
    def get_grid_coords(point):
        return (int(point.x // grid_resolution), int(point.y // grid_resolution))
    
    def add_to_grid(point):
        coord = get_grid_coords(point)
        if coord not in grid:
            grid[coord] = []
        grid[coord].append(point)

    def is_valid_point(point):
        # Only check nearby cells in the grid
        coord = get_grid_coords(point)
        nearby_coords = [(coord[0]+dx, coord[1]+dy) for dx in range(-1, 2) for dy in range(-1, 2)]
        for nearby_coord in nearby_coords:
            if nearby_coord in grid:
                for obstacle in grid[nearby_coord]:
                    if not in_bounds(point, obstacle):
                        return False
        return True

    # Add initial obstacles to grid
    for obstacle in obstacles:
        add_to_grid(obstacle)

    # Randomly generate positions for agents
    for p in range(21):
        works = False
        while not works:
            i = random.uniform(-5.0, 5.0)
            j = random.uniform(-5.0, 5.0)
            point = Vec3(i, j, -0.01)
            if is_valid_point(point):
                works = True
                add_to_grid(point)
                positions.append(point)

    return positions


def create_agents_goal_and_payload(barriers, map_id):
    agent_size = 0.2

    if map_id == 3:
        goal = Goal(position=(3, -3.5, -0.01), scale=(1,1))
        square = Payload(position=(-2, 3, -0.01), scale=(1, 1))
    elif map_id == 1:
        goal = Goal(position=(-3, -3.5, -0.01), scale=(1,1))
        square = Payload(position=(0, 3, -0.01), scale=(1, 1))
    elif map_id == 0:
        goal = Goal(position=(-3, -3, -0.01), scale=(1,1))
        square = Payload(position=(-3, 3, -0.01), scale=(1, 1))
    else:
        goal = Goal(position=(-3, -3.5, -0.01), scale=(1,1))
        square = Payload(position=(2, 3, -0.01), scale=(1, 1))

    agent_positions = create_positions(barriers, goal, square)

    circle = Agent(position=agent_positions[0], scale=agent_size)
    circle1 = Agent(position=agent_positions[1], scale=agent_size)
    circle2 = Agent(position=agent_positions[2], scale=agent_size)
    circle3 = Agent(position=agent_positions[3], scale=agent_size)
    circle4 = Agent(position=agent_positions[4], scale=agent_size)
    circle5 = Agent(position=agent_positions[5], scale=agent_size)
    circle6 = Agent(position=agent_positions[6], scale=agent_size)
    circle7 = Agent(position=agent_positions[7], scale=agent_size)
    circle8 = Agent(position=agent_positions[8], scale=agent_size)
    circle9 = Agent(position=agent_positions[9], scale=agent_size)
    circle10 = Agent(position=agent_positions[10], scale=agent_size)
    circle11 = Agent(position=agent_positions[11], scale=agent_size)
    circle12 = Agent(position=agent_positions[12], scale=agent_size)
    circle13 = Agent(position=agent_positions[13], scale=agent_size)
    circle14 = Agent(position=agent_positions[14], scale=agent_size)
    circle15 = Agent(position=agent_positions[15], scale=agent_size)
    circle16 = Agent(position=agent_positions[16], scale=agent_size)
    circle17 = Agent(position=agent_positions[17], scale=agent_size)
    circle18 = Agent(position=agent_positions[18], scale=agent_size)
    circle19 = Agent(position=agent_positions[19], scale=agent_size)

    circles = [circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, 
               circle9, circle10, circle11, circle12, circle13, circle14, circle15, circle16, circle17, circle18, circle19]

    return circles, goal, square
