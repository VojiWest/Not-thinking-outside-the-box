from entities.agent import Agent
from entities.goal import Goal
from entities.payload import Payload


def create_agents_goal_and_payload():
    circle = Agent(position=(-1, 3, -0.01), scale=0.2)
    circle1 = Agent(position=(-3, 3.75, -0.01), scale=0.2)
    circle2 = Agent(position=(-2, 4.25, -0.01), scale=0.2)
    circle3 = Agent(position=(3, 4.5, -0.01), scale=0.2)
    circle4 = Agent(position=(1, 4, -0.01), scale=0.2)
    circle5 = Agent(position=(1, -3.5, -0.01), scale=0.2)

    goal = Goal(position=(-3, -3.5, -0.01), scale=(1,1))
    square = Payload(position=(2, 3, -0.01), scale=(1, 1))

    return circle, circle1, circle2, circle3, circle4, circle5, goal, square