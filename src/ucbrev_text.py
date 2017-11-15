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
valid_indices = set(range(num_arms))
delta = 1
num_rounds = int(math.floor(0.5 * math.log(time_horizon / math.exp(1), 2)))
print num_rounds

iteration = 0
reward = 0
for m in range(num_rounds):
    counts = [0] * num_arms
    n_m = int(math.ceil(2 * math.log(time_horizon * delta**2) / (delta**2)))
    goal = [n_m if i in valid_indices else 0 for i in range(num_arms)]
    while counts != goal:
        i = np.random.choice(list(valid_indices))
        if counts[i] >= n_m:
            continue
        new_reward = all_arms[i].sample()
        counts[i] += 1
        reward += new_reward
        print "\nIteration: %d" % iteration
        print "Robot chose arm %d" % i
        print "Reward: %.2f" % new_reward
        print "Total Reward: %.2f" % reward
        raw_input("Press <Enter> to continue...")
        iteration += 1
    s = math.sqrt(math.log(time_horizon * delta**2) / (2 * n_m))
    max_r = float('-inf')
    for i in valid_indices:
        if all_arms[i].average - s > max_r:
            max_r = all_arms[i].average - s
    for i in list(valid_indices):
        if all_arms[i].average + s < max_r:
            valid_indices.remove(i)
    delta = delta / 2
    print list(valid_indices)