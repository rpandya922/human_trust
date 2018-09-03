from __future__ import division
import numpy as np
import csv
import ast
from parse_utils import *

# experiment_type = "stats"
experiment_type = "observe"
num_arms = 6

# users who did best with greedy (kinda)
exploratory_users_initial = [0,1,2,4,5,6,8,9,10,13,14,17,21,22,23,24,25,26,27,28,29,32,34,35,37,39,41,43,44,45,46,48,50,51]
# users who did best with ucb2 (kinda)
greedy_users_initial = [3,7,11,12,15,16,18,19,20,30,31,33,36,38,40,42,47,49]

# misclassified: [2, 7, 13, 16]
exploratory_users = [0,1,2,4,5,6,8,9,10,11,13,14,17,19,21,22,23,24,25,26,27,28,29,32,34,35,37,38,39,41,43,44,45,46,47,48,50,51]
greedy_users = [3,7,12,15,16,18,20,30,31,33,36,40,42,49]

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
robot_order = ['0.9-Greedy', 'HA-UCB', '0.1-Greedy', 'UCB']
robot_color_order = ['Yellow', 'Red', 'Green', 'Blue']

csv_headers = ['user id', 'condition', 'robot', 'trust', 'usefulness', 'advice', 'total regret', 'percent agreement', 
              'percent initial agreement', 'rank', 'initial choice entropy', 'final choice entropy', 'time until explored', 'manual condition']
csv_dataset = []

csv_headers_training = ['user id', 'condition', 'total training regret', 'policy entropy', 'time until explored', 'manual condition']
csv_dataset_training = []

# since some influence numbers can be nan (people never disagree with robot), so must do this separately
csv_headers_influence = ['user id', 'condition', 'robot', 'influence', 'manual condition']
csv_dataset_influence = []

to_ignore = set()
for k, v in user_data.iteritems():
    for c in collab_keys:
        if c not in v.keys():
            to_ignore.add(k)
to_ignore.add('A5NHP0N1XC09K:3TS1AR6UQR9BAHNBZANTRDU5WLW7FQ')

user_idx = 0
for k in user_data.keys():
    if k in to_ignore:
        continue

    if experiment_type == "observe":
        if set(observe_keys) <= set(user_data[k].keys()):
            # observe and collaborate condition
            condition = "observe and collaborate"
        else:
            # collaborate only condition
            condition = "collaborate"
    elif experiment_type == "stats":
        condition_num = int(user_data[k]['condition'])
        # if condition_num == 0:
        #     condition = "no stats"
        # elif condition_num == 1:
        #     condition = "mean"
        # elif condition_num == 2:
        #     condition = "num pulls"
        # elif condition_num == 3:
        #     condition = "all stats"
        if condition_num == 0:
            condition = "no stats"
        elif condition_num == 1:
            condition = "stats"
    if user_idx in exploratory_users:
            manual_condition = "Group 2"
    elif user_idx in greedy_users:
        manual_condition = "Group 1"

    user_data[k]['training'] = ast.literal_eval(user_data[k]['training'])
    
    training_regret = (30*2.9) - user_data[k]['training']['total_reward']
    training_decisions = user_data[k]['training']['human_decisions']
    training_entropy = policy_entropy(training_decisions, num_arms)
    time_until_explored = time_until_all_explored(training_decisions, num_arms)

    # if experiment_type == "stats":
        # csv_dataset.append([k, condition, "training", None, None, None, training_score, None, None, None, None, 
        #     training_entropy, time_until_explored])
    # csv_dataset.append([k, condition, "Human Alone", None, None, None, training_score, None, None, None, None, 
    #         training_entropy, time_until_explored])

    csv_dataset_training.append([k, condition, training_regret, training_entropy, time_until_explored, manual_condition])

    ranking_order = ast.literal_eval(user_data[k]['robot_ranking_order'])
    ranking = ast.literal_eval(user_data[k]['robot_ranking'])

    for i, robot in enumerate(collab_keys):
        user_data[k][robot] = ast.literal_eval(user_data[k][robot])

        robot_name = get_robot_name(robot)
        total_regret = 30*2.9 - user_data[k][robot]['total_reward']
        agreement = percent_agreement(user_data[k][robot]['human_decisions'], user_data[k][robot]['robot_decisions'])
        initial_agreement = percent_agreement_initial(user_data[k][robot]['before_suggest_decisions'], user_data[k][robot]['robot_decisions'])
        influence, _ = change_mind_to_robot(user_data[k][robot]['before_suggest_decisions'], user_data[k][robot]['human_decisions'], user_data[k][robot]['robot_decisions'])
        initial_choice_entropy = policy_entropy(user_data[k][robot]['human_decisions'], num_arms)
        before_suggest_decisions = np.array(user_data[k][robot]['before_suggest_decisions']) - 1
        final_choice_entropy = policy_entropy(before_suggest_decisions, num_arms)
        time_until_explored = time_until_all_explored(user_data[k][robot]['human_decisions'], num_arms)

        color = robot_color_order[i]
        useful = int(user_data[k]['useful_robot_' + color])
        advice = int(user_data[k]['advice_robot_' + color])
        trust = int(user_data[k]['trust_robot_' + color])

        ####################################################################################################################
        # CHECK THIS
        rank_idx = ranking_order.index(color)
        rank = ranking[rank_idx]
        ####################################################################################################################

        # if robot == "optimal2_hard_collaborate_suggest" and experiment_type == "stats":
        csv_dataset.append([k, condition, robot_name, trust, useful, advice, total_regret, agreement, 
              initial_agreement, rank, initial_choice_entropy, final_choice_entropy, time_until_explored, manual_condition])
        if influence is not None:
            csv_dataset_influence.append([k, condition, robot_name, influence, manual_condition])
    user_idx += 1

## writing data to csv
with open('../data/aaai_submission/jmp_full_dataset.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    headers = [csv_headers]
    for i in range(len(csv_dataset)):
        headers.append(csv_dataset[i])
    wr.writerows(headers)

with open('../data/aaai_submission/jmp_training_dataset.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    headers = [csv_headers_training]
    for i in range(len(csv_dataset_training)):
        headers.append(csv_dataset_training[i])
    wr.writerows(headers)

with open('../data/aaai_submission/jmp_influence_dataset.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    headers = [csv_headers_influence]
    for i in range(len(csv_dataset_influence)):
        headers.append(csv_dataset_influence[i])
    wr.writerows(headers)