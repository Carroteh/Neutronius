from typing import Callable

from neutronius.core.QTable import QTable
import pickle
from conf.conf import ACTIONS
import random

class Agent:
    def __init__(self, get_state: Callable, seed: int):
        try:
            file = f"qtables/qtable{str(seed)}.b"
            f = open(file, "rb")
            print(f"Loading Q-table {file}")
            self._qTable = pickle.load(f)
            f.close()
        except Exception:
            self._qTable = QTable()
        self._epsilon = 1.0
        self._alpha = 0.1
        self._gamma = 0.9
        self._seed = seed
        self._get_state = get_state
        self._last_state = ()
        self._last_reward = 0
        self._last_action = 'UP'
        self._training = True
        self._actions = ACTIONS

    def act(self):
        action = ''
        state = self._get_state()
        #print(f"Current state: {state}")
        if not self._training:
            action = self._qTable.get_best_action(state)
            print(f"Performing best action: {action}")
        else:
            # Update Q-value based on reward from previous action
            print(f"Rewarded for action: {self._last_reward}")

            # Update Q value based on previous action
            self.qTable.update_q_val(
                state,
                self._last_state,
                self._last_action,
                self._last_reward,
                self._gamma,
                self._alpha
            )

            # Decide whether to pick a random action
            if random.random() < self._epsilon:
                action =  random.choice(self._actions)
                print(f"Performing random action: {action}")
            else:
                # Get the current state, to choose the best action
                action = self._qTable.get_best_action(state)
                print(f"Performing best action: {action}")

            self._last_state = state
            self._last_action = action

        if self._epsilon > 0.2:
            self._epsilon *= 0.999
        return action


    @property
    def epsilon(self):
        return self._epsilon

    @epsilon.setter
    def epsilon(self, epsilon):
        self._epsilon = epsilon

    @property
    def reward(self):
        return self._last_reward

    @reward.setter
    def reward(self, reward):
        self._last_reward = reward

    @property
    def qTable(self):
        return self._qTable

    @qTable.setter
    def qTable(self, table):
        self._qTable = table

    @property
    def training(self):
        return self._training

    @training.setter
    def training(self, training):
        self._training = training