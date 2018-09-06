from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import csv
import ast
from parse_utils import *

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
robot_names = ['0.9-Greedy', 'HA-UCB', '0.1-Greedy', 'UCB']

to_ignore = set()
for k, v in user_data.iteritems():
    for c in collab_keys:
        if c not in v.keys():
            to_ignore.add(k)

# group 2
exploratory_users = [0,1,2,4,5,6,8,9,10,11,13,14,17,19,21,22,23,24,25,26,27,28,29,32,34,35,37,38,39,41,43,44,45,46,47,48,50,51]
# group 1
greedy_users = [3,7,12,15,16,18,20,30,31,33,36,40,42,49]

csv_headers = ['user id', 'robot', 'manual condition', 'total influence', 'time until suggest taken']
csv_dataset = []

influence_headers = ['user id', 'condition', 'robot', 'delay']
influence_dataset = []

user_idx = 0
robot_influence_scores = [[] for _ in range(len(collab_keys))]
robot_compatability_scores = [[] for _ in range(len(collab_keys))]
robot_explicit_influence = [[] for _ in range(len(collab_keys))]
time_until_accepted = [[] for _ in range(len(collab_keys))]
ages = []
num_female = 0
for k in user_data.keys():
    if k in to_ignore:
        continue
    if k == 'A5NHP0N1XC09K:3TS1AR6UQR9BAHNBZANTRDU5WLW7FQ':
        # user said they didn't understand the task and it hurt their hands 
        continue
    ages.append(int(user_data[k]['age']))
    if user_data[k]['gender'] == "female":
        num_female += 1

    if user_idx in greedy_users:
        manual_condition = "greedy"
    elif user_idx in exploratory_users:
        manual_condition = "exploratory"

    user_data[k]['training'] = ast.literal_eval(user_data[k]['training'])
    training_decisions = user_data[k]['training']['human_decisions']
    all_training_rewards = user_data[k]['training']['average_rewards']

    for i, robot in enumerate(collab_keys):
        user_data[k][robot] = ast.literal_eval(user_data[k][robot])
        human_decisions = user_data[k][robot]['human_decisions']
        human_initial_decisions = user_data[k][robot]['before_suggest_decisions']
        robot_decisions = user_data[k][robot]['robot_decisions']
        # human_decisions = [h - 1 for h in human_decisions]
        all_avg_rewards = user_data[k][robot]['average_rewards']

        exp_influence = explicit_influence(human_initial_decisions, human_decisions, robot_decisions, num_arms)
        imp_influence = implicit_influence_scores(human_decisions, all_avg_rewards, num_arms)

        # robot_influence_scores[i].append(imp_influence)
        robot_explicit_influence[i].append(exp_influence)
        robot_compatability_scores[i].append(simulation_agreement(training_decisions, all_training_rewards, num_arms, robot_names[i]))
        
        human_initial_decisions = user_data[k][robot]['before_suggest_decisions']
        human_initial_decisions = [h - 1 for h in human_initial_decisions]
        time = times_until_pulled(human_initial_decisions, robot_decisions)
        time_until_accepted[i].append(time)
        robot_influence_scores[i].append(implicit_influence_scores(human_initial_decisions, all_avg_rewards, num_arms))

        csv_dataset.append([k, robot_names[i], manual_condition, exp_influence, np.average(time)])

        robot_name = robot_names[i]
        for delay in time:
            influence_dataset.append([k, 'assisted', robot_name, delay])
    user_idx += 1

## writing data to csv
# with open('../data/aaai_submission/new_influence.csv', 'wb') as f:
#     wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
#     headers = [csv_headers]
#     for i in range(len(csv_dataset)):
#         headers.append(csv_dataset[i])
#     wr.writerows(headers)

for i in range(4):
    name = robot_names[i]
    times = np.array(time_until_accepted[i]).flatten()
    error = np.std(times) / np.sqrt(len(times))
    print name, np.average(times), error
print 

print "Explicit influence"
for i in range(4):
    name = robot_names[i]
    influences = np.array(robot_explicit_influence[i]) / 30
    error = np.std(influences) / np.sqrt(len(influences))
    print name, np.average(influences), error
print

fig, ax = plt.subplots()
colors = ["#262626", "#4472c4", "#ffc000", "#70ad47"]
names = ["0.9-Greedy", "HA-UCB", "0.1-Greedy", "UCB"]
for i in [1, 3]:
    ha_ucb_scores = robot_influence_scores[i]

    ha_ucb_scores = np.array(ha_ucb_scores)
    std_errors_ha_ucb = [np.std(ha_ucb_scores[:,j]) / np.sqrt(len(ha_ucb_scores)) for j in range(30)]
    avg_ha_ucb = np.average(ha_ucb_scores, axis=0)

    ax.plot(np.arange(30), avg_ha_ucb, label=names[i], color=colors[i], linewidth=3)
    ax.fill_between(np.arange(30), avg_ha_ucb - std_errors_ha_ucb,
        avg_ha_ucb + std_errors_ha_ucb, alpha=0.3, color=colors[i])

user_data = {}
with open('../data/mturk_humans_9_4_18/questiondata.csv', 'rb') as csvfile:
    for row in csv.reader(csvfile):
        user_data[row[0]] = {}
with open('../data/mturk_humans_9_4_18/questiondata.csv', 'rb') as csvfile:
    for row in csv.reader(csvfile):
        user_data[row[0]][row[1]] = row[2]

keys = ["training", "testing"]
to_ignore = set()
for k, v in user_data.iteritems():
    for c in keys:
        if c not in v.keys():
            to_ignore.add(k)

regrets = []
human_alone_scores = []
time_until_accepted_sim = [[] for _ in range(len(collab_keys))]
for k in user_data.keys():
    if k in to_ignore:
        continue

    user_data[k]['testing'] = ast.literal_eval(user_data[k]['testing'])
    user_data[k]['training'] = ast.literal_eval(user_data[k]['training'])
    training_decisions = user_data[k]['testing']['human_decisions']
    all_avg_rewards = user_data[k]['testing']['average_rewards']

    regrets.append(30*2.9 - user_data[k]['training']['total_reward'])

    human_alone_scores.append(implicit_influence_scores(training_decisions, all_avg_rewards, num_arms))

    for i in range(4):
        robot_compatability_scores[i].append(simulation_agreement(training_decisions, all_avg_rewards, num_arms, robot_names[i]))
        imp_influence = simulated_suggestion_acceptance(training_decisions, all_avg_rewards, num_arms, robot_names[i])
        time_until_accepted_sim[i].append(imp_influence)

        robot_name = robot_names[i]
        for delay in imp_influence:
            influence_dataset.append([k, 'unassisted', robot_name, delay])

print "TIME UNTIL ACCEPTED SIM"
for i in range(4):
    name = robot_names[i]
    times = np.array(time_until_accepted_sim[i]).flatten()
    error = np.std(times) / np.sqrt(len(times))
    print name, np.average(times), error
print

# writing data to csv
with open('../data/aaai_submission/implicit_influence.csv', 'wb') as f:
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    headers = [influence_headers]
    for i in range(len(influence_dataset)):
        headers.append(influence_dataset[i])
    wr.writerows(headers)

print "Regret: " + str(np.average(regrets)) + " " + str(np.std(regrets) / np.sqrt(len(regrets)))
print np.array(robot_compatability_scores).shape
print robot_names[0], np.average(robot_compatability_scores[0])
print robot_names[1], np.average(robot_compatability_scores[1])
print robot_names[2], np.average(robot_compatability_scores[2])
print robot_names[3], np.average(robot_compatability_scores[3])

ha_ucb_scores = human_alone_scores
ha_ucb_scores = np.array(ha_ucb_scores)
std_errors_ha_ucb = [np.std(ha_ucb_scores[:,j]) / np.sqrt(len(ha_ucb_scores)) for j in range(30)]
avg_ha_ucb = np.average(ha_ucb_scores, axis=0)

# ax.plot(np.arange(30), avg_ha_ucb, label="Human Alone", color="grey", linewidth=3)
# ax.fill_between(np.arange(30), avg_ha_ucb - std_errors_ha_ucb,
#     avg_ha_ucb + std_errors_ha_ucb, alpha=0.3, color="grey")

ax.legend()
ax.set_xlim(0, 29)
ax.set_ylim(0, 1)
plt.show()
