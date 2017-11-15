from __future__ import division
import numpy as np
from arm import Arm
import math

###############################################################################
# CONSTANTS AND FUNCTIONS
num_arms = 3
time_horizon = 50
###############################################################################

all_arms = [Arm(0, 1), Arm(1, 1), Arm(1.1, 1)]
times_suboptimal = 0
reward = 0

for t in range(time_horizon):
    avg_rewards = [a.average for a in all_arms]
    best_arm = np.argmax(avg_rewards)

    c = False
    choice = raw_input("Enter arm number to choose [0-%d]: " % (num_arms-1))
    try:
        choice = int(choice)
        if choice in list(range(num_arms)):
            c = True
    except:
        pass
    while not c:
        choice = raw_input("Invalid. Enter arm to choose [0-%d]: " % (num_arms-1))
        try:
            choice = int(choice)
        except:
            continue
        if choice in list(range(num_arms)):
            c = True

    new_reward = all_arms[choice].sample()
    reward += new_reward
    print "\nIteration: %d" % t
    print "Reward: %.2f" % new_reward
    print "Total Reward: %.2f" % reward
    if t != 0:
        if choice != best_arm:
            times_suboptimal += 1
epsilon = times_suboptimal / time_horizon
print epsilon

