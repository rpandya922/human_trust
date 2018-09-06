from __future__ import division 
import numpy as np
import matplotlib.pyplot as plt
import ast
import csv
from parse_utils import *

objective_measures = False
subjective_measures = False
answers = False
entropy_plots = True
# experiment_type = "stats"
experiment_type = "observe"
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

training_scores = [[], []]
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
all_robot_maxes = [[],[],[],[]]
robot_answers = [[],[],[],[]]

# users who did best with greedy (kinda)
exploratory_users_initial = [0,1,2,4,5,6,8,9,10,13,14,17,21,22,23,24,25,26,27,28,29,32,34,35,37,39,41,43,44,45,46,48,50,51]
# users who did best with ucb2 (kinda)
greedy_users_initial = [3,7,11,12,15,16,18,19,20,30,31,33,36,38,40,42,47,49]
# misclassified: [2, 7, 13, 16]
exploratory_users = [0,1,2,4,5,6,8,9,10,11,13,14,17,19,21,22,23,24,25,26,27,28,29,32,34,35,37,38,39,41,43,44,45,46,47,48,50,51]
greedy_users = [3,7,12,15,16,18,20,30,31,33,36,40,42,49]

user_idx = 0
fig, ax = plt.subplots()
best_robot_explore = []
best_robot_greedy = []
all_greedy_user_traj = []
all_exploratory_user_traj = []

group1_ha_ucb = []
group1_ha_ucb_robot = []
group1_greedy = []
group1_greedy_robot = []
group1_ucb = []
group1_random = []
# fig2, ax2 = plt.subplots()
for k in user_data.keys():
    if k in to_ignore:
        continue
    if k == 'A5NHP0N1XC09K:3TS1AR6UQR9BAHNBZANTRDU5WLW7FQ':
        # user said they didn't understand the task and it hurt their hands 
        continue

    if experiment_type == "observe":
        if set(observe_keys) <= set(user_data[k].keys()):
            # observe and collaborate condition
            condition = 0
        else:
            # collaborate only condition
            condition = 1
    elif experiment_type == "stats":
        condition = int(user_data[k]['condition'])

    user_data[k]['training'] = ast.literal_eval(user_data[k]['training'])
    training_score = user_data[k]['training']['total_reward']
    training_scores[condition].append(training_score)

    training_decisions = user_data[k]['training']['human_decisions']
    training_entropy.append(policy_entropy(training_decisions, num_arms))

    # print training_decisions
    # print get_exploratory_actions(training_decisions, user_data[k]['training']['average_rewards'])

    # print user_idx
    # fig, ax = plt.subplots()
    # if user_idx in greedy_users:
    #     ents = entropy_over_time(training_decisions, num_arms)
    #     ax.plot(np.arange(len(ents)), ents, c='C0', alpha=0.7)
    #     plt.pause(0.01)
    # if user_idx in exploratory_users:
    #     ents = entropy_over_time(training_decisions, num_arms)
    #     ax.plot(np.arange(len(ents)), ents, c='C1', alpha=0.7)
    #     plt.pause(0.01)
    # raw_input()
    # plt.close(fig)

    all_robot_scores = []
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

        # ax2.scatter(initial_agreement, total_reward, color='C0')
        
        # if robot == 'optimal2_hard_collaborate_suggest':
        #     fig, ax = plt.subplots()
        #     human_ents = entropy_over_time(user_data[k][robot]['human_decisions'], num_arms)
        #     ents = entropy_over_time(user_data[k][robot]['robot_decisions'], num_arms)
        #     ax.plot(np.arange(len(ents)), ents)
        #     ax.plot(np.arange(len(ents)), human_ents)
        #     plt.pause(0.01)
        #     raw_input()
        #     plt.close(fig)
############################################################################################################################################
# ENTROPY CURVES CODE
        # if robot == "random_hard_collaborate_suggest" and user_idx in exploratory_users:
        #     all_exploratory_user_traj.append(entropy_over_time(user_data[k][robot]['human_decisions'], num_arms))
        # elif robot == "random_hard_collaborate_suggest" and user_idx in greedy_users:
        #     all_greedy_user_traj.append(entropy_over_time(user_data[k][robot]['human_decisions'], num_arms))

        # if robot == "optimal2_hard_collaborate_suggest" and user_idx in exploratory_users:
        #     all_exploratory_user_traj.append(entropy_over_time(user_data[k][robot]['human_decisions'], num_arms))
        #     all_greedy_user_traj.append(entropy_over_time(user_data[k][robot]['robot_decisions'], num_arms))

        if robot == "optimal2_hard_collaborate_suggest" and user_idx in greedy_users:
            group1_ha_ucb.append(entropy_over_time(user_data[k][robot]['human_decisions'], num_arms))
            group1_ha_ucb_robot.append(entropy_over_time_robot(user_data[k][robot]['human_decisions'], 
                user_data[k][robot]['robot_decisions'], num_arms))
        elif robot == "greedy_hard_collaborate_suggest" and user_idx in greedy_users:
            group1_greedy.append(entropy_over_time(user_data[k][robot]['human_decisions'], num_arms))
            group1_greedy_robot.append(entropy_over_time_robot(user_data[k][robot]['human_decisions'], 
                user_data[k][robot]['robot_decisions'], num_arms))
        elif robot == "optimal_hard_collaborate_suggest" and user_idx in greedy_users:
            group1_ucb.append(entropy_over_time(user_data[k][robot]['human_decisions'], num_arms))
        elif robot == "random_hard_collaborate_suggest" and user_idx in greedy_users:
            group1_random.append(entropy_over_time(user_data[k][robot]['human_decisions'], num_arms))

        all_robot_scores.append(total_reward)
    all_robot_maxes[np.argmax(all_robot_scores)].append(np.amax(all_robot_scores))
    if user_idx in exploratory_users:
        best_robot_explore.append(np.argmax(all_robot_scores))
        all_exploratory_user_traj.append(entropy_over_time(training_decisions, num_arms))
    elif user_idx in greedy_users:
        best_robot_greedy.append(np.argmax(all_robot_scores))
        all_greedy_user_traj.append(entropy_over_time(training_decisions, num_arms))
    
    # instead split based on which robot they performed best with
    # if np.argmax(all_robot_scores) == 2 :
    #     all_exploratory_user_traj.append(entropy_over_time(training_decisions, num_arms))
    # elif np.argmax(all_robot_scores) == 1:
    #     all_greedy_user_traj.append(entropy_over_time(training_decisions, num_arms))

    # robot_answers[np.argmax(all_robot_scores)].append(user_data[k][collab_keys[np.argmax(all_robot_scores)]]['answer'])
    robot_answers[np.argmax(all_robot_scores)].append(percent_agreement_initial(user_data[k][collab_keys[np.argmax(all_robot_scores)]]\
        ['before_suggest_decisions'], user_data[k][collab_keys[np.argmax(all_robot_scores)]]['robot_decisions']))
    user_idx += 1
# plt.show()
if entropy_plots:
    ## humans in isolation
    all_greedy_user_scores = np.array(all_greedy_user_traj)
    all_exploratory_user_scores = np.array(all_exploratory_user_traj)

    all_greedy_user_traj = np.array(all_greedy_user_traj)
    std_errors_greedy = [np.std(all_greedy_user_traj[:,i]) / np.sqrt(len(all_greedy_user_traj)) for i in range(30)]
    avg_greedy_traj = np.average(all_greedy_user_traj, axis=0)

    all_exploratory_user_traj = np.array(all_exploratory_user_traj)
    std_errors_exploratory = [np.std(all_exploratory_user_traj[:,i]) / np.sqrt(len(all_exploratory_user_traj)) for i in range(30)]
    avg_exploratory_traj = np.average(all_exploratory_user_traj, axis=0)

    plt.plot(np.arange(30), avg_greedy_traj, label="Group 1", color='#5b9bd5', linewidth=3)
    ax.fill_between(np.arange(30), avg_greedy_traj - std_errors_greedy, avg_greedy_traj + std_errors_greedy, alpha=0.3, color='#5b9bd5')

    plt.plot(np.arange(30), avg_exploratory_traj, label="Group 2", color='#ed7d31', linewidth=3)
    ax.fill_between(np.arange(30), avg_exploratory_traj - std_errors_exploratory, avg_exploratory_traj + std_errors_exploratory, alpha=0.3, color='#ed7d31')
    
    ax.plot(np.arange(30), np.ones(30)*2.5849, linestyle='--', color='k', label='Maximum Entropy', linewidth=3)
    ax.set_xlim(0, 29)
    ax.set_xlabel("Number of Pulls")
    ax.set_ylabel("Entropy of Arm Pulls")
    ax.legend()

    ## with robots
    fig, ax = plt.subplots()

    group1_ha_ucb = np.array(group1_ha_ucb)
    std_errors_group1_ha_ucb = [np.std(group1_ha_ucb[:,i]) / np.sqrt(len(group1_ha_ucb)) for i in range(30)]
    avg_group1_ha_ucb = np.average(group1_ha_ucb, axis=0)

    group1_ha_ucb_robot = np.array(group1_ha_ucb_robot)
    std_errors_group1_ha_ucb_robot = [np.std(group1_ha_ucb_robot[:,i]) / np.sqrt(len(group1_ha_ucb_robot)) for i in range(30)]
    avg_group1_ha_ucb_robot = np.average(group1_ha_ucb_robot, axis=0)

    group1_greedy = np.array(group1_greedy)
    std_errors_group1_greedy = [np.std(group1_greedy[:,i]) / np.sqrt(len(group1_greedy)) for i in range(30)]
    avg_group1_greedy = np.average(group1_greedy, axis=0)

    group1_greedy_robot = np.array(group1_greedy_robot)
    std_errors_group1_greedy_robot = [np.std(group1_greedy_robot[:,i]) / np.sqrt(len(group1_greedy_robot)) for i in range(30)]
    avg_group1_greedy_robot = np.average(group1_greedy_robot, axis=0)

    group1_ucb = np.array(group1_ucb)
    std_errors_group1_ucb = [np.std(group1_ucb[:,i]) / np.sqrt(len(group1_ucb)) for i in range(30)]
    avg_group1_ucb = np.average(group1_ucb, axis=0)

    group1_random = np.array(group1_random)
    std_errors_group1_random = [np.std(group1_random[:,i]) / np.sqrt(len(group1_random)) for i in range(30)]
    avg_group1_random = np.average(group1_random, axis=0)

    plt.plot(np.arange(30), avg_greedy_traj, label="Training", color='#a5a5a5', linewidth=3)
    ax.fill_between(np.arange(30), avg_greedy_traj - std_errors_greedy, avg_greedy_traj + std_errors_greedy, alpha=0.3, color='#a5a5a5')
    # plt.plot(np.arange(30), avg_exploratory_traj, label="Training", color='#a5a5a5', linewidth=3)
    # ax.fill_between(np.arange(30), avg_exploratory_traj - std_errors_exploratory, avg_exploratory_traj + std_errors_exploratory, alpha=0.3, color='#a5a5a5')

    plt.plot(np.arange(30), avg_group1_ha_ucb, label="HA-UCB", color='#4472c4', linewidth=3)
    ax.fill_between(np.arange(30), avg_group1_ha_ucb - std_errors_group1_ha_ucb, 
        avg_group1_ha_ucb + std_errors_group1_ha_ucb, alpha=0.3, color='#4472c4')

    # plt.plot(np.arange(30), avg_group1_ha_ucb_robot, label="HA-UCB Agent", color='C0', linewidth=3, linestyle='--')
    # ax.fill_between(np.arange(30), avg_group1_ha_ucb_robot - std_errors_group1_ha_ucb_robot, 
    #     avg_group1_ha_ucb_robot + std_errors_group1_ha_ucb_robot, alpha=0.3, color='C0')

    plt.plot(np.arange(30), avg_group1_greedy, label="0.1-Greedy", color='#ffc000', linewidth=3)
    ax.fill_between(np.arange(30), avg_group1_greedy - std_errors_group1_greedy, 
        avg_group1_greedy + std_errors_group1_greedy, alpha=0.3, color='#ffc000')

    # plt.plot(np.arange(30), avg_group1_greedy_robot, label="0.1-Greedy Agent", color='C1', linewidth=3, linestyle='--')
    # ax.fill_between(np.arange(30), avg_group1_greedy_robot - std_errors_group1_greedy_robot, 
    #     avg_group1_greedy_robot + std_errors_group1_greedy_robot, alpha=0.3, color='C1')

    # plt.plot(np.arange(30), avg_group1_ucb, label="UCB", color='C2', linewidth=3)
    # ax.fill_between(np.arange(30), avg_group1_ucb - std_errors_group1_ucb, 
    #     avg_group1_ucb + std_errors_group1_ucb, alpha=0.3, color='C2')

    # plt.plot(np.arange(30), avg_group1_random, label="0.9-Greedy", color='C3', linewidth=3)
    # ax.fill_between(np.arange(30), avg_group1_random - std_errors_group1_random, 
    #     avg_group1_random + std_errors_group1_random, alpha=0.3, color='C3')
    
    ax.plot(np.arange(30), np.ones(30)*2.5849, linestyle='--', color='k', label='Maximum Entropy', linewidth=3)
    ax.set_xlim(0, 29)
    ax.set_xlabel("Number of Pulls")
    ax.set_ylabel("Entropy of Arm Pulls")
    ax.legend()

    plt.show()

    percents_greedy = np.zeros(4)
    for robot in best_robot_greedy:
        percents_greedy[robot] += 1
    percents_greedy = percents_greedy / len(greedy_users)

    percents_exploratory = np.zeros(4)
    for robot in best_robot_explore:
        percents_exploratory[robot] += 1
    percents_exploratory = percents_exploratory / len(exploratory_users)

    print "Greedy: " + str(percents_greedy)
    print "Exploratory: " + str(percents_exploratory)

    print len(all_robot_maxes[0]), np.average(all_robot_maxes[0])
    print np.average(robot_answers[0])
    print len(all_robot_maxes[1]), np.average(all_robot_maxes[1])
    print np.average(robot_answers[1])
    print len(all_robot_maxes[2]), np.average(all_robot_maxes[2])
    print np.average(robot_answers[2])
    print len(all_robot_maxes[3]), np.average(all_robot_maxes[3])
    print np.average(robot_answers[3])
############################################################################################################################################
if objective_measures:
    print robot_order
    print
    print np.average(training_scores[0])
    print np.average(training_scores[1])
    print
    print np.average(training_entropy)
    print 
    print np.average(robot_collab_scores[0], axis=1)
    print np.average(robot_collab_scores[1], axis=1)
    print [np.std(x) / np.sqrt(len(x)) for x in robot_collab_scores[0]]
    print [np.std(x) / np.sqrt(len(x)) for x in robot_collab_scores[1]]
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
        if k == 'A5NHP0N1XC09K:3TS1AR6UQR9BAHNBZANTRDU5WLW7FQ':
            # user said they didn't understand the task and it hurt their hands 
            continue

        if experiment_type == "observe":
            if set(observe_keys) <= set(user_data[k].keys()):
                # observe and collaborate condition
                condition = 0
            else:
                # collaborate only condition
                condition = 1
        elif experiment_type == "stats":
            condition = int(user_data[k]['condition'])

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
    print [np.std(x) / np.sqrt(len(x))for x in robot_usefulness[0]]
    print [np.std(x) / np.sqrt(len(x))for x in robot_usefulness[1]]
    print
    print "'I followed the robot's advice'"
    print np.average(robot_advice[0], axis=1)
    print np.average(robot_advice[1], axis=1)
    print [np.std(x) / np.sqrt(len(x))for x in robot_advice[0]]
    print [np.std(x) / np.sqrt(len(x))for x in robot_advice[1]]
    print
    print "'I trusted the robot'"
    print np.average(robot_trust[0], axis=1)
    print np.average(robot_trust[1], axis=1)
    print [np.std(x) / np.sqrt(len(x))for x in robot_trust[0]]
    print [np.std(x) / np.sqrt(len(x))for x in robot_trust[1]]
    print
    print "Rankings"
    print np.average(robot_ranks[0], axis=1)
    print np.average(robot_ranks[1], axis=1)
if answers:
    robot = collab_keys[0]
    for c in [0, 1]:
        print "Condition " + str(c)
        for k in user_data.keys():
            if k in to_ignore:
                continue
            if experiment_type == "observe":
                if set(observe_keys) <= set(user_data[k].keys()):
                    # observe and collaborate condition
                    condition = 0
                else:
                    # collaborate only condition
                    condition = 1
            elif experiment_type == "stats":
                condition = int(user_data[k]['condition'])

            if c == condition:
                print user_data[k][robot]['answer']
