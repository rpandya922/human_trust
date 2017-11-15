from __future__ import division
import numpy as np
from arm import *
import math

###############################################################################
# CONSTANTS AND FUNCTIONS
num_arms = 3
time_horizon = 50
epsilon = 0.3
###############################################################################

all_arms = [BernoulliArm(0.5), BernoulliArm(0.3, 3), BernoulliArm(0.8, 0.5)]
reward = 0

for t in range(time_horizon):
    avg_rewards = [a.average for a in all_arms]
    best_arm = np.argmax(avg_rewards)
    be_greedy = np.random.choice([0, 1], p=[epsilon, 1 - epsilon])

    if be_greedy:
        i = best_arm
    else:
        i = np.random.choice(list(range(num_arms)))

    new_reward = all_arms[i].sample()
    reward += new_reward

    print "\nIteration: %d" % t+1
    print "Robot chose rm %d" % i
    print "Reward: %.2f" % new_reward
    print "Total Reward: %.2f" % reward
    raw_input("Press <Enter> to continue...")
