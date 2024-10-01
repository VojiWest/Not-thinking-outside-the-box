import math
from ursina import Vec3

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


def get_main_direction(square_direction):
    # Check which component of the direction vector is larger and set the max_square_direction to that
    # This prevents the sticky behavior when the agent reaches the payload

    max_square_direction = Vec3(0, 0, 0)
    if abs(square_direction.x) > abs(square_direction.y):
        max_square_direction.x = square_direction.x
    else:
        max_square_direction.y = square_direction.y

    return max_square_direction


def get_distance_between_two_3D_points(point1, point2):
    # Calculate the Euclidean distance between two 3D points
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)


def get_direction_to(agent, obj):
    """
    Calculate the direction (angle) from the agent to the object in radians.
    Args:
        agent: The agent object, assumed to have a position attribute (x, y).
        obj: The target object, assumed to have a position attribute (x, y).
    Returns:
        The angle in radians between the agent and the object.
    """
    # Calculate the difference in positions
    dx = obj.x - agent.x
    dy = obj.y - agent.y

    # Return the angle using atan2, which handles full 360 degrees
    return math.atan2(dy, dx)


def get_distance(agent, obj):
    """
    Calculate the distance between the agent and the object.
    Args:
        agent: The agent object, assumed to have a position attribute (x, y).
        obj: The target object, assumed to have a position attribute (x, y).
    Returns:
        The Euclidean distance between the agent and the object.
    """
    # Calculate the difference in positions
    dx = obj.x - agent.x
    dy = obj.y - agent.y
    
    # Return the Euclidean distance
    return math.sqrt(dx**2 + dy**2)