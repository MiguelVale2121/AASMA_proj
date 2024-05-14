import random

class RandomAgent:
    def __init__(self, role='prey'):
        self.role = role
        self.moves = {
            'prey': [('up', 0, -1), ('down', 0, 1), ('left', -1, 0), ('right', 1, 0)],
            'hunter': [('up', 0, -1), ('down', 0, 1), ('left', -1, 0), ('right', 1, 0)]
        }
    
    def choose_action(self, state):
        if self.role == 'prey':
            return random.choice(self.moves['prey'])
        elif self.role == 'hunter':
            return random.choice(self.moves['hunter'])