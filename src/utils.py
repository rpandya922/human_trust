from __future__ import division
import numpy as np
from Tkinter import *
import time
import abc

class BernoulliArm():
    def __init__(self, p, reward=1, name=-1):
        self.p = p
        self.reward = reward
        self.samples = 0
        self.average = 0
        self.name = name
    def sample(self, turns, reward, next_iter, arm_chosen, prev_reward):
        val = np.random.choice([0, self.reward], p=[1 - self.p, self.p])
        self.average = ((self.average * self.samples) + val) / (self.samples + 1)
        self.samples += 1

        turns.set(turns.get() + 1)
        reward.set(reward.get() + val)
        next_iter.set(True)
        arm_chosen.set(self.name)
        prev_reward.set(val)

        return val

class GaussianArm():
    def __init__(self, mean, stddev):
        self.mean = mean
        self.stddev = stddev
        self.samples = 0
        self.average = 0
    def sample(self, turns, reward, next_iter):
        val = np.random.normal(self.mean, self.stddev)
        self.average = ((self.average * self.samples) + val) / (self.samples + 1)
        self.samples += 1

        turns.set(turns.get() + 1)
        reward.set(reward.get() + val)
        next_iter.set(True)

        return val

class Window(Frame):
    def __init__(self, master=None, title='Arms'):
        Frame.__init__(self, master)
        self.master = master
        self.master.title(title)

def click_button(root, button):
    root.update_idletasks()
    root.update()
    time.sleep(0.25)
    button.config(relief=SUNKEN, state=ACTIVE)
    root.update_idletasks()
    root.update()
    time.sleep(0.25)
    button.config(relief=RAISED, state=NORMAL)
    root.update_idletasks()
    root.update()
    time.sleep(0.5)
    button.invoke()

class LFDModel(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, arms):
        """Initialize with list of BernoulliArm objects"""
        self.arms = arms

    @abc.abstractmethod
    def update(self, reward, arm_idx, average_rewards):
        """Update current model using reward from chosen arm"""
        return
    @abc.abstractmethod
    def sample(self, arms=None):
        """Return which arm index to sample from based on current model for the
           given set of arms (should default to self.arms)"""
        return

class EpsilonModel(LFDModel):
    def __init__(self, arms):
        super(EpsilonModel, self).__init__(arms)
        self.epsilon = 0
        self.iterations = 0
        self.times_suboptimal = 0
    def update(self, reward, arm_idx, average_rewards):
        if self.iterations == 0:
            self.iterations += 1
            self.epsilon = 0.0
            return
        self.iterations += 1
        best_idx = np.argmax([a.average for a in self.arms])
        if arm_idx != best_idx:
            self.times_suboptimal += 1
        self.epsilon = self.times_suboptimal / self.iterations
    def sample(self, arms=None):
        if arms is None:
            arms = self.arms
        best_idx = np.argmax([a.average for a in arms])
        be_greedy = np.random.choice([0, 1], p=[self.epsilon, 1 - self.epsilon])
        if be_greedy:
            return best_idx
        else:
            return np.random.choice(list(range(len(arms))))