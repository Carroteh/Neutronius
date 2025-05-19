from collections.abc import Callable

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import deque

from pygame.key import start_text_input

from conf.conf import *

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self._input_layer = nn.Linear(state_size, 128)
        self._hidden_layer = nn.Linear(128, 128)
        self._output_layer = nn.Linear(128, action_size)
        nn.init.uniform_(self._output_layer.weight, -0.1, 0.1)
        nn.init.zeros_(self._output_layer.bias)

    def forward(self, x):
        x = F.relu(self._input_layer(x))
        x = F.relu(self._hidden_layer(x))
        return self._output_layer(x)

class DeepAgent(nn.Module):
    def __init__(self, state_size, get_state: Callable, seed, training=True):
        super(DeepAgent, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        random.seed(seed)
        torch.manual_seed(seed)

        self._state_size = state_size
        self._action_size = len(ACTIONS)
        self.seed = seed
        self._get_state = get_state
        self._gamma = 0.95
        self._epsilon = 0.99
        self._alpha = 0.001
        self._steps = 0
        self._batch_size = 64
        self._initial = True

        self._last_state = None
        self.training = training
        self._last_reward = 0
        self._last_action = 'UP'
        self._last_done = False

        self.model = QNetwork(state_size, self._action_size).to(self.device)

        # Target Q-network
        self.target_model = QNetwork(state_size, self._action_size).to(self.device)
        self.update_target_network()

        self.memory = deque(maxlen=100000)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self._alpha)
        self.loss = nn.MSELoss()
        if not self.training:
            self.model.eval()
            self.model.load_state_dict(torch.load(f"qtables/DQN{str(self.seed)}.b"))

        self.model.to(self.device)

    def update_target_network(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def forward(self, x):
        return self.model(x)

    def target_forward(self, x):
        return self.target_model(x)

    def remember(self, state, action, reward, next_state, done):
        # Add an experience to the deque
        self.memory.append((state, action, reward, next_state, done))

    def act(self):
        state = self._get_state()

        # Training
        if self.training:
            if random.random() <= self._epsilon:
                action = random.choice(ACTIONS)
                print(f"Performing random action: {action}")
                return action
            else:
                # Check if this is the first iteration

                if not self._initial:
                    self.remember(self._last_state, self._last_action, self._last_reward, state, self._last_done)
                    self._last_done = False

                self._initial = False
                state = torch.FloatTensor(state).unsqueeze(0)
                self.model(state)

                #Choose the best action
                with torch.no_grad():
                    q_values = self.model(state.unsqueeze(0))
                action = torch.argmax(q_values).item()
                actual_action = self._unpack_action(action)

                # Save variables for next iteration
                self._last_state = state
                self._last_action = action
                print(f"Training Q-values: {self.model(state)}")
                print(f"Performing best action: {actual_action}")
                if self._epsilon > 0.1:
                    self._epsilon *= 0.9999
                return actual_action
        # Pure inference
        else:
            state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
            with torch.no_grad():
                q_values = self.model(state.unsqueeze(0))
            action = torch.argmax(q_values).item()
            actual_action = self._unpack_action(action)
            print(f"Performing best action: {actual_action}")
            return actual_action

    def replay(self):
        if len(self.memory) < self._batch_size:
            return
        batch = random.sample(self.memory, self._batch_size)

        states, actions, rewards, next_states, dones = zip(*batch)
        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)

        q_values = self.model(states).gather(1, actions)
        with torch.no_grad():
            next_q_values = self.target_forward(next_states).max(1)[0]
        target_q_values = rewards + (1 - dones) * self._gamma * next_q_values

        loss = self.loss(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self._steps += 1
        if self._steps % self._update_target_freq == 0:
            self.update_target_network()

    def _unpack_action(self, action):
        return ACTIONS[action]

    def save(self):
        torch.save(self.model.state_dict(), f"qtables/DQN{str(self.seed)}.b")

    def load(self):
        self.model.load_state_dict(torch.load(f"qtables/DQN{str(self.seed)}.b"))
        self.update_target_network()

    @property
    def reward(self):
        return self._last_reward

    @reward.setter
    def reward(self, reward):
        self._last_reward = reward

    @property
    def done(self):
        return self._last_done

    @done.setter
    def done(self, done):
        self._last_done = done
