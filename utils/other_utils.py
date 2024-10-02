# import ursina
import time


def update_timing(start_time, time_limit, square, goal):
    time_elapsed = time.time() - start_time
    print("Time Elapsed: ", round(time_elapsed, 2))

    if square.intersects(goal).hit:
        print("Success! Payload reached the goal in", round(time_elapsed, 2), "seconds.")
        exit()

    if time_elapsed > time_limit:
        print("Time limit reached. Payload did not reach the goal.")
        exit()