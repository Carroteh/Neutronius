from typing import Callable

from neutronius.core.QTable import QTable
import pickle
from conf.conf import ACTIONS
import random

class Agent:
    def __init__(self, get_state: Callable):
        try:
            f = open("qtables/qtable.b", "rb")
            self._qTable = pickle.load(f)
            f.close()
        except Exception:
            self._qTable = QTable()
        self._epsilon = 1.0
        self._alpha = 0.1
        self._gamma = 0.9
        self._get_state = get_state
        self._last_state = ()
        self._last_reward = 0
        self._last_action = 'UP'
        self._training = True
        self._actions = ACTIONS

    def act(self):
        action = ''
        state = self._get_state()
        print(f"Current state: {state}")
        if not self._training:
            pass
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

        if self._epsilon > 0.1:
            self._epsilon *= 0.9999
        return action


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