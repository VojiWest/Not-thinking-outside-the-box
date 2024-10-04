import math
from ursina import Vec3, Vec2

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


def get_angle_between_two_points(origin_pos, target_pos1, target_pos2):
    vector1 = Vec2(target_pos1.x - origin_pos.x, target_pos1.y - origin_pos.y)
    vector2 = Vec2(target_pos2.x - origin_pos.x, target_pos2.y - origin_pos.y)

    angle = math.degrees(math.acos(vector1.dot(vector2) / (vector1.length() * vector2.length() + 0.0001)))

    return angle

def check_if_entities_intersect(entity1, entity2):
    """
    Check if two entities intersect using Separating Axis Theorem (SAT).
    :param entity1: The first entity (rotated square or rectangle).
    :param entity2: The second entity (rotated square or rectangle).
    :return: True if the entities intersect, False otherwise.
    """
    # Get the corners of both entities
    corners1 = get_rotated_corners(entity1)
    corners2 = get_rotated_corners(entity2)

    # print(corners1, " --- ", corners2)

    # Get the edges (normals) of both entities
    edges1 = get_edges(corners1)
    edges2 = get_edges(corners2)

    # Check for separating axis on all edges of entity1
    for edge in edges1:
        if is_separating_axis(edge, corners1, corners2):
            return False  # If a separating axis is found, they don't intersect

    # Check for separating axis on all edges of entity2
    for edge in edges2:
        if is_separating_axis(edge, corners1, corners2):
            return False  # If a separating axis is found, they don't intersect

    # No separating axis found, the entities intersect
    return True

def get_rotated_corners(entity):
    # Assuming rotation around z-axis in a 2D plane
    angle_rad = math.radians(entity.rotation.z)  # Use the z-component for rotation
    
    half_width = entity.scale_x / 2
    half_height = entity.scale_y / 2

    # Define the four corners relative to the center of the entity
    corners = [
        Vec3(-half_width, -half_height, 0),
        Vec3(half_width, -half_height, 0),
        Vec3(half_width, half_height, 0),
        Vec3(-half_width, half_height, 0),
    ]

    # Apply rotation to each corner
    rotated_corners = []
    for corner in corners:
        rotated_x = corner.x * math.cos(angle_rad) - corner.y * math.sin(angle_rad)
        rotated_y = corner.x * math.sin(angle_rad) + corner.y * math.cos(angle_rad)
        rotated_corners.append(Vec3(rotated_x + entity.x, rotated_y + entity.y, 0))  # Translate back to entity's position

    return rotated_corners


def get_edges(corners):
    """
    Get the edges of the rectangle (the vectors between consecutive corners).
    :param corners: List of Vec3 representing the rectangle's corners.
    :return: List of edge vectors (Vec3).
    """
    edges = []
    for i in range(len(corners)):
        p1 = corners[i]
        p2 = corners[(i + 1) % len(corners)]
        edge = Vec3(p2.x - p1.x, p2.y - p1.y, 0)
        edges.append(edge)
    return edges


def is_separating_axis(edge, corners1, corners2):
    """
    Check if an edge is a separating axis between two sets of corners.
    :param edge: The edge vector.
    :param corners1: Corners of the first entity.
    :param corners2: Corners of the second entity.
    :return: True if the edge is a separating axis, False otherwise.
    """
    # Compute the normal of the edge (perpendicular vector)
    normal = Vec3(-edge.y, edge.x, 0)

    # Project corners of both entities onto the normal
    min_proj1, max_proj1 = project_onto_axis(normal, corners1)
    min_proj2, max_proj2 = project_onto_axis(normal, corners2)

    # Check if projections are disjoint (i.e., if there is a gap between them)
    if max_proj1 < min_proj2 or max_proj2 < min_proj1:
        return True  # A gap exists, so this is a separating axis

    return False  # No gap, not a separating axis


def project_onto_axis(axis, corners):
    """
    Project the corners of a rectangle onto an axis (normal) and find the min and max projections.
    :param axis: The axis to project onto.
    :param corners: The corners of the rectangle.
    :return: The minimum and maximum projection values.
    """
    min_proj = float('inf')
    max_proj = float('-inf')
    for corner in corners:
        projection = corner.x * axis.x + corner.y * axis.y
        min_proj = min(min_proj, projection)
        max_proj = max(max_proj, projection)
    return min_proj, max_proj


def project_onto_vector(v1, v2):
    """Project vector v1 onto v2."""
    v2_normalized = v2.normalized()
    return v2_normalized * (v1.dot(v2_normalized))

def remove_movement_towards_barrier(square, movement, barrier):
    # Get the nearest edge's normal vector of the barrier (simplified for axis-aligned barriers)
    nearest_normal = Vec3(0, 0, 0)  # This will hold the normal of the nearest edge

    # Calculate barrier edges
    top_barrier = barrier.y + barrier.scale_y / 2
    bottom_barrier = barrier.y - barrier.scale_y / 2
    right_barrier = barrier.x + barrier.scale_x / 2
    left_barrier = barrier.x - barrier.scale_x / 2

    # Get the closest side and the normal vector
    if square.y + square.scale_y/2 > top_barrier:
        nearest_normal = Vec3(0, 1, 0)  # Top edge: normal points up
    elif square.y - square.scale_y/2 < bottom_barrier:
        nearest_normal = Vec3(0, -1, 0)  # Bottom edge: normal points down
    if square.x - square.scale_x/2> right_barrier:
        nearest_normal = Vec3(1, 0, 0)  # Right edge: normal points right
    elif square.x + square.scale_x/2< left_barrier:
        nearest_normal = Vec3(-1, 0, 0)  # Left edge: normal points left

    # Project the movement vector onto the nearest edge's normal vector
    movement_towards_barrier = project_onto_vector(movement, nearest_normal)

    # Subtract the movement in the direction of the barrier's normal (keep perpendicular component)
    adjusted_movement = movement - movement_towards_barrier

    # Apply the remaining movement (which won't intersect with the barrier)
    square.position += adjusted_movement
    return adjusted_movement
