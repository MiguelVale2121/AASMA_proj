from math import sqrt

class HunterAgent:
    def __init__(self):
        pass

    def choose_action(self, state):
        hunter_pos = state['hunter_pos']
        prey1_pos = state['prey1_pos']
        prey2_pos = state['prey2_pos']
        obstacles = state['obstacles']
        
        # Determine which prey to chase (prefer prey1 if both are active)
        target_prey_pos = prey1_pos if state['prey1_active'] else prey2_pos
        
        # If both preys are inactive, no movement is necessary
        if target_prey_pos is None:
            return None, None, None

        # Calculate possible moves
        possible_moves = ['up', 'down', 'left', 'right', None]
        best_move = None
        min_distance = float('inf')

        for move in possible_moves:
            new_position = hunter_pos[:]
            if move == 'up' and hunter_pos[1] > 0:
                new_position[1] -= 1
            elif move == 'down' and hunter_pos[1] < state['grid_size'] - 1:
                new_position[1] += 1
            elif move == 'left' and hunter_pos[0] > 0:
                new_position[0] -= 1
            elif move == 'right' and hunter_pos[0] < state['grid_size'] - 1:
                new_position[0] += 1
            
            if tuple(new_position) not in obstacles:
                distance = sqrt((new_position[0] - target_prey_pos[0])**2 + (new_position[1] - target_prey_pos[1])**2)
                if distance < min_distance:
                    min_distance = distance
                    best_move = move
        
        return best_move, None, None