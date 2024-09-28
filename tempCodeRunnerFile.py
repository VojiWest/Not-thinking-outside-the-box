def slide_barrier(barrier_object, barrier_speed, reverse=False):
    # Slide barrier side to side
    barrier_speed = 0.5
    if barrier_object.position.x > 2:
        barrier_object.update()
    elif barrier_object.position.x < -2:
        barrier_object.update()
    barrier_direction = barrier_object.direction
    if reverse:
        barrier_object.position -= Vec3(time.dt * barrier_speed * barrier_direction, 0, 0)
    else:
        barrier_object.position += Vec3(time.dt * barrier_speed * barrier_direction, 0, 0)