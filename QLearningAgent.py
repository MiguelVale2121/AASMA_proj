import random


class QLearningAgent:
    def __init__(self, name, strategy, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.name = name
        self.strategy = strategy
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}
        self.actions = ['up', 'down', 'left', 'right']

    def get_state(self, state):
        # Define state representation
        prey1_pos = tuple(state['prey1_pos'])
        prey2_pos = tuple(state['prey2_pos'])
        hunter_pos = tuple(state['hunter_pos'])
        return (prey1_pos, prey2_pos, hunter_pos)

    def choose_action(self, state):
        current_state = self.get_state(state)
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(self.actions)
        else:
            action = self.get_best_action(current_state)
        return action, None, None

    def get_best_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}
        q_values = self.q_table[state]
        max_value = max(q_values.values())
        best_actions = [action for action, value in q_values.items() if value == max_value]
        return random.choice(best_actions)

    def update_q_values(self, state, action, reward, next_state):
        state = self.get_state(state)
        next_state = self.get_state(next_state)
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0.0 for a in self.actions}

        best_next_action = self.get_best_action(next_state)
        self.q_table[state][action] = self.q_table[state][action] + self.alpha * (
            reward + self.gamma * self.q_table[next_state][best_next_action] - self.q_table[state][action]
        )

    def get_reward(self, state, action, next_state):
        reward = -1  # Default reward for each move
        
        prey1_pos = state['prey1_pos']
        prey2_pos = state['prey2_pos']
        end_pos = state['end_pos']
        prey1_reach = state['prey1_reach']
        prey2_reach = state['prey2_reach']
        hunter_active = state['hunter_active']
        combined_prey_active = state['combined_prey_active']

        if combined_prey_active and not hunter_active:
            reward = 150  # Reward for combined prey killing the hunter
        elif prey1_pos == end_pos and prey2_pos == end_pos:
            reward = 90  # Reward for both preys reaching the end
        elif prey1_pos == end_pos or prey2_pos == end_pos:
            reward = 50 if prey1_pos == end_pos else -50
            reward = 50 if prey2_pos == end_pos else -50
        else:
            reward = -50  # Penalty for neither prey reaching the end

        return reward
