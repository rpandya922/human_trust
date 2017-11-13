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
