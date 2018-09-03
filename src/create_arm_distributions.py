from __future__ import division
import numpy as np
from random import shuffle

num_arms = 6
possible_payoffs = list(range(1, 5))
expected_reward_values = [1, 1, 1, 1.5, 1.5, 2.9]
# expected_reward_values = [1, 1, 2, 2, 3, 3]
shuffle(expected_reward_values)
print expected_reward_values

payoff_matrix = []
for reward in expected_reward_values:
    finished = False
    while not finished:
        payoff1, payoff2 = np.random.choice(possible_payoffs, 2, replace=False)
        p = 4 * max(payoff1, payoff2)

        # sample a
        a = np.random.choice(range(1, p))
        b = ((reward * p) - (a * payoff1)) / payoff2

        payoff1_prob = a / p
        payoff2_prob = b / p

        if payoff1_prob >= 0 and payoff1_prob <= 1 and payoff2_prob >= 0 and payoff2_prob <= 1 and payoff1_prob + payoff2_prob <= 1:
            finished = True
        
            zero_prob = 1 - payoff1_prob - payoff2_prob

            probs = np.zeros(len(possible_payoffs)+1)
            probs[0] = zero_prob
            probs[payoff1] = payoff1_prob
            probs[payoff2] = payoff2_prob

            payoff_matrix.append(probs)
# each row represnts one arm:
# to sample, use row as weights for sampling from 0-4
# to find expected reward, take row dot [0 1 2 3 4]
print repr(np.array(payoff_matrix))
print np.dot(payoff_matrix, [0, 1, 2, 3, 4])
