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
reward = 0
iteration = 0
for i, arm in enumerate(all_arms):
    new_reward = arm.sample()
    reward += new_reward
    print "\nIteration: %d" % iteration
    print "Robot chose arm %d" % i
    print "Reward: %.2f" % new_reward
    print "Total Reward: %.2f" % reward
    raw_input("Press <Enter> to continue...")
    iteration += 1

for n in range(num_arms, time_horizon):
    vals = [a.average + math.sqrt(2 * math.log(n) / a.samples) for a in all_arms]
    i = np.argmax(vals)
    new_reward = all_arms[i].sample()
    reward += new_reward
    print "\nIteration: %d" % iteration
    print "Robot chose arm %d" % i
    print "Reward: %.2f" % new_reward
    print "Total Reward: %.2f" % reward
    raw_input("Press <Enter> to continue...")
    iteration += 1
