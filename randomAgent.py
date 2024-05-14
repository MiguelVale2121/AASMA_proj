import random

class RandomAgent:
    def __init__(self, role='prey'):
        self.role = role
        self.moves = {
            'prey1': [('up', 0, -1), ('down', 0, 1), ('left', -1, 0), ('right', 1, 0)],
            'prey2': [('up', 0, -1), ('down', 0, 1), ('left', -1, 0), ('right', 1, 0)],
            'hunter': [('up', 0, -1), ('down', 0, 1), ('left', -1, 0), ('right', 1, 0)]
        }
    
    def choose_action(self, state):
        if self.role == 'prey1':
            return random.choice(self.moves['prey1'])
        elif self.role == 'prey2':
            return random.choice(self.moves['prey2'])
        elif self.role == 'hunter':
            return random.choice(self.moves['hunter'])