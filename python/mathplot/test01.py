import matplotlib.pyplot as plt
import numpy as np
import math



def rec(des):

    params = {
        "track_width": 5,
        "distance_from_center": des,
        "speed": 1
    }   

    return reward_function(params)



def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']


    # Calculate 3 markers that are at varying distances away from the center line
    m0 = 0.2    

    max = 10

    des_ratio = distance_from_center/track_width

    if des_ratio > .99:
        return 1e-3

    if des_ratio < m0:
        reward = max + speed*3 - (des_ratio*max/2)**2


    else:
        reward = max + speed*3 - (m0*max/2)**2 - (des_ratio-m0) * track_width *((.5+speed))

    if reward < 0.2:
        reward = 0.2

    return float(reward)



# setting the x - coordinates
x = np.arange(0, 16+2, 0.1)
# setting the corresponding y - coordinates
y = [  rec(x1) for x1 in x ]

# plotting the points
plt.plot(x, y)

# function to show the plot
plt.show()

