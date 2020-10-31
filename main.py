from ai import AI
from client import Client
import numpy as np
import math

ai = AI()
client = Client()

def wrap_pi(theta):
    theta = math.fmod(theta, 2 * math.pi)
    if (theta > math.pi):
        return theta - 2 * math.pi
    elif (theta < -math.pi):
        return theta + 2 * math.pi
    else:
        return theta;

def to_ai_format(robots, is_adv):
    if is_adv:
        return [[r.x, r.y] for r in robots]
    else:
        return [[r.x, r.y, wrap_pi(r.orientation)] for r in robots]

is_start = True
is_yellow = False

while True:
    blue, yellow, ball = client.receive()
    if (is_yellow):
        main = to_ai_format(yellow, False)
        adv = to_ai_format(blue, True)
    else:
        main = to_ai_format(blue, False)
        adv = to_ai_format(yellow, True)
    vels = ai.run_strategy(main[0], main[1], main[2], [ball.x, ball.y], adv[0], adv[1], adv[2], is_start)
    print(vels)
    client.send(vels, is_yellow)
    is_start = False
    
