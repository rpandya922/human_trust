from __future__ import division
from utils import *
from Tkinter import *
import tkFont
import numpy as np
import time
from functools import partial
import argparse
import math
import pickle
# 2 3 1 = o r g
################################################################################
# CONSTANTS/FUNCTIONS
parser = argparse.ArgumentParser()
parser.add_argument('--user', type=int, default=None)
args = parser.parse_args()
NUM_TURNS = 30
DATA_FOLDER = "../data/user_%s" % args.user
arms = [BernoulliArm(0.6, 2, name=0), BernoulliArm(1, 1, name=1), \
        BernoulliArm(0.3, 4, name=2), BernoulliArm(0.5, 3, name=3)]
mu_star = max([a.p * a.reward for a in arms])
num_arms = len(arms)
################################################################################
if args.user is None:
    print "Need user number"
    1/0
root = Tk()
# for x in range(60):
#     Grid.columnconfigure(root, x, weight=1)
# for y in range(30):
#     Grid.rowconfigure(root, y, weight=1)

sans = tkFont.Font(family='Sans', size=36)
root.geometry("2400x800")
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

times_suboptimal = 0
decisions = []
average_rewards = []
times_taken = []
regret = []
total_rewards = []

while num_turns.get() < NUM_TURNS:
    avg_rewards = [a.average for a in arms]
    best_arm = np.argmax(avg_rewards)

    root.update_idletasks()
    root.update()
    next_iter.set(False)

    average_rewards.append(np.copy(avg_rewards))

    time_before = time.clock()
    while not next_iter.get():
        root.update_idletasks()
        root.update()
    time_taken = time.clock() - time_before
    choice = arm_chosen.get()

    if num_turns.get() - 1 != 0:
        if choice != best_arm:
            times_suboptimal += 1
    decisions.append(choice)
    regret.append((num_turns.get() * mu_star) - reward.get())
    times_taken.append(time_taken)
    total_rewards.append(reward.get())

    # for button in arm_buttons:
    #     button.config(relief=RAISED, state=NORMAL, fg='black')
    root.update_idletasks()
    root.update()
    time.sleep(0.1)

epsilon = times_suboptimal / (NUM_TURNS - 1)
pickle_dict = {'arms': arms, 'regret': regret, 'human_decisions': decisions,\
               'average_rewards': average_rewards, 'times_taken': times_taken, \
               'epsilon': epsilon, 'reward': total_rewards}
output = open('%s/epsilon.pkl' % DATA_FOLDER, 'wb')
pickle.dump(pickle_dict, output)
output.close()

for button in arm_buttons:
    button.config(state=DISABLED)
root.mainloop()

