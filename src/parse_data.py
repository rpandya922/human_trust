from __future__ import division
from utils import *
import numpy as np
import pickle
import pprint
import itertools
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

################################################################################
# CONSTANTS/FUNCTIONS
DATA_FOLDER = '../data/user_'
pp = pprint.PrettyPrinter()
PRETRAIN = 30
NUM_TURNS = 30

def disagreement(human, robot):
    human = human[30:]
    robot = robot[30:]
    d = 0
    for i, h in enumerate(human):
        if h != robot[i]:
            d += 1
    return d / NUM_TURNS
################################################################################
fig, axes = plt.subplots(nrows=2, ncols=2)
axes = np.ndarray.flatten(np.array(axes))

# palette = itertools.cycle(sns.color_palette())
# sns.set_palette("Reds")
sns.set_color_codes()

for user in [1, 2, 3, 4]:
    i = user - 1
    pkl_file = open("%s%d/greedy.pkl" % (DATA_FOLDER, user), 'rb')
    greedy = pickle.load(pkl_file)
    pkl_file = open("%s%d/optimal.pkl" % (DATA_FOLDER, user), 'rb')
    optimal = pickle.load(pkl_file)
    pkl_file = open("%s%d/random.pkl" % (DATA_FOLDER, user), 'rb')
    random = pickle.load(pkl_file)

    dis_greedy = disagreement(greedy['human_decsions'], greedy['robot_decisions'])
    dis_optimal = disagreement(optimal['human_decsions'], optimal['robot_decisions'])
    dis_random = disagreement(random['human_decsions'], random['robot_decisions'])

    ax = axes[i]
    # ax.bar(0, dis_greedy, 1, color=next(palette), label='greedy')
    # ax.bar(1, dis_optimal, 1, color=next(palette), label='optimal')
    # ax.bar(2, dis_random, 1, color=next(palette), label='random')
    ax.bar(0, dis_greedy, 1, color='b', label='greedy')
    ax.bar(1, dis_optimal, 1, color='r', label='optimal')
    ax.bar(2, dis_random, 1, color='g', label='random')
    ax.legend(loc='upper right')
plt.show()
