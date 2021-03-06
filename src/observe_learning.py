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

################################################################################
# CONSTANTS/FUNCTIONS
parser = argparse.ArgumentParser()
parser.add_argument('--robot', type=str, default='greedy')
parser.add_argument('--epsilon', type=float, default=None)
parser.add_argument('--user', type=int, default=None)
args = parser.parse_args()
NUM_TURNS = 30
DATA_FOLDER = "../data/user_%s" % args.user
if args.epsilon is None:
    pkl_file = open('%s/epsilon.pkl' % DATA_FOLDER, 'rb')
    epsilon = pickle.load(pkl_file)['epsilon']
else:
    epsilon = args.epsilon
if args.robot == 'greedy':
    arms = [BernoulliArm(0.5, 3, name=0), BernoulliArm(0.2, 1, name=1), \
            BernoulliArm(0.9, 1, name=2), BernoulliArm(0.7, 2, name=3)]
elif args.robot == 'optimal':
    arms = [BernoulliArm(0.9, 1, name=0), BernoulliArm(0.7, 2, name=1), \
            BernoulliArm(0.5, 3, name=2), BernoulliArm(0.2, 1, name=3)]
elif args.robot == 'random':
    arms = [BernoulliArm(0.2, 1, name=0), BernoulliArm(0.7, 2, name=1), \
            BernoulliArm(0.9, 1, name=2), BernoulliArm(0.5, 3, name=3)]
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

def n(nex):
    nex.set(True)
next_button = Button(root, text='Next', font=sans, command=partial(n, next_iter))
next_button.grid(row=3, column=num_arms+1)

robot_decisions = []
average_rewards = []
times_taken = []
regret = []
total_rewards = []

while num_turns.get() < NUM_TURNS:
    avg_rewards = [a.average for a in arms]
    if args.robot == 'greedy':
        best_arm = np.argmax(avg_rewards)
        be_greedy = np.random.choice([0, 1], p=[epsilon, 1 - epsilon])
        if be_greedy:
            i = best_arm
        else:
            i = np.random.choice(list(range(num_arms)))
    elif args.robot == 'optimal':
        if num_turns.get() < num_arms:
            i = num_turns.get()
        else:
            avg_rewards = [a.average + math.sqrt(2 * math.log(num_turns.get()) / a.samples) for a in arms]
            i = np.argmax(avg_rewards)
    elif args.robot == 'random':
        i = np.random.choice(list(range(num_arms)))

    root.update_idletasks()
    root.update()
    arm_buttons[i].config(fg='green')
    next_iter.set(False)

    average_rewards.append(np.copy(avg_rewards))

    time_before = time.clock()
    while not next_iter.get():
        root.update_idletasks()
        root.update()
    time_taken = time.clock() - time_before

    robot_decisions.append(i)
    regret.append((num_turns.get() * mu_star) - reward.get())
    times_taken.append(time_taken)
    total_rewards.append(reward.get())

    click_button(root, arm_buttons[i])
    for button in arm_buttons:
        button.config(relief=RAISED, state=NORMAL, fg='black')
    root.update_idletasks()
    root.update()
    time.sleep(0.1)

if args.robot == 'greedy':
    pickle_dict = {'arms': arms, 'regret': regret, 'robot_decisions': robot_decisions,\
                   'average_rewards': average_rewards, 'times_taken': times_taken, \
                   'epsilon': epsilon, 'reward': total_rewards}
    output = open('%s/observe_greedy.pkl' % DATA_FOLDER, 'wb')
elif args.robot == 'optimal':
    pickle_dict = {'arms': arms, 'regret': regret, 'robot_decisions': robot_decisions,\
                   'arm_values': average_rewards, 'times_taken': times_taken, \
                   'reward': total_rewards}
    output = open('%s/observe_optimal.pkl' % DATA_FOLDER, 'wb')
if args.robot == 'random':
    pickle_dict = {'arms': arms, 'regret': regret, 'robot_decisions': robot_decisions,\
                   'average_rewards': average_rewards, 'times_taken': times_taken, \
                   'reward': total_rewards}
    output = open('%s/observe_random.pkl' % DATA_FOLDER, 'wb')
pickle.dump(pickle_dict, output)
output.close()

for button in arm_buttons:
    button.config(state=DISABLED)
next_button.config(state=DISABLED)
root.mainloop()
