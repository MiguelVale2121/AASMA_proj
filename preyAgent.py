import random
import utils
from math import sqrt


class PreyAgent:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.previous_move_list = []
        self.previous_move = None
        self.recent_positions = []
        self.recent_positions_limit = 5
        self.combined_prey_pos = None

    def choose_action(self, state):
        if self.strategy == "runner":
            return self.runner_strategy_action(state)
        elif self.strategy == "alive":
            return self.alive_strategy_action(state)
        elif self.strategy == "killer":
            return self.killer_strategy_action(state)
        elif self.strategy == "mixed":
            return self.mixed_strategy_action(state)

    def runner_strategy_action(self, state):
        prey_pos = state[f'{self.name}_pos']
        hunter_pos = state['hunter_pos']
        end_pos = state['end_pos']
        obstacles = state['obstacles']
        grid_size = state['grid_size']
        
        possible_moves = ['up', 'down', 'left', 'right']
        best_move = None
        min_distance = float('inf')

        if state['combined_prey_active']:
            self.killer_strategy_action(state)

        for move in possible_moves:
            new_position = self.calculate_new_position(prey_pos, move, grid_size)
            if new_position and tuple(new_position) not in obstacles and new_position not in self.recent_positions:
                distance_to_end = sqrt((new_position[0] - end_pos[0])**2 + (new_position[1] - end_pos[1])**2)
                distance_to_hunter = sqrt((new_position[0] - hunter_pos[0])**2 + (new_position[1] - hunter_pos[1])**2)
                
                if distance_to_end < min_distance and distance_to_hunter > 1 and not self.is_in_corner(new_position, grid_size):
                    min_distance = distance_to_end
                    best_move = move

        if self.is_adjacent_to_obstacle(prey_pos, obstacles):
            safe_moves_from_obstacle = self.is_safe_move_from_obstacle(prey_pos, obstacles, grid_size)
            for move in safe_moves_from_obstacle:
                if move not in self.previous_move_list:
                    self.previous_move_list.append(move)
                    self.previous_move = best_move
                    best_move = move
                    break

        if best_move is None:
            safe_moves = [move for move in possible_moves if self.is_safe_move(prey_pos, move, hunter_pos, obstacles, grid_size)]
            safe_moves = [move for move in safe_moves if not self.is_in_corner(self.calculate_new_position(prey_pos, move, grid_size), grid_size)]
            best_move = random.choice(safe_moves) if safe_moves else None

        new_position = self.calculate_new_position(prey_pos, best_move, grid_size)
        if new_position:
            self.recent_positions.append(new_position)
            if len(self.recent_positions) > self.recent_positions_limit:
                self.recent_positions.pop(0)

        return best_move, None, None

    def alive_strategy_action(self, state):
        prey_pos = state[f'{self.name}_pos']
        hunter_pos = state['hunter_pos']
        obstacles = state['obstacles']
        grid_size = state['grid_size']

        possible_moves = ['up', 'down', 'left', 'right']
        best_move = None
        max_distance_to_hunter = float('-inf')
        
        if state['combined_prey_active']:
            self.killer_strategy_action(state)

        for move in possible_moves:
            new_position = self.calculate_new_position(prey_pos, move, grid_size)
            if new_position and tuple(new_position) not in obstacles and new_position not in self.recent_positions:
                distance_to_hunter = sqrt((new_position[0] - hunter_pos[0])**2 + (new_position[1] - hunter_pos[1])**2)

                if distance_to_hunter > max_distance_to_hunter and not self.is_in_corner(new_position, grid_size):
                    max_distance_to_hunter = distance_to_hunter
                    best_move = move

        if best_move is None:
            safe_moves = [move for move in possible_moves if self.is_safe_move(prey_pos, move, hunter_pos, obstacles, grid_size)]
            safe_moves = [move for move in safe_moves if not self.is_in_corner(self.calculate_new_position(prey_pos, move, grid_size),grid_size)]
            best_move = random.choice(safe_moves) if safe_moves else None

        new_position = self.calculate_new_position(prey_pos, best_move, grid_size)
        if new_position:
            self.recent_positions.append(new_position)
            if len(self.recent_positions) > self.recent_positions_limit:
                self.recent_positions.pop(0)

        return best_move, None, None

    def killer_strategy_action(self, state):
        prey_pos = state[f'{self.name}_pos']
        other_prey_name = 'prey1' if self.name == 'prey2' else 'prey2'
        other_prey_pos = state[f'{other_prey_name}_pos']
        hunter_pos = state['hunter_pos']
        obstacles = state['obstacles']
        grid_size = state['grid_size']

        possible_moves = ['up', 'down', 'left', 'right']
        best_move = None

        if prey_pos == other_prey_pos:
            state['combined_prey_active'] = True
            if self.combined_prey_pos is None:
                self.combined_prey_pos = prey_pos
            min_distance_to_hunter = float('inf')
            for move in possible_moves:
                new_position = self.calculate_new_position(self.combined_prey_pos, move, grid_size)
                if new_position and tuple(new_position) not in obstacles:
                    distance_to_hunter = abs(new_position[0] - hunter_pos[0]) + abs(new_position[1] - hunter_pos[1])
                    if distance_to_hunter < min_distance_to_hunter and not self.is_in_corner(new_position, grid_size):
                        min_distance_to_hunter = distance_to_hunter
                        best_move = move
                        self.combined_prey_pos = new_position
                        state['combined_prey_pos'] = self.combined_prey_pos
        elif (state['prey1_active'] and state['prey2_active']) and prey_pos != other_prey_pos and not state['combined_prey_active']:
            min_distance_to_other_prey = float('inf')
            for move in possible_moves:
                new_position = self.calculate_new_position(prey_pos, move, grid_size)
                if new_position and tuple(new_position) not in obstacles:
                    distance_to_other_prey = abs(new_position[0] - other_prey_pos[0]) + abs(new_position[1] - other_prey_pos[1])
                    if distance_to_other_prey < min_distance_to_other_prey and not self.is_in_corner(new_position, grid_size):
                        min_distance_to_other_prey = distance_to_other_prey
                        best_move = move

        if not state['combined_prey_active'] and self.is_adjacent_to_obstacle(prey_pos, obstacles):
            safe_moves_from_obstacle = self.is_safe_move_from_obstacle(prey_pos, obstacles, grid_size)
            for move in safe_moves_from_obstacle:
                if move not in self.previous_move_list:
                    self.previous_move_list.append(move)
                    self.previous_move = best_move
                    best_move = move
                    break
        elif state['combined_prey_active'] and self.is_adjacent_to_obstacle(self.combined_prey_pos, obstacles):
            safe_moves_from_obstacle = self.is_safe_move_from_obstacle(self.combined_prey_pos, obstacles, grid_size)
            for move in safe_moves_from_obstacle:
                if move not in self.previous_move_list:
                    self.previous_move_list.append(move)
                    self.previous_move = best_move
                    best_move = move
                    break

        if not state['combined_prey_active']:
            new_position = self.calculate_new_position(prey_pos, best_move, grid_size)
            if new_position:
                self.recent_positions.append(new_position)
                if len(self.recent_positions) > self.recent_positions_limit:
                    self.recent_positions.pop(0)
        if state['combined_prey_active']:
            new_position = self.calculate_new_position(self.combined_prey_pos, best_move, grid_size)
            if new_position:
                self.recent_positions.append(new_position)
                if len(self.recent_positions) > self.recent_positions_limit:
                    self.recent_positions.pop(0)

        return best_move, None, None

    def mixed_strategy_action(self, state):
        prey1_pos = state['prey1_pos']
        prey2_pos = state['prey2_pos']
        hunter_pos = state['hunter_pos']

        distance_prey1_to_hunter = 0
        distance_prey2_to_hunter = 0
        
        if state['combined_prey_active']:
            self.killer_strategy_action(state)

        if prey1_pos is not None:
            distance_prey1_to_hunter = sqrt((prey1_pos[0] - hunter_pos[0])**2 + (prey1_pos[1] - hunter_pos[1])**2)
        if prey2_pos is not None:
            distance_prey2_to_hunter = sqrt((prey2_pos[0] - hunter_pos[0])**2 + (prey2_pos[1] - hunter_pos[1])**2)

        if (self.name == 'prey1' and distance_prey1_to_hunter <= distance_prey2_to_hunter) or \
           (self.name == 'prey2' and distance_prey2_to_hunter < distance_prey1_to_hunter):
            return self.alive_strategy_action(state)
        else:
            return self.runner_strategy_action(state)

    def calculate_new_position(self, current_position, move, grid_size):
        new_position = current_position[:]
        if move == 'up' and current_position[1] > 0:
            new_position[1] -= 1
        elif move == 'down' and current_position[1] < grid_size - 1:
            new_position[1] += 1
        elif move == 'left' and current_position[0] > 0:
            new_position[0] -= 1
        elif move == 'right' and current_position[0] < grid_size - 1:
            new_position[0] += 1
        else:
            return None
        return new_position

    def is_safe_move(self, prey_pos, move, hunter_pos, obstacles, grid_size):
        new_position = self.calculate_new_position(prey_pos, move, grid_size)
        if new_position is None or tuple(new_position) in obstacles:
            return False

        distance_to_hunter = sqrt((new_position[0] - hunter_pos[0])**2 + (new_position[1] - hunter_pos[1])**2)
        return distance_to_hunter > 1

    def is_safe_move_from_obstacle(self, prey_pos, obstacles, grid_size):
        valid_moves = []
        
        if prey_pos is not None or tuple(prey_pos) not in obstacles:
            adjacent_positions = [
                {(prey_pos[0], prey_pos[1] - 1): 'up'},  
                {(prey_pos[0], prey_pos[1] + 1): 'down'},  
                {(prey_pos[0] - 1, prey_pos[1]): 'left'},  
                {(prey_pos[0] + 1, prey_pos[1]): 'right'}   
            ]
            for pos in adjacent_positions:
                pos_tuple = utils.convert_dicKeys_to_tuple(pos)
                if pos_tuple not in obstacles:
                    if pos not in self.previous_move_list and pos not in valid_moves:
                        valid_moves.append(pos)      
            return utils.extrair_valores(valid_moves)

    def is_adjacent_to_obstacle(self, prey_pos, obstacles):
        adjacent_positions = [
            (prey_pos[0], prey_pos[1] - 1),  
            (prey_pos[0], prey_pos[1] + 1),  
            (prey_pos[0] - 1, prey_pos[1]),  
            (prey_pos[0] + 1, prey_pos[1])   
        ]
        for pos in adjacent_positions:
            if pos in obstacles:
                return True  

        return False

    def is_in_corner(self, pos, grid_size):
        if pos[0] == 0 and pos[1] == 0:
            return True
        if pos[0] == 0 and pos[1] == grid_size - 1:
            return True
        if pos[0] == grid_size - 1 and pos[1] == 0:
            return True
        if pos[0] == grid_size - 1 and pos[1] == grid_size - 1:
            return True
        return False
