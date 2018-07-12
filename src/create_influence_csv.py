from __future__ import division
import numpy as np
import csv
import ast

def percent_agreement(human_decisions, robot_decisions):
    times_agree = 0
    interaction_length = 0
    for i, human_decision in enumerate(human_decisions):
        robot_decision = robot_decisions[i]
        if len(robot_decision) > 1:
            # robot wanted to explore randomly
            # ignore this choice, robot essentially withheld a suggestion
            continue
        else:
            if human_decision == robot_decision[0]:
                times_agree += 1
            interaction_length += 1
    return times_agree / interaction_length
def percent_agreement_initial(human_decisions, robot_decisions):
    times_agree = 0
    interaction_length = 0
    for i, human_decision in enumerate(human_decisions):
        robot_decision = robot_decisions[i]
        if len(robot_decision) > 1:
            # robot wanted to explore randomly
            # ignore this choice, robot essentially withheld a suggestion
            continue
        else:
            # arm numbers are off by one from arm indices
            if (human_decision - 1) == robot_decision[0]:
                times_agree += 1
            interaction_length += 1
    return times_agree / interaction_length
def change_mind_to_robot(before_suggest_decisions, human_decisions, robot_decisions):
    interaction_length = 0
    times_changed_to_robot = 0
    times_changed_against_robot = 0
    times_disagree = 0
    for i, human_decision in enumerate(human_decisions):
        before_suggest_decision = before_suggest_decisions[i] - 1
        robot_decision = robot_decisions[i]
        if len(robot_decision) > 1:
            # ignore multiple suggestions
            continue
        interaction_length += 1
        if before_suggest_decision != robot_decision[0]:
            # initially disagree
            times_disagree += 1
            if human_decision == robot_decision[0]:
                # changed mind to agree with robot
                times_changed_to_robot += 1
        else:
            # initially agree
            if human_decision != robot_decision[0]:
                # changed mind to disagree with robot
                times_changed_against_robot += 1
    if times_disagree == 0:
        return None, times_changed_against_robot / interaction_length
    return times_changed_to_robot / times_disagree, times_changed_against_robot / interaction_length
def change_mind(before_suggest_decisions, human_decisions, robot_decisions, arm_payoffs=None, arm_probabilities=None):
    # expected_arm_rewards = np.multiply(arm_probabilities, arm_payoffs)
    same_decision = 0
    interaction_length = 0
    changed_to_robot = 0
    changed_mind = 0
    for i, human_decision in enumerate(human_decisions):
        # arm numbers start at 1, indices at 0
        before_suggest_decision = before_suggest_decisions[i] - 1
        robot_decision = robot_decisions[i]
        if human_decision == before_suggest_decision:
            same_decision += 1
        else:
            if len(robot_decision) > 1:
                pass
            else:
                if human_decision == robot_decision[0]:
                    changed_to_robot += 1
                changed_mind += 1
        interaction_length += 1
    if changed_mind == 0:
        return 1 - (same_decision / interaction_length), None
    return 1 - (same_decision / interaction_length), (changed_to_robot / changed_mind)
def time_until_all_explored(human_decisions, arm_payoffs):
    num_arms = len(arm_payoffs)
    explored = set()
    for i in range(30):
        explored.add(human_decisions[i])
        if set(range(num_arms)) <= explored:
            return i
    return 30
def find_epsilon(before_suggest_decisions, average_rewards):
    times_suboptimal = 0
    for i, avgs in enumerate(average_rewards):
        human_decision = before_suggest_decisions[i] - 1
        if human_decision != np.argmax(avgs):
            times_suboptimal += 1
    return times_suboptimal / 30
def total_reward_in_expectation(human_decisions, arm_payoffs, arm_probabilities):
    expected_rewards = np.multiply(arm_probabilities, arm_payoffs)
    total_reward = 0
    for i in human_decisions:
        total_reward += expected_rewards[i]
    return total_reward
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
csv_headers = ['user id', 'condition', 'robot', 'difficulty', 'initial_agreement', 'robot_influence']
csv_dataset = []
agree0 = []
agree1 = []

## observe and collab
time_until_explored0_greedy = []
time_until_explored0_optimal = []
## collab
time_until_explored1_greedy = []
time_until_explored1_optimal = []

## observe and collab
total_expected_reward0_greedy = []
total_expected_reward0_optimal = []
# collab
total_expected_reward1_greedy = []
total_expected_reward1_optimal = []

## observe and collab
training_reward0 = []
## collab
training_reward1 = []

## observe and colab
total_rewards0 = []
## collab
total_rewards1 = []

avg_epsilon = []

avg_percent_agreement = []

g = []
g2 = []
o = []
r = []

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
            continue

        initial_agreement = percent_agreement_initial(collab_dict['before_suggest_decisions'], collab_dict['robot_decisions'])
        change_to_agree, _ = change_mind_to_robot(collab_dict['before_suggest_decisions'], collab_dict['human_decisions'], collab_dict['robot_decisions'])
        if change_to_agree is None:
            continue

        rank = None
        if 'robot_ranking' in user_dict.keys():
            if robot == 'greedy':
                rank = ast.literal_eval(user_dict['robot_ranking'])[0]
                g.append(rank)
            elif robot == 'greedy2':
                rank = ast.literal_eval(user_dict['robot_ranking'])[1]
                g2.append(rank)
            elif robot == 'optimal':
                rank = ast.literal_eval(user_dict['robot_ranking'])[2]
                o.append(rank)
            elif robot == 'random':
                rank = ast.literal_eval(user_dict['robot_ranking'])[3]
                r.append(rank)
        # if rank is None:
        #     continue

        csv_dataset.append([user, condition, robot, difficulty, initial_agreement, change_to_agree])

## writing data to csv
with open('../data/mturk_influence_dataset.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    headers = [csv_headers]
    for i in range(len(csv_dataset)):
        headers.append(csv_dataset[i])
    wr.writerows(headers)


