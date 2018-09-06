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
def simulation_agreement(human_decisions, all_average_rewards, num_arms, robot):
    times_agree = 0
    times_chosen = np.zeros(num_arms)
    gamma = 1

    for iteration in range(30):
        human_decision = human_decisions[iteration]
        current_avg_rewards = all_average_rewards[iteration]

        if robot == "0.1-Greedy":
            all_best = all_argmax(current_avg_rewards)
            if human_decision in all_best:
                times_agree += 0.9 / len(all_best)
            else:
                times_agree += 0.1 / (num_arms - len(all_best))
        elif robot == "0.9-Greedy":
            all_best = all_argmax(current_avg_rewards)
            if human_decision in all_best:
                times_agree += 0.1 / len(all_best)
            else:
                times_agree += 0.9 / (num_arms - len(all_best))
        elif robot == "HA-UCB":
            avg_plus_conf = []
            for i in range(num_arms):
                avg_plus_conf.append(current_avg_rewards[i] + (gamma * np.sqrt(2 * np.log(iteration + 2) / times_chosen[i])))
            all_best = all_argmax(avg_plus_conf)
            gamma = gamma - (1/29)

            if human_decision in all_best:
                times_agree += 1 / len(all_best)

        elif robot == "UCB":
            avg_plus_conf = []
            for i in range(num_arms):
                avg_plus_conf.append(current_avg_rewards[i] + np.sqrt(2 * np.log(iteration + 2) / times_chosen[i]))
            all_best = all_argmax(avg_plus_conf)

            if human_decision in all_best:
                times_agree += 1 / len(all_best)

        times_chosen[human_decision] += 1
    return times_agree / 30
def implicit_influence_scores(human_decisions, all_average_rewards, num_arms):
    times_chosen = np.zeros(num_arms)
    gamma = 1
    decision_scores = []
    for iteration in range(30):
        human_decision = human_decisions[iteration]
        current_avg_rewards = all_average_rewards[iteration]

        avg_plus_conf = []
        for i in range(num_arms):
            avg_plus_conf.append(current_avg_rewards[i] + (gamma * np.sqrt(2 * np.log(iteration + 2) / times_chosen[i])))
        gamma = gamma - (1/29)

        inf_idxs = [i for i in range(num_arms) if avg_plus_conf[i] == np.inf]
        regular_idxs = [i for i in range(num_arms) if avg_plus_conf[i] != np.inf]
        if len(regular_idxs) != 0:
            max_val = max([avg_plus_conf[i] for i in regular_idxs])
            # max_val = max(avg_plus_conf)

        if human_decision in inf_idxs:
            decision_scores.append(1)
        else:
            if len(inf_idxs) != 0:
                decision_scores.append(0)
            else:
                normalized_scores = avg_plus_conf / max_val
                # print avg_plus_conf
                # print max_val   
                # print normalized_scores
                # print normalized_scores[human_decision]
                decision_scores.append(normalized_scores[human_decision])
        times_chosen[human_decision] += 1

    return decision_scores
def explicit_influence(before_suggest_decisions, human_decisions, robot_decisions, num_arms):
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
    return times_changed_to_robot
def times_until_pulled(human_decisions, robot_decisions):
    times_until_taken = []
    for iteration, robot_decision in enumerate(robot_decisions):
        found = False
        for i in range(iteration, 30):
            if found:
                break
            human_decision = human_decisions[i]
            if human_decision in robot_decision:
                time_taken = i - iteration
                found = True
        if not found:
            time_taken = 30 - iteration
        times_until_taken.append(time_taken)
    return times_until_taken
def simulated_suggestion_acceptance(human_decisions, all_average_rewards, num_arms, robot):
    times_agree = 0
    times_chosen = np.zeros(num_arms)
    gamma = 1
    times_until_taken = []

    for iteration in range(30):
        human_decision = human_decisions[iteration]
        current_avg_rewards = all_average_rewards[iteration]

        if robot == "0.1-Greedy":
            all_best = all_argmax(current_avg_rewards)
            r = np.random.uniform()
            if r > 0.1: # be greedy
                robot_decision = all_best
            else:
                robot_decision = [arm for arm in range(num_arms) if arm not in all_best]
            
        elif robot == "0.9-Greedy":
            all_best = all_argmax(current_avg_rewards)
            r = np.random.uniform()
            if r > 0.9: # be greedy
                robot_decision = all_best
            else:
                robot_decision = [arm for arm in range(num_arms) if arm not in all_best]
            
        elif robot == "HA-UCB":
            avg_plus_conf = []
            for i in range(num_arms):
                avg_plus_conf.append(current_avg_rewards[i] + (gamma * np.sqrt(2 * np.log(iteration + 2) / times_chosen[i])))
            robot_decision = all_argmax(avg_plus_conf)
            gamma = gamma - (1/29)

        elif robot == "UCB":
            avg_plus_conf = []
            for i in range(num_arms):
                avg_plus_conf.append(current_avg_rewards[i] + np.sqrt(2 * np.log(iteration + 2) / times_chosen[i]))
            robot_decision = all_argmax(avg_plus_conf)

        found = False
        for i in range(iteration, 30):
            if found:
                break
            human_decision = human_decisions[i]
            if human_decision in robot_decision:
                time_taken = i - iteration
                found = True
        if not found:
            time_taken = 30 - iteration
        times_until_taken.append(time_taken)

        times_chosen[human_decision] += 1
    return times_until_taken
