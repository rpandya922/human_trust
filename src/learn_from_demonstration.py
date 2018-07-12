from __future__ import division
from utils import *
from Tkinter import *
import tkFont
import numpy as np
import time
from functools import partial
import argparse
import pickle
import math

################################################################################
# CONSTANTS/FUNCTIONS
parser = argparse.ArgumentParser()
parser.add_argument('--robot', type=str, default='greedy')
parser.add_argument('--epsilon', type=float, default=None)
parser.add_argument('--user', type=int, default=None)
parser.add_argument('--pretrain', type=int, default=30)
parser.add_argument('--type', type=str, default='suggest')
args = parser.parse_args()
NUM_TURNS = 30
DATA_FOLDER = "../data/user_%s" % args.user
if args.epsilon is None:
    pkl_file = open('%s/epsilon.pkl' % DATA_FOLDER, 'rb')
    epsilon = pickle.load(pkl_file)['epsilon']
else:
    epsilon = args.epsilon
if args.robot == 'greedy':
    arms = [BernoulliArm(0.9, 1, name=0), BernoulliArm(0.2, 1, name=1), \
            BernoulliArm(0.7, 2, name=2), BernoulliArm(0.5, 3, name=3)]
elif args.robot == 'optimal':
    arms = [BernoulliArm(0.5, 3, name=0), BernoulliArm(0.2, 1, name=1), \
            BernoulliArm(0.9, 1, name=2), BernoulliArm(0.7, 2, name=3)]
elif args.robot == 'random':
    arms = [BernoulliArm(0.5, 3, name=0), BernoulliArm(0.7, 2, name=1), \
            BernoulliArm(0.2, 1, name=2), BernoulliArm(0.9, 1, name=3)]
mu_star = max([a.p * a.reward for a in arms])
num_arms = len(arms)
################################################################################
if args.user is None:
    print "Need user number"
    1/0
root = Tk()

sans = tkFont.Font(family='Sans', size=36)
root.geometry("2500x800")
app = Window(root)

num_turns = IntVar()
num_turns.set(0)
reward = DoubleVar()
reward.set(0)
prev_reward = DoubleVar()
prev_reward.set(0)
next_iter = BooleanVar()
next_iter.set(False)
arm_chosen = IntVar()
arm_chosen.set(-1)
user_turn = StringVar()
user_turn.set('Human')

arm_buttons = []
for i, arm in enumerate(arms):
    button = Button(root, text='Arm %d' % (i+1), font=sans, command=\
    partial(arm.sample, num_turns, reward, next_iter, arm_chosen, prev_reward))
    button.grid(row=0, column=i+2)
    arm_buttons.append(button)

Label(root, text='Iteration: ', font=sans).grid(row=1, column=0)
Label(root, textvariable=num_turns, font=sans).grid(row=1, column=1)
Label(root, text='Previous Reward: ', font=sans).grid(row=2, column=0)
Label(root, textvariable=prev_reward, font=sans).grid(row=2, column=1)
Label(root, text='Total Reward: ', font=sans).grid(row=3, column=0)
Label(root, textvariable=reward, font=sans).grid(row=3, column=1)

human_decsions = []
robot_decisions = []
average_rewards = []
times_taken = []
regret = []
total_rewards = []
model = EpsilonModel(arms)

while num_turns.get() < NUM_TURNS:
    while not next_iter.get():
        root.update_idletasks()
        root.update()
    next_iter.set(False)

    model.update(prev_reward.get(), arm_chosen.get())
    print model.epsilon

    for button in arm_buttons:
        button.config(relief=RAISED, state=NORMAL, fg='black')
    root.update_idletasks()
    root.update()
    time.sleep(0.1)

