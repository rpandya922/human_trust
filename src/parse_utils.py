from __future__ import division
import numpy as np

def all_argmax(arr):
    return np.argwhere(arr == np.amax(arr)).flatten()
def percent_agreement(human_decisions, robot_decisions):
    times_agree = 0
    interaction_length = len(robot_decisions)
    for i, human_decision in enumerate(human_decisions):
        robot_decision = robot_decisions[i]
        if human_decision in robot_decision:
            times_agree += 1
    return times_agree / interaction_length
def percent_agreement_initial(human_decisions, robot_decisions):
    times_agree = 0
    interaction_length = len(robot_decisions)
    for i, human_decision in enumerate(human_decisions):
        robot_decision = robot_decisions[i]
        # arm number person inputs will be 1 off from stored arm indices
        if (human_decision - 1) in robot_decision:
            times_agree += 1
    return times_agree / interaction_length
def change_mind_to_robot(before_suggest_decisions, human_decisions, robot_decisions):
    interaction_length = len(robot_decisions)
    times_changed_to_robot = 0
    times_changed_against_robot = 0
    times_disagree = 0
    times_agree = 0
    for i, human_decision in enumerate(human_decisions):
        before_suggest_decision = before_suggest_decisions[i] - 1
        robot_decision = robot_decisions[i]
        
        if before_suggest_decision not in robot_decision:
            # initially disagree
            times_disagree += 1
            if human_decision in robot_decision:
                # changed mind to agree with robot
                times_changed_to_robot += 1
        else:
            # initially agree
            times_agree += 1
            if human_decision not in robot_decision:
                # changed mind to disagree with robot
                times_changed_against_robot += 1
    if times_disagree == 0:
        return None, times_changed_against_robot / times_agree
    return times_changed_to_robot / times_disagree, times_changed_against_robot / times_agree
def time_until_all_explored(human_decisions, num_arms):
    explored = set()
    for i in range(30):
        explored.add(human_decisions[i])
        if set(range(num_arms)) <= explored:
            return i
    return 30
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
def get_robot_name(name):
    if name == 'random_hard_collaborate_suggest':
        return '0.9-Greedy'
    elif name == 'optimal2_hard_collaborate_suggest':
        return 'HA-UCB'
    elif name == 'greedy_hard_collaborate_suggest':
        return '0.1-Greedy'
    elif name == 'optimal_hard_collaborate_suggest':
        return 'UCB'
def time_until_all_explored(human_decisions, num_arms):
    explored = set()
    for i in range(30):
        explored.add(human_decisions[i])
        if set(range(num_arms)) <= explored:
            return i
    return 30
def get_exploratory_actions(human_decisions, average_rewards):
    exploratory = []
    average_rewards.insert(0, [0, 0, 0, 0, 0, 0])
    average_rewards.pop()

    for i, (decision, averages) in enumerate(zip(human_decisions, average_rewards)):
        if type(decision) == 'list':
            if set(decision) != set(all_argmax(averages)):
                exploratory.append(i)
        else:
            if decision not in all_argmax(averages):
                exploratory.append(i)
    return exploratory
def entropy_over_time(human_decisions, num_arms):
    entropies = []
    decisions_so_far = []
    for decision in human_decisions:
        decisions_so_far.append(decision)
        entropies.append(policy_entropy(decisions_so_far, num_arms))
    return entropies
def entropy_over_time_robot(human_decisions, robot_decisions, num_arms):
    entropies = []
    decisions_so_far = []
    for i, (human_decision, robot_decision) in enumerate(zip(human_decisions, robot_decisions)):
        decisions_copy = decisions_so_far[:]
        decisions_copy.append(robot_decision[0])
        entropies.append(policy_entropy(decisions_copy, num_arms))
        decisions_so_far.append(human_decision)
    return entropies