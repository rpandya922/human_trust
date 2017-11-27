from __future__ import division
import numpy as np
from Tkinter import *
import time

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