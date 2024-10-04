from ursina import Vec3

def check_entity_at_barrier_level(entity, barrier, thershold=0.0):
    # Check if the entity is at the same level as the barrier

    if abs(entity.y - barrier.y) < barrier.scale_y / 2 + thershold:
        return True


def reach_payload(agent, payload, threshold = 1):
    ### Check if the agent has reached the payload ###
    ### Given an agent, payload, and threshold, return True if the agent has reached the payload within the threshold distance, False otherwise ###

    distance = Vec3(payload.x - agent.x, payload.y - agent.y, 0).length()
    if distance < threshold:
        return True
    return False
