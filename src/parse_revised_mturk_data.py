from __future__ import division 
import numpy as np
import ast
import csv
from parse_utils import *

objective_measures = True
subjective_measures = False
answers = False
num_arms = 6

user_data = {}
with open('../data/mturk_8_20_18/questiondata.csv', 'rb') as csvfile:
    for row in csv.reader(csvfile):
        user_data[row[0]] = {}
with open('../data/mturk_8_20_18/questiondata.csv', 'rb') as csvfile:
    for row in csv.reader(csvfile):
        user_data[row[0]][row[1]] = row[2]

collab_keys = ['random_hard_collaborate_suggest', 'optimal2_hard_collaborate_suggest', 
               'greedy_hard_collaborate_suggest', 'optimal_hard_collaborate_suggest']

observe_keys = ['random_hard_observe', 'optimal2_hard_observe',
                'greedy_hard_observe', 'optimal_hard_observe']
robot_order = ['random', 'optimal2', 'greedy', 'optimal']
robot_color_order = ['Yellow', 'Red', 'Green', 'Blue']

to_ignore = set()
for k, v in user_data.iteritems():
    for c in collab_keys:
        if c not in v.keys():
            to_ignore.add(k)

training_scores = []
training_entropy = []
robot_collab_scores = [[[] for _ in range(len(collab_keys))], 
                       [[] for _ in range(len(collab_keys))]]
robot_percent_agreements = [[[] for _ in range(len(collab_keys))], 
                            [[] for _ in range(len(collab_keys))]]
robot_initial_agreements = [[[] for _ in range(len(collab_keys))], 
                            [[] for _ in range(len(collab_keys))]]
robot_influences = [[[] for _ in range(len(collab_keys))], 
                    [[] for _ in range(len(collab_keys))]]
human_entropy = [[[] for _ in range(len(collab_keys))], 
                 [[] for _ in range(len(collab_keys))]]
for k in user_data.keys():
    if k in to_ignore:
        continue
    user_data[k]['training'] = ast.literal_eval(user_data[k]['training'])
    training_score = user_data[k]['training']['total_reward']
    training_scores.append(training_score)

    training_decisions = user_data[k]['training']['human_decisions']
    training_entropy.append(policy_entropy(training_decisions, num_arms))

    if set(observe_keys) <= set(user_data[k].keys()):
        # observe and collaborate condition
        condition = 0
    else:
        # collaborate only condition
        condition = 1

    for i, robot in enumerate(collab_keys):
        user_data[k][robot] = ast.literal_eval(user_data[k][robot])

        total_reward = user_data[k][robot]['total_reward']
        robot_collab_scores[condition][i].append(total_reward)

        agreement = percent_agreement(user_data[k][robot]['human_decisions'], user_data[k][robot]['robot_decisions'])
        robot_percent_agreements[condition][i].append(agreement)

        initial_agreement = percent_agreement_initial(user_data[k][robot]['before_suggest_decisions'], user_data[k][robot]['robot_decisions'])
        robot_initial_agreements[condition][i].append(initial_agreement)

        influence, _ = change_mind_to_robot(user_data[k][robot]['before_suggest_decisions'], user_data[k][robot]['human_decisions'], user_data[k][robot]['robot_decisions'])
        if influence is not None:
            robot_influences[condition][i].append(influence)
        else:
            robot_influences[condition][i].append(np.nan)
        
        # num_arms = len(user_data[k][robot]['arms_payoff_matrix'])
        entropy = policy_entropy(user_data[k][robot]['human_decisions'], num_arms)    
        human_entropy[condition][i].append(entropy)
if objective_measures:
    print robot_order
    print
    print np.average(training_scores)
    print
    print np.average(training_entropy)
    print 
    print np.average(robot_collab_scores[0], axis=1)
    print np.average(robot_collab_scores[1], axis=1)
    print
    print np.average(robot_percent_agreements[0], axis=1)
    print np.average(robot_percent_agreements[1], axis=1)
    print
    print np.average(robot_initial_agreements[0], axis=1)
    print np.average(robot_initial_agreements[1], axis=1)
    print
    print np.nanmean(robot_influences[0], axis=1)
    print np.nanmean(robot_influences[1], axis=1)
    print
    print np.average(human_entropy[0], axis=1)
    print np.average(human_entropy[1], axis=1)

    print policy_entropy([0,0,0,0,0, 1,1,1,1,1, 2,2,2,2,2, 3,3,3,3,3, 4,4,4,4,4, 5,5,5,5,5], 6)

if subjective_measures:
    robot_usefulness = [[[] for _ in range(len(collab_keys))], 
                        [[] for _ in range(len(collab_keys))]]
    robot_advice = [[[] for _ in range(len(collab_keys))], 
                    [[] for _ in range(len(collab_keys))]]
    robot_trust = [[[] for _ in range(len(collab_keys))], 
                   [[] for _ in range(len(collab_keys))]]
    robot_ranks = [[[] for _ in range(len(collab_keys))], 
                   [[] for _ in range(len(collab_keys))]]
    for k in user_data.keys():
        if k in to_ignore:
            continue
        if set(observe_keys) <= set(user_data[k].keys()):
            # observe and collaborate
            condition = 0
        else:
            # collaborate only
            condition = 1

        for i, color in enumerate(robot_color_order):
            useful = int(user_data[k]['useful_robot_' + color])
            robot_usefulness[condition][i].append(useful)

            advice = int(user_data[k]['advice_robot_' + color])
            robot_advice[condition][i].append(advice)

            trust = int(user_data[k]['trust_robot_' + color])
            robot_trust[condition][i].append(trust)
        ranking_order = ast.literal_eval(user_data[k]['robot_ranking_order'])
        ranking = ast.literal_eval(user_data[k]['robot_ranking'])
        for rank_idx, robot in enumerate(ranking_order):
            i = robot_color_order.index(robot)
            rank = ranking[rank_idx]

            robot_ranks[condition][i].append(rank)

    print "'I thought the robot's advice was useful'"
    print np.average(robot_usefulness[0], axis=1)
    print np.average(robot_usefulness[1], axis=1)
    print
    print "'I followed the robot's advice'"
    print np.average(robot_advice[0], axis=1)
    print np.average(robot_advice[1], axis=1)
    print
    print "'I trusted the robot'"
    print np.average(robot_trust[0], axis=1)
    print np.average(robot_trust[1], axis=1)
    print
    print "Rankings"
    print np.average(robot_ranks[0], axis=1)
    print np.average(robot_ranks[1], axis=1)
if answers:
    robot = collab_keys[3]
    for k in user_data.keys():
        if k in to_ignore:
            continue
        print user_data[k][robot]['answer']
