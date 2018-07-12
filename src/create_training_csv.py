from __future__ import division
import numpy as np
import csv
import ast

def get_robot_and_difficulty(s):
    if s == 'greedy_medium_observe':
        return 'greedy', 'medium'
    elif s == 'optimal_medium_observe':
        return 'optimal', 'medium'
    elif s == 'random_medium_observe':
        return 'random', 'medium'
    elif s == 'greedy2_medium_observe':
        return 'greedy2', 'medium'

user_data = {}
with open('mturk_questiondata.csv', 'rb') as csvfile:
    for row in csv.reader(csvfile):
        user_data[row[0]] = {}
with open('mturk_questiondata.csv', 'rb') as csvfile:
    for row in csv.reader(csvfile):
        user_data[row[0]][row[1]] = row[2]

collab_keys = ['greedy_easy_collaborate_suggest', 'random_hard_collaborate_suggest',
                'greedy2_hard_collaborate_suggest', 'greedy_hard_collaborate_suggest',
                'optimal_hard_collaborate_suggest', 'optimal_easy_collaborate_suggest',
                'random_easy_collaborate_suggest', 'greedy2_easy_collaborate_suggest']

observe_keys = ['greedy_medium_observe', 'optimal_medium_observe',
                'random_medium_observe', 'greedy2_medium_observe']
## for user_dict
all_keys = ['gender', 'robot_order', 'advice_robot_Green', 'trust_robot_Yellow',
            'useful_robot_Red', 'robot_colors', 'greedy_medium_observe', 'useful_robot_Green',
            'advice_robot_Blue', 'optimal_medium_observe', 'trust_robot_Red', 'greedy_easy_collaborate_suggest',
            'time_taken_Blue', 'useful_robot_Blue', 'useful_robot_Yellow', 'random_hard_collaborate_suggest',
            'time_taken_Red', 'time_taken_Yellow', 'robot_ranking', 'greedy2_hard_collaborate_suggest',
            'greedy_hard_collaborate_suggest', 'optimal_hard_collaborate_suggest', 'optimal_easy_collaborate_suggest',
            'trust_robot_Green', 'robot_ranking_order', 'advice_robot_Yellow', 'training',
            'observation_difficulty_order', 'trust_robot_Blue', 'collaborate_difficulty_order',
            'age', 'random_easy_collaborate_suggest', 'time_taken_Green', 'advice_robot_Red',
            'random_medium_observe', 'greedy2_easy_collaborate_suggest', 'greedy2_medium_observe']
## for collab_dict
collaborate_keys = ['robot_args', 'average_rewards', 'pretrain_decisions', 'before_suggest_decisions', 'arm_payoffs', 
                    'all_total_rewards', 'arm_probabilities', 'difficulty', 'total_reward', 'robot_type', 'times_chosen', 
                    'collaboration_type', 'human_decisions', 'robot_decisions', 'pretrain_payoffs', 'all_payoffs']
csv_headers = ['user id', 'training_reward']
csv_dataset = []

for user in user_data.keys():
    user_dict = user_data[user]
    total_reward = ast.literal_eval(user_dict['training'])['total_reward']
    csv_dataset.append([user, total_reward])

## writing data to csv
with open('../data/mturk_training_dataset.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    headers = [csv_headers]
    for i in range(len(csv_dataset)):
        headers.append(csv_dataset[i])
    wr.writerows(headers)
