from __future__ import division
import numpy as np
import csv
import ast
import matplotlib.pyplot as plt

def time_until_all_explored(human_decisions, arm_payoffs):
    num_arms = len(arm_payoffs)
    explored = set()
    for i in range(30):
        explored.add(human_decisions[i])
        if set(range(num_arms)) <= explored:
            return i
    return 30
def num_explored_arms(human_decisions):
    explored = set()
    explored_each_iter = [0]
    for i in range(30):
        explored.add(human_decisions[i])
        explored_each_iter.append(len(explored))
    return explored_each_iter
def get_robot_and_difficulty(s):
    if s == 'greedy_easy_collaborate_suggest':
        return 'greedy', 'easy'
    elif s == 'greedy_hard_collaborate_suggest':
        return 'greedy', 'hard'
    elif s == 'greedy2_easy_collaborate_suggest':
        return 'greedy2', 'easy'
    elif s == 'greedy2_hard_collaborate_suggest':
        return 'greedy2', 'hard'
    elif s == 'optimal_easy_collaborate_suggest':
        return 'optimal', 'easy'
    elif s == 'optimal_hard_collaborate_suggest':
        return 'optimal', 'hard'
    elif s == 'random_easy_collaborate_suggest':
        return 'random', 'easy'
    elif s == 'random_hard_collaborate_suggest':
        return 'random', 'hard'
def calc_error_bounds(data):
    n = np.array(data).shape[0]
    sample_mean = np.mean(data, axis=0)
    sample_std = np.std(data, axis=0)
    return (1 / np.sqrt(n)* sample_std)

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

explored_g = []
explored_g2 = []
explored_o = []
explored_r = []

GREEDY_COLOR = '#1eb0ff'
# GREEDY2_COLOR = '#00ba72'
GREEDY2_COLOR = 'g'
# OPTIMAL_COLOR = '#ff9a02'
OPTIMAL_COLOR = '#ff8330'
RANDOM_COLOR = '#6b6761'

for user in user_data.keys():
    user_dict = user_data[user]
    if set(observe_keys) <= set(user_dict.keys()):
        # observe and collaborate condition
        condition = 'observe and collaborate'
    elif set(collab_keys) <= set(user_dict.keys()):
        # collaborate condition
        condition = 'collaborate'
    else:
        continue
    for key in collab_keys:
        collab_dict = ast.literal_eval(user_dict[key])
        robot, difficulty = get_robot_and_difficulty(key)
        if difficulty == 'easy':
            continue
        try:
            if robot == 'greedy':
                trust = user_dict['trust_robot_Green']
                usefulness = user_dict['useful_robot_Green']
                advice = user_dict['advice_robot_Green']
            elif robot == 'greedy2':
                trust = user_dict['trust_robot_Red']
                usefulness = user_dict['useful_robot_Red']
                advice = user_dict['advice_robot_Red']
            elif robot == 'optimal':
                trust = user_dict['trust_robot_Blue']
                usefulness = user_dict['useful_robot_Blue']
                advice = user_dict['advice_robot_Blue']
            elif robot == 'random':
                trust = user_dict['trust_robot_Yellow']
                usefulness = user_dict['useful_robot_Yellow']
                advice = user_dict['advice_robot_Yellow']
        except:
            ## user did not finish interacting with all robots
            continue
        
        human_decisions = collab_dict['human_decisions']
        explore = num_explored_arms(human_decisions)

        if robot == 'greedy':
            explored_g.append(explore)
        elif robot == 'greedy2':
            explored_g2.append(explore)
        elif robot == 'optimal':
            explored_o.append(explore)
        elif robot == 'random':
            explored_r.append(explore)

g_error = calc_error_bounds(explored_g)
g2_error = calc_error_bounds(explored_g2)
o_error = calc_error_bounds(explored_o)
r_error = calc_error_bounds(explored_r)

avg_explored_g = np.average(explored_g, axis=0)
avg_explored_g2 = np.average(explored_g2, axis=0)
avg_explored_o = np.average(explored_o, axis=0)
avg_explored_r = np.average(explored_r, axis=0)
x = range(0, 31)

plt.plot(x, avg_explored_g, c=GREEDY_COLOR, label='0.1-Greedy')
plt.plot(x, avg_explored_g2, c=GREEDY2_COLOR, label='0.3-Greedy')
plt.plot(x, avg_explored_o, c=OPTIMAL_COLOR, label='Optimal')
plt.plot(x, avg_explored_r, c=RANDOM_COLOR, label='Random')

plt.fill_between(x, avg_explored_g - g_error, avg_explored_g + g_error, color=GREEDY_COLOR, alpha=0.3)
plt.fill_between(x, avg_explored_g2 - g2_error, avg_explored_g2 + g2_error, color=GREEDY2_COLOR, alpha=0.3)
plt.fill_between(x, avg_explored_o - o_error, avg_explored_o + o_error, color=OPTIMAL_COLOR, alpha=0.3)
plt.fill_between(x, avg_explored_r - r_error, avg_explored_r + r_error, color=RANDOM_COLOR, alpha=0.3)

plt.xlim(0, 30)
plt.ylim(0, 6)
plt.legend(loc="lower right")
plt.show()
