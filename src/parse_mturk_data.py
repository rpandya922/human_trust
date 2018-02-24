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
def print_average_rewards():
    # Observe and collaborate condition variables
    # condition number: 0
    greedy_rewards0 = []
    greedy2_rewards0 = []
    optimal_rewards0 = []
    random_rewards0 = []
    # Collaborate condition variables
    # condition number: 1
    greedy_rewards1 = []
    greedy2_rewards1 = []
    optimal_rewards1 = []
    random_rewards1 = []

    for k in user_data.keys():
        user_dict = user_data[k]
        if 'greedy_medium_observe' in user_dict.keys():
            # observe and collaborate condition
            try:
                greedy_collab = ast.literal_eval(user_dict[collab_keys[3]])
                greedy2_collab = ast.literal_eval(user_dict[collab_keys[2]])
                optimal_collab = ast.literal_eval(user_dict[collab_keys[4]])
                random_collab = ast.literal_eval(user_dict[collab_keys[1]])
            except:
                continue
            greedy_rewards0.append(int(greedy_collab['total_reward']))
            greedy2_rewards0.append(int(greedy2_collab['total_reward']))
            optimal_rewards0.append(int(optimal_collab['total_reward']))
            random_rewards0.append(int(random_collab['total_reward']))
        else:
            # collaborate conndition
            try:
                greedy_collab = ast.literal_eval(user_dict[collab_keys[3]])
                greedy2_collab = ast.literal_eval(user_dict[collab_keys[2]])
                optimal_collab = ast.literal_eval(user_dict[collab_keys[4]])
                random_collab = ast.literal_eval(user_dict[collab_keys[1]])
            except:
                continue
            greedy_rewards1.append(int(greedy_collab['total_reward']))
            greedy2_rewards1.append(int(greedy2_collab['total_reward']))
            optimal_rewards1.append(int(optimal_collab['total_reward']))
            random_rewards1.append(int(random_collab['total_reward']))

    print "#####################################"
    print "Collaborate"
    print "Greedy 0.1: " + str(np.average(greedy_rewards1))
    print "Greedy 0.3: " + str(np.average(greedy2_rewards1))
    print "Optimal: " + str(np.average(optimal_rewards1))
    print "Random: " + str(np.average(random_rewards1))
    print "#####################################"
    print
    print "#####################################"
    print "Observe and Collaborate"
    print "Greedy 0.1: " + str(np.average(greedy_rewards0))
    print "Greedy 0.3: " + str(np.average(greedy2_rewards0))
    print "Optimal: " + str(np.average(optimal_rewards0))
    print "Random: " + str(np.average(random_rewards0))
    print "#####################################"
    print
def print_average_times():
    # Observe and Collaborate vars
    # condition number: 0
    time_taken0_robot0 = []
    time_taken0_robot1 = []
    time_taken0_robot2 = []
    time_taken0_robot3 = []
    # Collaborate vars
    # condition number: 1
    time_taken1_robot0 = []
    time_taken1_robot1 = []
    time_taken1_robot2 = []
    time_taken1_robot3 = []

    for k in user_data.keys():
            user_dict = user_data[k]
            if 'greedy_medium_observe' in user_dict.keys():
                # observe and collaborate condition
                try:
                    robot_order = ast.literal_eval(user_dict['robot_colors'])
                    time_taken0_robot0.append(int(user_dict['time_taken_' + robot_order[0]]) / 1000 / 60)
                    time_taken0_robot1.append(int(user_dict['time_taken_' + robot_order[1]]) / 1000 / 60)
                    time_taken0_robot2.append(int(user_dict['time_taken_' + robot_order[2]]) / 1000 / 60)
                    time_taken0_robot3.append(int(user_dict['time_taken_' + robot_order[3]]) / 1000 / 60)
                except:
                    continue
            else:
                # collaborate condition
                try:
                    robot_order = ast.literal_eval(user_dict['robot_colors'])
                    time_taken1_robot0.append(int(user_dict['time_taken_' + robot_order[0]]) / 1000 / 60)
                    time_taken1_robot1.append(int(user_dict['time_taken_' + robot_order[1]]) / 1000 / 60)
                    time_taken1_robot2.append(int(user_dict['time_taken_' + robot_order[2]]) / 1000 / 60)
                    time_taken1_robot3.append(int(user_dict['time_taken_' + robot_order[3]]) / 1000 / 60)
                except:
                    continue

    print "Average Time Taken per Robot (minutes)"
    print "#####################################"
    print "Collaborate"
    print "Robot 0: " + str(np.average(time_taken1_robot0))
    print "Robot 1: " + str(np.average(time_taken1_robot1))
    print "Robot 2: " + str(np.average(time_taken1_robot2))
    print "Robot 3: " + str(np.average(time_taken1_robot3))
    print "#####################################"
    print
    print "#####################################"
    print "Observe and Collaborate"
    print "Robot 0: " + str(np.average(time_taken0_robot0))
    print "Robot 1: " + str(np.average(time_taken0_robot1))
    print "Robot 2: " + str(np.average(time_taken0_robot2))
    print "Robot 3: " + str(np.average(time_taken0_robot3))
    print "#####################################"
    print
def print_mind_change():
    # Observe and Collaborate vars
    # condition number: 0
    change0 = []
    change_to_robot0 = []
    # Collaborate vars
    # condition number: 1
    change1 = []
    change_to_robot1 = []
    for key in collab_keys:
        change0.append([])
        change1.append([])
        change_to_robot0.append([])
        change_to_robot1.append([])
        for k in user_data.keys():
            user_dict = user_data[k]
            try:
                collab_dict = ast.literal_eval(user_dict[key])
            except:
                continue
            human_decisions = collab_dict['human_decisions']
            robot_decisions = collab_dict['robot_decisions']
            before_suggest_decisions = collab_dict['before_suggest_decisions']
            change_percent, change_to_robot_percent = change_mind(before_suggest_decisions, human_decisions, robot_decisions)
            if set(observe_keys) <= set(user_dict.keys()):
                # observe and collaborate condition
                change0[-1].append(change_percent)
                if change_to_robot_percent is not None:
                    change_to_robot0[-1].append(change_to_robot_percent)
            elif set(collab_keys) <= set(user_dict.keys()):
                # collaborate_condition
                change1[-1].append(change_percent)
                if change_to_robot_percent is not None:
                    change_to_robot1[-1].append(change_to_robot_percent)

    print "% Change"
    print "#####################################"
    print "Collaborate"
    for i, key in enumerate(collab_keys):
        avg = np.average(change0[i])
        print key + ": " + str(avg)
    print "#####################################"
    print
    print "#####################################"
    print "Observe and Collaborate"
    for i, key in enumerate(collab_keys):
        avg = np.average(change1[i])
        print key + ": " + str(avg)
    print "#####################################"
    print
    print "% Change To Robot"
    print "#####################################"
    print "Collaborate"
    for i, key in enumerate(collab_keys):
        avg = np.average(change_to_robot0[i])
        print key + ": " + str(avg)
    print "#####################################"
    print
    print "#####################################"
    print "Observe and Collaborate"
    for i, key in enumerate(collab_keys):
        avg = np.average(change_to_robot1[i])
        print key + ": " + str(avg)
    print "#####################################"
    print
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
csv_headers = ['user id', 'condition', 'robot', 'difficulty', 'trust', 'usefulness', 'advice', 'total_reward', 'percent agreement', 
              'percent mind changed', 'percent mind channged to robot']
csv_dataset = []
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
        total_reward = collab_dict['total_reward']
        agreement = percent_agreement(collab_dict['human_decisions'], collab_dict['robot_decisions'])
        percent_mind_changed, percent_mind_changed_to_robot = change_mind(collab_dict['before_suggest_decisions'], collab_dict['human_decisions'], collab_dict['robot_decisions'])
        csv_dataset.append([user, condition, robot, difficulty, trust, usefulness, advice, total_reward, agreement, percent_mind_changed, percent_mind_changed_to_robot])
## writing data to csv
with open('../data/mturk_full_dataset.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    headers = [csv_headers]
    for i in range(len(csv_dataset)):
        headers.append(csv_dataset[i])
    wr.writerows(headers)


