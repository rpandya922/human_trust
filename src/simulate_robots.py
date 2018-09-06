from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--ucb', action='store_true')
parser.add_argument('-u2', '--ucb2', action='store_true') # linear decaying exploration
parser.add_argument('--gittins', action='store_true')
parser.add_argument('-g', '--greedy', action='store_true')
parser.add_argument('-g2', '--greedy2', action='store_true')
parser.add_argument('-r', '--random', action='store_true')
parser.add_argument('-r2', '--random2', action='store_true')
parser.add_argument('-c', '--compare', action='store_true')
parser.add_argument('-t', '--times', type=int, default=1)
parser.add_argument('--plot', action='store_true')
parser.add_argument('--entropy', action='store_true')
args = parser.parse_args()

num_arms = 6
time_horizon = 30

def all_argmax(arr):
    return np.argwhere(arr == np.amax(arr)).flatten()
def entropy(times_chosen):
    num_decisions = sum(times_chosen)
    e = 0
    for c in times_chosen:
        if c == 0:
            continue
        e += -np.log2(c / num_decisions) * (c / num_decisions)
    return e
def policy_entropy(human_decisions, num_arms):
    arm_counts = np.zeros(num_arms)
    for arm in human_decisions:
        arm_counts[arm] += 1
    num_decisions = len(human_decisions)
    entropy = 0
    for c in arm_counts:
        if c == 0:
            continue
        entropy += -np.log2(c / num_decisions) * (c / num_decisions)
    return entropy
def entropy_over_time(decisions, num_arms):
    entropies = []
    decisions_so_far = []
    for decision in decisions:
        decisions_so_far.append(decision)
        entropies.append(policy_entropy(decisions_so_far, num_arms))
    return entropies

# payoff_matrices = []
epsilons = []
robots = []
plot_colors = []
if args.ucb:
    epsilons.append(0)
    robots.append("UCB")
    plot_colors.append("#70ad47")
if args.ucb2: 
    epsilons.append(0)
    robots.append("HA-UCB")
    plot_colors.append("#4472c4")
if args.gittins:
    epsilons.append(0)
    robots.append("gittins")
if args.greedy:
    epsilons.append(0.1)
    robots.append("0.1-Greedy")
    plot_colors.append("#ffc000")
if args.greedy2:
    epsilons.append(0.3)
    robots.append("0.3-Greedy")
if args.random:
    epsilons.append(0.9)
    robots.append("0.9-Greedy")
    plot_colors.append("#262626")
if args.random2:
    epsilons.append(1)
    robots.append("1-Greedy")

payoff_matrix = np.array([[ 0.25      ,  0.5       ,  0.25      ,  0.        ,  0.        ],
                          [ 0.625     ,  0.        ,  0.25      ,  0.        ,  0.125     ],
                          [ 0.1875    ,  0.75      ,  0.        ,  0.        ,  0.0625    ],
                          [ 0.36111111,  0.        ,  0.41666667,  0.22222222,  0.        ],
                          [ 0.2375    ,  0.        ,  0.075     ,  0.        ,  0.6875    ],
                          [ 0.53125   ,  0.125     ,  0.        ,  0.        ,  0.34375   ]])
# payoff_matrix = np.array([[ 0.03125   ,  0.        ,  0.9375    ,  0.        ,  0.03125   ],
#                        [ 0.55555556,  0.16666667,  0.        ,  0.27777778,  0.        ],
#                        [ 0.16666667,  0.25      ,  0.        ,  0.58333333,  0.        ],
#                        [ 0.375     ,  0.25      ,  0.375     ,  0.        ,  0.        ],
#                        [ 0.171875  ,  0.        ,  0.        ,  0.3125    ,  0.515625  ],
#                        [ 0.25      ,  0.        ,  0.        ,  0.        ,  0.75      ]])

all_total_rewards = []
all_entropies = []
fig, ax = plt.subplots()

for robot_idx, robot in enumerate(robots):
    # payoff_matrix = payoff_matrices[i]
    epsilon = epsilons[robot_idx]
    total_rewards = []
    entropies = []
    entropies_over_time = []
    for _ in range(args.times):
        total_reward = 0
        averages = np.zeros(num_arms)
        times_chosen = np.zeros(num_arms)
        decisions = []
        # parameter for modified UCB
        gamma = 1
        # discount for gittins index policy
        beta = 0.9
        
        for iteration in range(time_horizon):
            if robot in ['0.1-Greedy', '0.3-Greedy', '0.9-Greedy', '1-Greedy']:
                if np.random.uniform() > epsilon and iteration != 0:
                    # be greedy, but pick randomly among all equally good arms
                    all_argmax_idxs = all_argmax(averages)
                    arm = np.random.choice(all_argmax_idxs)
                else:
                    # pick randomly
                    arm = np.random.choice(range(num_arms))
            elif robot == "UCB":
                avg_plus_conf = []
                for i in range(num_arms):
                    avg_plus_conf.append(averages[i] + np.sqrt(2 * np.log(iteration + 2) / times_chosen[i]))
                all_argmax_idxs = all_argmax(avg_plus_conf)
                arm = np.random.choice(all_argmax_idxs)
            elif robot == "HA-UCB":
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
            decisions.append(arm)
        total_rewards.append((2.9*30) - total_reward)
        entropies.append(entropy(times_chosen))
        entropies_over_time.append(entropy_over_time(decisions, num_arms))
    all_total_rewards.append(total_rewards)
    all_entropies.append(entropies)

    print "####################################################################"
    print "Robot: " + robot
    # print total_rewards
    print "Avg Regret: " + str(np.average(total_rewards))
    print "Avg Entropy: " + str(np.average(entropies))
    if len(total_rewards) > 1:
        print min(total_rewards), max(total_rewards)
        print "Std Dev: " + str(np.std(total_rewards))
        print "Std Err: " + str(scipy.stats.sem(total_rewards))
    print "####################################################################"
    print

    if args.entropy:
        entropies_over_time = np.array(entropies_over_time)
        std_errors = [np.std(entropies_over_time[:,j]) / np.sqrt(args.times) for j in range(len(entropies_over_time[0]))]
        ents = np.average(entropies_over_time, axis=0)
        print robot_idx
        ax.plot(np.arange(len(ents)), ents, label=robot, color=plot_colors[robot_idx], linewidth=3)
        print ents[-1]
        ax.fill_between(np.arange(len(ents)), ents - std_errors, ents + std_errors, alpha=0.3, color=plot_colors[robot_idx])
        # ax.set_ylim(0, 1.8)
if args.entropy:
    ax.plot(np.arange(30), np.ones(30)*2.5849, linestyle='--', color='k', label='Maximum Entropy', linewidth=3)
    ax.set_xlabel("Number of Pulls")
    ax.set_ylabel("Entropy of Arm Pulls")
    ax.legend()
    ax.set_title("Average Entropy over 10,000 Trials")
    ax.set_xlim(0, 29)
    plt.show()

if args.compare:
    optimal = all_total_rewards[0]
    greedy = all_total_rewards[1]

    times = 0
    for i in range(len(optimal)):
        if greedy[i] >= optimal[i]:
            times += 1
    print times
if args.plot:
    fig, ax = plt.subplots()
    print np.average(all_total_rewards, axis=1)
    ax.bar(np.arange(len(robots)), np.average(all_total_rewards, axis=1))
    plt.show()