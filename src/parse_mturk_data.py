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
              'percent mind changed', 'percent mind channged to robot', 'changed mind to robot total', 'percent initial agreement', 
              'rank', 'iterations_to_explore_all']
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

    ## person's training data
    training_dict = ast.literal_eval(user_dict['training'])
    if condition == 'observe and collaborate':
        training_reward0.append(training_dict['total_reward'])
    elif condition == 'collaborate':
        training_reward1.append(training_dict['total_reward'])

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
        initial_agreement = percent_agreement_initial(collab_dict['before_suggest_decisions'], collab_dict['robot_decisions'])
        percent_mind_changed, percent_mind_changed_to_robot = change_mind(collab_dict['before_suggest_decisions'], collab_dict['human_decisions'], collab_dict['robot_decisions'])
        change_to_agree, change_to_disagree = change_mind_to_robot(collab_dict['before_suggest_decisions'], collab_dict['human_decisions'], collab_dict['robot_decisions'])
        time_until_explored = time_until_all_explored(collab_dict['human_decisions'], collab_dict['arm_payoffs'])
        epsilon = find_epsilon(collab_dict['before_suggest_decisions'], collab_dict['average_rewards'])
        
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

        total_expected_reward = total_reward_in_expectation(collab_dict['human_decisions'], collab_dict['arm_payoffs'], collab_dict['arm_probabilities'])

        ## regular total rewards
        if difficulty == 'easy' and condition == 'observe and collaborate':
            total_rewards0.append(total_reward)
        elif difficulty == 'easy' and condition == 'collaborate':
            total_rewards1.append(total_reward)

        ## total rewards but taken in expectation
        if robot == 'greedy' and difficulty == 'hard' and condition == 'observe and collaborate':
            total_expected_reward0_greedy.append(total_expected_reward)
        elif robot == 'greedy' and difficulty == 'hard' and condition == 'collaborate':
            total_expected_reward1_greedy.append(total_expected_reward)
        elif robot == 'optimal' and difficulty == 'hard' and condition == 'observe and collaborate':
            total_expected_reward0_optimal.append(total_expected_reward)
        elif robot == 'optimal' and difficulty == 'hard' and condition == 'collaborate':
            total_expected_reward1_optimal.append(total_expected_reward)

        ## time taken to explore all arms
        if robot == 'greedy' and difficulty == 'hard' and condition == 'observe and collaborate':
            time_until_explored0_greedy.append(time_until_explored)
        elif robot == 'greedy' and difficulty == 'hard' and condition == 'collaborate':
            time_until_explored1_greedy.append(time_until_explored)
        elif robot == 'optimal' and difficulty == 'hard' and condition == 'observe and collaborate':
            time_until_explored0_optimal.append(time_until_explored)
        elif robot == 'optimal' and difficulty == 'hard' and condition == 'collaborate':
            time_until_explored1_optimal.append(time_until_explored)

        if percent_mind_changed_to_robot is None:
            total_mind_changed = 0
        else:
            total_mind_changed = percent_mind_changed * percent_mind_changed_to_robot
        
        if robot == 'greedy' and change_to_agree is not None:
            agree0.append(change_to_agree)
        elif robot == 'optimal' and change_to_agree is not None:
            agree1.append(change_to_agree)
        
        if robot == 'optimal' and difficulty == 'hard':
            avg_epsilon.append(epsilon)
            avg_percent_agreement.append(initial_agreement)

        csv_dataset.append([user, condition, robot, difficulty, trust, usefulness, advice, total_reward, agreement, percent_mind_changed, percent_mind_changed_to_robot, 
            total_mind_changed, initial_agreement, rank, time_until_explored])

## writing data to csv
with open('../data/mturk_full_dataset3.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    headers = [csv_headers]
    for i in range(len(csv_dataset)):
        headers.append(csv_dataset[i])
    wr.writerows(headers)


