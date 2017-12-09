from __future__ import division
import numpy as np
import csv
import pickle
import pprint

################################################################################
# CONSTANTS/FUNCTIONS
DATA_FOLDER = "../data"
NUM_TURNS = 30
PRETRAIN = 30

def agreement(human, robot):
    human = human[PRETRAIN:]
    robot = robot[PRETRAIN:]
    a = 0
    for i, h in enumerate(human):
        if h == robot[i]:
            a += 1
    return a / NUM_TURNS
################################################################################

full_dataset = []

headers = ['User', 'Condition', 'Robot', 'Trust', 'Good Decisions', 'Intelligence',\
'Agreement', 'Reward']

with open("../data/obs_collab_survey.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(reader):
        if i == 0:
            continue
        user = row[0][5:]
        pkl_file = open("%s/user_%s/greedy.pkl" % (DATA_FOLDER, user), 'rb')
        greedy = pickle.load(pkl_file)
        pkl_file = open("%s/user_%s/optimal.pkl" % (DATA_FOLDER, user), 'rb')
        optimal = pickle.load(pkl_file)
        pkl_file = open("%s/user_%s/random.pkl" % (DATA_FOLDER, user), 'rb')
        random = pickle.load(pkl_file)

        greedy_row = []
        greedy_row.append(user)                 # User number
        greedy_row.append('Obs and Collab')     # Condition
        greedy_row.append('Greedy')             # Robot name
        greedy_row.append(row[1])               # Trust score
        greedy_row.append(row[4])               # Good Decisions score
        greedy_row.append(row[7])               # Intelligence score
        greedy_row.append(agreement(\
        greedy['human_decsions'], greedy['robot_decisions'])) # % Agreement
        greedy_row.append(greedy['reward'][-1])        # Final reward

        optimal_row = []
        optimal_row.append(user)                 # User number
        optimal_row.append('Obs and Collab')     # Condition
        optimal_row.append('Optimal')            # Robot name
        optimal_row.append(row[2])               # Trust score
        optimal_row.append(row[5])               # Good Decisions score
        optimal_row.append(row[8])               # Intelligence score
        optimal_row.append(agreement(\
        optimal['human_decsions'], optimal['robot_decisions'])) # % Agreement
        optimal_row.append(optimal['reward'][-1])        # Final reward

        random_row = []
        random_row.append(user)                 # User number
        random_row.append('Obs and Collab')     # Condition
        random_row.append('Random')             # Robot name
        random_row.append(row[3])               # Trust score
        random_row.append(row[6])               # Good Decisions score
        random_row.append(row[9])               # Intelligence score
        random_row.append(agreement(\
        random['human_decsions'], random['robot_decisions'])) # % Agreement
        random_row.append(random['reward'][-1])        # Final reward

        full_dataset.append(greedy_row)
        full_dataset.append(optimal_row)
        full_dataset.append(random_row)

with open("../data/collab_only_survey.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(reader):
        if i == 0:
            continue
        user = row[0][5:]
        pkl_file = open("%s/user_%s/greedy.pkl" % (DATA_FOLDER, user), 'rb')
        greedy = pickle.load(pkl_file)
        pkl_file = open("%s/user_%s/optimal.pkl" % (DATA_FOLDER, user), 'rb')
        optimal = pickle.load(pkl_file)
        pkl_file = open("%s/user_%s/random.pkl" % (DATA_FOLDER, user), 'rb')
        random = pickle.load(pkl_file)

        greedy_row = []
        greedy_row.append(user)                 # User number
        greedy_row.append('Collab')             # Condition
        greedy_row.append('Greedy')             # Robot name
        greedy_row.append(row[1])               # Trust score
        greedy_row.append(row[4])               # Good Decisions score
        greedy_row.append(row[7])               # Intelligence score
        greedy_row.append(agreement(\
        greedy['human_decsions'], greedy['robot_decisions'])) # % Agreement
        greedy_row.append(greedy['reward'][-1])        # Final reward

        optimal_row = []
        optimal_row.append(user)                 # User number
        optimal_row.append('Collab')             # Condition
        optimal_row.append('Optimal')            # Robot name
        optimal_row.append(row[2])               # Trust score
        optimal_row.append(row[5])               # Good Decisions score
        optimal_row.append(row[8])               # Intelligence score
        optimal_row.append(agreement(\
        optimal['human_decsions'], optimal['robot_decisions'])) # % Agreement
        optimal_row.append(optimal['reward'][-1])        # Final reward

        random_row = []
        random_row.append(user)                 # User number
        random_row.append('Collab')     # Condition
        random_row.append('Random')             # Robot name
        random_row.append(row[3])               # Trust score
        random_row.append(row[6])               # Good Decisions score
        random_row.append(row[9])               # Intelligence score
        random_row.append(agreement(\
        random['human_decsions'], random['robot_decisions'])) # % Agreement
        random_row.append(random['reward'][-1])        # Final reward

        full_dataset.append(greedy_row)
        full_dataset.append(optimal_row)
        full_dataset.append(random_row)

with open('../data/full_dataset.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    headers = [headers]
    for i in range(len(full_dataset)):
        headers.append(full_dataset[i])
    wr.writerows(headers)

