from __future__ import division
import numpy as np
import pickle
import csv

################################################################################
# CONSTANTS/FUNCTIONS
DATA_FOLDER = "../data"
both_users = [1, 2, 5, 6, 8]
collab_only_users = [3, 4, 7, 9, 10]
PRETRAIN = 30
NUM_TURNS = 30

def disagreement(human, robot):
    human = human[PRETRAIN:]
    robot = robot[PRETRAIN:]
    d = 0
    for i, h in enumerate(human):
        if h != robot[i]:
            d += 1
    return d

################################################################################

disagreements_greedy = []
disagreements_optimal= []
disagreements_random = []

for user in collab_only_users:
    pkl_file = open("%s/user_%d/greedy.pkl" % (DATA_FOLDER, user), 'rb')
    greedy = pickle.load(pkl_file)
    pkl_file = open("%s/user_%d/optimal.pkl" % (DATA_FOLDER, user), 'rb')
    optimal = pickle.load(pkl_file)
    pkl_file = open("%s/user_%d/random.pkl" % (DATA_FOLDER, user), 'rb')
    random = pickle.load(pkl_file)

    dis_greedy = disagreement(greedy['human_decsions'], greedy['robot_decisions'])
    dis_optimal = disagreement(optimal['human_decsions'], optimal['robot_decisions'])
    dis_random = disagreement(random['human_decsions'], random['robot_decisions'])

    disagreements_greedy.append(dis_greedy)
    disagreements_optimal.append(dis_optimal)
    disagreements_random.append(dis_random)

with open('../data/collab_only_disagreements.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    headers = [['Greedy', 'Optimal', 'Random']]
    for i in range(len(both_users)):
        headers.append([disagreements_greedy[i], disagreements_optimal[i], \
                        disagreements_random[i]])
    wr.writerows(headers)
