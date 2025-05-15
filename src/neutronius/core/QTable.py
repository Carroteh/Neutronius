from conf.conf import ACTIONS

class QTable:
    def __init__(self):
        self.table = {}

    def get_best_action(self, state):
        q_vals = self.get_q_row(state)
        best_action = max(zip(q_vals, ACTIONS))
        return best_action[1]

    def get_q_row(self, state):
        if state not in self.table:
            self.table[state] = [0.0 for _ in ACTIONS]
        return self.table[state]

    def update_q_val(self, new_state, last_state, last_action, last_reward, gamma, alpha):
        if last_state not in self.table:
            self.table[last_state] = [0.0 for _ in ACTIONS]

        # Get the Q value from the previous state and action
        prev_q_val_row = self.get_q_row(last_state)
        prev_q_val = prev_q_val_row[ACTIONS.index(last_action)]

        # Get the best Q value in the current state
        old_q_val = max(self.get_q_row(new_state))

        temporal_diff = last_reward + gamma * old_q_val - prev_q_val
        new_q_val = prev_q_val + alpha * temporal_diff

        print(f"Updating Q value for {last_action}: {prev_q_val} -> {new_q_val}")
        self.table[last_state][ACTIONS.index(last_action)] = new_q_val


