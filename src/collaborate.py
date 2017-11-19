from Tkinter import *
import tkFont
import numpy as np
import time
from functools import partial

class BernoulliArm():
    def __init__(self, p, reward=1):
        self.p = p
        self.reward = reward
        self.samples = 0
        self.average = 0
    def sample(self, turns, reward, next_iter):
        val = np.random.choice([0, self.reward], p=[1 - self.p, self.p])
        self.average = ((self.average * self.samples) + val) / (self.samples + 1)
        self.samples += 1

        turns.set(turns.get() + 1)
        reward.set(reward.get() + val)
        next_iter.set(True)

        return val

class Window(Frame):
    def __init__(self, master=None, title='GUI'):
        Frame.__init__(self, master)
        self.master = master
        self.master.title(title)

def click_button(button):
    root.update_idletasks()
    root.update()
    time.sleep(0.5)
    button.config(relief=SUNKEN, state=ACTIVE)
    root.update_idletasks()
    root.update()
    time.sleep(0.5)
    button.config(relief=RAISED, state=NORMAL)
    root.update_idletasks()
    root.update()
    time.sleep(0.5)
    button.invoke()

root = Tk()
for x in range(60):
    Grid.columnconfigure(root, x, weight=1)
for y in range(30):
    Grid.rowconfigure(root, y, weight=1)

sans = tkFont.Font(family='Sans', size=20)
root.geometry("1200x400")
app = Window(root)

num_turns = IntVar()
num_turns.set(0)
reward = DoubleVar()
reward.set(0)
next_iter = BooleanVar()
next_iter.set(False)

arms = [BernoulliArm(1, 1), BernoulliArm(1, 2), BernoulliArm(1, 3), BernoulliArm(1, 4)]
epsilon = 0.3
num_arms = len(arms)

arm_buttons = []
for i, arm in enumerate(arms):
    button = Button(root, text='Arm %d' % (i+1), font=sans, command=\
    partial(arm.sample, num_turns, reward, next_iter))
    button.grid(row=0, column=i+2)
    arm_buttons.append(button)

Label(root, text='Iteration: ', font=sans).grid(row=1, column=0)
Label(root, textvariable=num_turns, font=sans).grid(row=1, column=1)
Label(root, text='Total Reward: ', font=sans).grid(row=2, column=0)
Label(root, textvariable=reward, font=sans).grid(row=2, column=1)


while num_turns.get() < 10:
    avg_rewards = [a.average for a in arms]
    best_arm = np.argmax(avg_rewards)
    be_greedy = np.random.choice([0, 1], p=[epsilon, 1 - epsilon])
    if be_greedy:
        i = best_arm
    else:
        i = np.random.choice(list(range(num_arms)))

    root.update_idletasks()
    root.update()
    arm_buttons[i].config(fg='green')
    while not next_iter.get():
        root.update_idletasks()
        root.update()
    next_iter.set(False)
    for button in arm_buttons:
        button.config(relief=RAISED, state=NORMAL, fg='black')
    root.update_idletasks()
    root.update()
