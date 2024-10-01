from ursina import Vec3

def check_entity_at_barrier_level(entity, barrier, thershold=0.05):
    top_barrier = barrier.y + barrier.scale_y / 2
    bottom_barrier = barrier.y - barrier.scale_y / 2

    top_entity = entity.y + entity.scale_y / 2
    bottom_entity = entity.y - entity.scale_y / 2

    if bottom_entity * (1 + thershold) < top_barrier or top_entity > bottom_barrier * (1 + thershold):
        return True
    return False


def reach_payload(agent, payload, threshold = 1):
    ### Check if the agent has reached the payload ###
    ### Given an agent, payload, and threshold, return True if the agent has reached the payload within the threshold distance, False otherwise ###

    distance = Vec3(payload.x - agent.x, payload.y - agent.y, 0).length()
    if distance < threshold:
        return True
    return False
