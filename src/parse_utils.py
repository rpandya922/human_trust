from __future__ import division
import numpy as np

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
        entropy += -np.log(c / num_decisions) * (c / num_decisions)
    return entropy