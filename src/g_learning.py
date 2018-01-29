from __future__ import division
# from __future__ import print_function
import gym
import itertools
import matplotlib
import numpy as np
import gym_bandits
import plotting
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.stats import entropy
import pickle

################################################################################
# CONSTANTS
human_epsilon = 0.3
best_arm = 5
seed = 0
np.random.seed(seed)
# prob_pick_best = 1 - human_epsilon
# other_prob = human_epsilon / (10 - 1)
# rho = np.ones((1, 10)) * other_prob
# rho[0][best_arm] = prob_pick_best
DATA_FOLDER = '../data/simulation'
################################################################################

class GLearningAgent():
    def __init__(self, env, k):
        ns, na = env.observation_space.n, env.action_space.n
        self.G = np.zeros((ns, na))
        self.N = np.zeros((ns, na))
        # self.rho = rho
        self.rho = np.ones((ns, na)) / na
        self.k = k

    def policy_exploration(self, state, epsilon=0.0):
        """ The agent's current exploration policy. Right now we default to
        epsilon-greedy on the G(s,a) values.

        Args:
            state: The current state the agent is in.
            epsilon: The probability of taking a random action.

        Returns:
            The action to take.
        """
        na = self.G.shape[1]
        action_probs = np.ones(na, dtype=float) * epsilon / na
        best_action = np.argmax(self.G[state,:]) 
        action_probs[best_action] += (1.0-epsilon)
        return np.random.choice(np.arange(na), p=action_probs)

    def alpha_schedule(self, t, state, action):
        """ The alpha scheduling. By default, Equation 29 in the paper.
        
        Args:
            t: The iteration of the current episode (t >= 1).
            state: The current state.
            action: The current action.
        Returns:
            The alpha to use for the G-learning update.
        """
        alpha = self.N[state,action] ** -0.8
        assert 0 < alpha <= 1, "Error, alpha = {}".format(alpha)
        return alpha


    def beta_schedule(self, t):
        """ The beta scheduling. By default, Equation 26 in the paper.
        
        Args:
            t: The iteration of the current episode (t >= 1).
        Returns:
            The beta to use for the G-learning update. If it's 0, G-learning
            turns into Q^\rho-learning. If it approaches infinity, G-learning
            approaches Q-learning.
        """
        beta = self.k * t
        assert beta >= 0, "Error, beta={}, k={}, t={}".format(beta, self.k, t)
        return beta

    def kl_divergence(self):
        # p = np.zeros(self.G.shape[1])
        # p[np.argmax(self.G[0])] = 1
        p = np.exp(self.G[0])
        q = self.rho[0]
        return entropy(p, q)

    def g_learning(self, num_episodes, max_ep_steps=10000, discount=1.0, epsilon=0.1):
        """ The G-learning algorithm.
    
        Args:
            num_episodes: Number of episodes to run.
            max_ep_steps: Maximum time steps allocated to one episode.
            discount: Standard discount factor, usually denoted as \gamma.
            epsilon: Probability of taking random actions during exploration.
    
        Returns:
            A tuple (G, stats) of the G-values and statistics, which should be
            plotted and thoroughly analyzed.
        """
        cum_t = 0
        stats = plotting.EpisodeStats(episode_lengths=np.zeros(num_episodes),
                                      episode_rewards=np.zeros(num_episodes),
                                      kl_divergence=np.zeros(num_episodes))

        for i_episode in tqdm(range(num_episodes)):
            state = env.reset()

            # Run this episode until we finish as indicated by the environment.
            for t in range(1, max_ep_steps+1):

                # Uses exploration policy to take a step.
                action = self.policy_exploration(state, epsilon)
                next_state, reward, done, _ = env.step(action)
                # cost = -reward
                # print(reward) 

                # Collect statistics (cum_t currently not used).
                stats.episode_rewards[i_episode] += reward
                stats.episode_lengths[i_episode] = t
                stats.kl_divergence[i_episode] = self.kl_divergence()
                self.N[state,action] += 1
                cum_t += 1

                # Intermediate terms for the G-learning update.
                alpha = self.alpha_schedule(t, state, action)
                beta = self.beta_schedule(t)
                temp = np.sum(self.rho[next_state,:] * 
                              np.exp(-beta * self.G[next_state,:]))

                # Official G-learning update at last. Equation 18 in the paper.
                td_target = -reward - (discount/beta) * np.log(temp)
                td_delta = td_target - self.G[state,action]
                self.G[state,action] += (alpha * td_delta)

                if done:
                    break
                state = next_state
    
        print
        return self.G, stats
    

class QLearningAgent():

    def __init__(self, env):
        """ For now, we'll make a limitation that we know the number of states
        and actions.  It creates:
        
        - Q: Contains Q(state,action) values.
        - N: Contains N(state,action) values, counts of the times each
            state-action pair was visited; needed for some alpha updates.
        Args:
            env: An OpenAI gym environment, either custom or built-in, but be
                aware that not all of them can be used in this setting.
        """
        ns, na = env.observation_space.n, env.action_space.n
        self.Q = np.zeros((ns,na))
        self.N = np.zeros((ns,na))


    def policy_exploration(self, state, epsilon=0.0):
        """ The agent's current exploration policy. Right now we default to
        epsilon-greedy on the Q(s,a) values.
        
        Args:
            state: The current state the agent is in.
            epsilon: The probability of taking a random action.
        
        Returns:
            The action to take.
        """
        na = self.Q.shape[1]
        action_probs = np.ones(na, dtype=float) * epsilon / na
        best_action = np.argmax(self.Q[state,:])
        action_probs[best_action] += (1.0-epsilon)
        return np.random.choice(np.arange(na), p=action_probs)
 

    def alpha_schedule(self, t, state, action):
        """ The alpha scheduling.
        
        Args:
            t: The iteration of the current episode (t >= 1).
            state: The current state.
            action: The current action.
        Returns:
            The alpha to use for the Q-learning update.
        """
        # return 0.5     # the most basic strategy
        alpha = self.N[state,action] ** -0.8
        assert 0 < alpha <= 1, "Error, alpha = {}".format(alpha)
        return alpha

    def kl_divergence(self):
        # p = np.zeros(self.Q.shape[1])
        # p[np.argmax(self.Q[0])] = 1
        p = np.exp(self.Q[0])
        q = rho[0]
        return entropy(p, q)

    def q_learning(self, num_episodes, max_ep_steps=10000, discount=1.0, epsilon=0.1):
        """ The Q-learning algorithm.
    
        Args:
            num_episodes: Number of episodes to run.
            max_ep_steps: Maximum time steps allocated to one episode.
            discount: Standard discount factor, usually denoted as \gamma.
            epsilon: Probability of taking random actions during exploration.
    
        Returns:
            A tuple (Q, stats) of the Q-values and statistics, which should be
            plotted and thoroughly analyzed.
        """
        cum_t = 0
        stats = plotting.EpisodeStats(episode_lengths=np.zeros(num_episodes),
                                      episode_rewards=np.zeros(num_episodes),
                                      kl_divergence=np.zeros(num_episodes))

        for i_episode in tqdm(range(num_episodes)):
            state = env.reset()

            # Run this episode until we finish as indicated by the environment.
            for t in range(1, max_ep_steps+1):

                # Uses exploration policy to take a step.
                action = self.policy_exploration(state, epsilon)
                next_state, reward, done, _ = env.step(action)

                # Collect statistics (cum_t currently not used).
                stats.episode_rewards[i_episode] += reward
                stats.episode_lengths[i_episode] = t
                stats.kl_divergence[i_episode] = self.kl_divergence()
                self.N[state,action] += 1
                cum_t += 1

                # The official Q-learning update.
                alpha = self.alpha_schedule(t, state, action)
                best_next_action = np.argmax(self.Q[next_state,:])
                td_target = reward + discount * self.Q[next_state,best_next_action]
                td_delta = td_target - self.Q[state,action]
                self.Q[state,action] += (alpha * td_delta)

                if done:
                    break
                state = next_state
    
        print("")
        return self.Q, stats

if __name__ == "__main__":
    num_episodes = 5000
    env = gym.make("BanditTenArmedRandomFixed-v0")

    avg_rewards = [0] * 10
    times_played = [0] * 10
    for i in range(10):
        env.reset()
        if i == 0:
            action = np.random.choice(np.arange(10))
        else:
            be_greedy = np.random.uniform()
            if be_greedy > human_epsilon:
                action = np.argmax(avg_rewards)
            else:
                action = np.random.choice(np.arange(10))
        next_state, reward, done, _ = env.step(action)
        if times_played[action] == 0:
            times_played[action] += 1
            avg_rewards[action] += reward
        else:
            avg_rewards[action] = ((avg_rewards[action] * times_played[action]) + \
                                  reward) / (times_played[action] + 1)
            times_played[action] += 1

    print avg_rewards
    print env.env.p_dist
    best_arm = np.argmax(avg_rewards)
    prob_pick_best = 1 - human_epsilon
    other_prob = human_epsilon / (10 - 1)
    rho = np.ones((1, 10)) * other_prob
    rho[0][best_arm] = prob_pick_best

    agent = GLearningAgent(env, k=1e-3)
    G, g_stats = agent.g_learning(num_episodes=num_episodes,
                                max_ep_steps=500,
                                discount=0.95,
                                epsilon=0.5)
    agent = QLearningAgent(env) 
    Q, q_stats = agent.q_learning(num_episodes=num_episodes,
                                max_ep_steps=500,
                                discount=0.95,
                                epsilon=0.1)
    mu_star = max(env.env.p_dist)
    g_regret = []
    g_rewards = []
    t = 0
    for i, r in enumerate(g_stats.episode_rewards):
        t += r
        g_rewards.append(t)
        g_regret.append(t / (mu_star * (i+1)))

    q_regret = []
    q_rewards = []
    t = 0
    for i, r in enumerate(q_stats.episode_rewards):
        t += r
        q_rewards.append(t)
        q_regret.append(t / (mu_star * (i+1)))

    # pickle_dict = {'g_rewards': g_rewards, 'q_rewards': q_rewards,\
    #                'g_divergence': g_stats.kl_divergence, \
    #                'q_divergence': q_stats.kl_divergence}
    # output = open('%s/sim_%d.pkl' % (DATA_FOLDER, seed), 'wb')
    # pickle.dump(pickle_dict, output)
    # output.close()
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    # fig, axes = plt.subplots(nrows=1, ncols=2)
    # axes = np.ndarray.flatten(np.array(axes))
    # ax = axes[0]
    # ax2 = axes[1]
    ax.set_xlim(0, num_episodes)
    ax.set_ylim(0, 1.1)
    ax2.set_xlim(0, num_episodes)
    ax2.set_ylim(0, 3.5)
    x = np.arange(0, num_episodes)

    ax.plot(x, q_regret, label='Q-learning', lw=3, c='#838383')
    ax.plot(x, g_regret, label='G-learning', lw=3, c='#e67e00')
    ax.plot(x, [1]*num_episodes, c='k', lw=3, linestyle='dashed')
    # ax.plot(x, [mu_star * num_episodes]* num_episodes, label='Maximum Possible Reward')

    ax2.plot(x, q_stats.kl_divergence, label='Q-learning', lw=3, c='#838383')
    ax2.plot(x, g_stats.kl_divergence, label='G-learning', lw=3, c='#e67e00')
    
    lgnd = ax.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left")
    lgnd.legendHandles[0]._sizes = [30]
    lgnd.legendHandles[1]._sizes = [30]
    plt.show()
