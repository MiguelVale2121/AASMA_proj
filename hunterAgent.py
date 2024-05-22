from math import sqrt
import random

class HunterAgent:
    def __init__(self):
        pass

    def choose_action(self, state):
        hunter_pos = state['hunter_pos']
        prey1_pos = state['prey1_pos']
        prey2_pos = state['prey2_pos']
        obstacles = state['obstacles']
        
        # Calculate possible moves
        possible_moves = ['up', 'down', 'left', 'right']
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
                if state['prey1_active']:
                    distance1 = sqrt((new_position[0] - prey1_pos[0])**2 + (new_position[1] - prey1_pos[1])**2)
                    if distance1 < min_distance:
                        min_distance = distance1
                        best_move = move
                if state['prey2_active']:
                    distance2 = sqrt((new_position[0] - prey2_pos[0])**2 + (new_position[1] - prey2_pos[1])**2)
                    if distance2 < min_distance:
                        min_distance = distance2
                        best_move = move
            
        if best_move == None:
            best_move = random.choice(possible_moves)

            new_position = hunter_pos[:]
            if move == 'up' and hunter_pos[1] > 0:
                new_position[1] -= 1
            elif move == 'down' and hunter_pos[1] < state['grid_size'] - 1:
                new_position[1] += 1
            elif move == 'left' and hunter_pos[0] > 0:
                new_position[0] -= 1
            elif move == 'right' and hunter_pos[0] < state['grid_size'] - 1:
                new_position[0] += 1

            if tuple(new_position) in obstacles:
                best_move = None

        return best_move, None, None