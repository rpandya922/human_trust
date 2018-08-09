from __future__ import division
import numpy as np
import scipy.stats
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--ucb', action='store_true')
parser.add_argument('-u2', '--ucb2', action='store_true') # linear decaying exploration
parser.add_argument('--gittins', action='store_true')
parser.add_argument('-g', '--greedy', action='store_true')
parser.add_argument('-g2', '--greedy2', action='store_true')
parser.add_argument('-r', '--random', action='store_true')
parser.add_argument('-c', '--compare', action='store_true')
parser.add_argument('-t', '--times', type=int, default=1)
args = parser.parse_args()

num_arms = 6
time_horizon = 30

def all_argmax(arr):
    return np.argwhere(arr == np.amax(arr)).flatten()

# payoff_matrices = []
epsilons = []
robots = []
if args.ucb:
    epsilons.append(0)
    robots.append("ucb")
if args.ucb2: 
    epsilons.append(0)
    robots.append("ucb2")
if args.gittins:
    epsilons.append(0)
    robots.append("gittins")
if args.greedy:
    epsilons.append(0.1)
    robots.append("greedy")
if args.greedy2:
    epsilons.append(0.3)
    robots.append("greedy2")
if args.random:
    epsilons.append(0.9)
    robots.append("random")

payoff_matrix = np.array([[ 0.25      ,  0.5       ,  0.25      ,  0.        ,  0.        ],
                          [ 0.625     ,  0.        ,  0.25      ,  0.        ,  0.125     ],
                          [ 0.1875    ,  0.75      ,  0.        ,  0.        ,  0.0625    ],
                          [ 0.36111111,  0.        ,  0.41666667,  0.22222222,  0.        ],
                          [ 0.2375    ,  0.        ,  0.075     ,  0.        ,  0.6875    ],
                          [ 0.53125   ,  0.125     ,  0.        ,  0.        ,  0.34375   ]])

all_total_rewards = []

for i, robot in enumerate(robots):
    # payoff_matrix = payoff_matrices[i]
    epsilon = epsilons[i]
    total_rewards = []
    for _ in range(args.times):
        total_reward = 0
        averages = np.zeros(num_arms)
        times_chosen = np.zeros(num_arms)

        # parameter for modified UCB
        gamma = 1
        # discount for gittins index policy
        beta = 
        for iteration in range(time_horizon):
            if robot in ['greedy', 'greedy2', 'random']:
                if np.random.uniform() > epsilon and iteration != 0:
                    # be greedy, but pick randomly among all equally good arms
                    all_argmax_idxs = all_argmax(averages)
                    arm = np.random.choice(all_argmax_idxs)
                else:
                    # pick randomly
                    arm = np.random.choice(range(num_arms))
            elif robot == "ucb":
                avg_plus_conf = []
                for i in range(num_arms):
                    avg_plus_conf.append(averages[i] + np.sqrt(2 * np.log(iteration + 2) / times_chosen[i]))
                all_argmax_idxs = all_argmax(avg_plus_conf)
                arm = np.random.choice(all_argmax_idxs)
            elif robot == "ucb2":
                avg_plus_conf = []
                for i in range(num_arms):
                    avg_plus_conf.append(averages[i] + (gamma * np.sqrt(2 * np.log(iteration + 2) / times_chosen[i])))
                all_argmax_idxs = all_argmax(avg_plus_conf)
                arm = np.random.choice(all_argmax_idxs)
                gamma = gamma - (1/29)
            elif robot == "gittins":
                continue

            reward = np.random.choice([0, 1, 2, 3, 4], p=payoff_matrix[arm])
            averages[arm] = ((averages[arm] * times_chosen[arm]) + reward) / (times_chosen[arm] + 1)
            times_chosen[arm] += 1
            total_reward += reward
        total_rewards.append(total_reward)

    print "####################################################################"
    print "Robot: " + robot
    # print total_rewards
    print "Avg: " + str(np.average(total_rewards))
    if len(total_rewards) > 1:
        print min(total_rewards), max(total_rewards)
        print "Std Dev: " + str(np.std(total_rewards))
        print "Std Err: " + str(scipy.stats.sem(total_rewards))
    print "####################################################################"
    print

if args.compare:
    optimal = all_total_rewards[0]
    greedy = all_total_rewards[1]

    times = 0
    for i in range(len(optimal)):
        if greedy[i] >= optimal[i]:
            times += 1
    print times