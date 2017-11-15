from __future__ import division
import numpy as np

class Arm():
    def __init__(self, mean, stddev):
        self.mean = mean
        self.stddev = stddev
        self.samples = 0
        self.average = 0
    def sample(self):
        val = np.random.normal(self.mean, self.stddev)
        self.average = ((self.average * self.samples) + val) / (self.samples + 1)
        self.samples += 1
        return val

class GaussianArm():
    def __init__(self, mean, stddev):
        self.mean = mean
        self.stddev = stddev
        self.samples = 0
        self.average = 0
    def sample(self):
        val = np.random.normal(self.mean, self.stddev)
        self.average = ((self.average * self.samples) + val) / (self.samples + 1)
        self.samples += 1
        return val

class BernoulliArm():
    def __init__(self, p, reward=1):
        self.p = p
        self.reward = reward
        self.samples = 0
        self.average = 0
    def sample(self):
        val = np.random.choice([0, self.reward], p=[1 - self.p, self.p])
        self.average = ((self.average * self.samples) + val) / (self.samples + 1)
        self.samples += 1
        return val
