import random
import utils

class PreyAgent:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.initial_move_completed = False  # Flag to track if the initial movement is completed
        self.previous_move_list = []
        self.initial_move_counter = 0
        self.previous_move = None
        self.recent_positions = []  # List to track recently visited positions
        self.recent_positions_limit = 5  # Limit on how many recent positions to track

    def choose_action(self, state):
        print(self.strategy)
        if self.strategy == "runner":
            print("GAU")
            return self.runner_strategy_action(state)
        elif self.strategy == "alive":
            return self.alive_strategy_action(state)
    
    def runner_strategy_action(self, state):
        prey_pos = state[f'{self.name}_pos']
        hunter_pos = state['hunter_pos']
        end_pos = state['end_pos']
        obstacles = state['obstacles']
        grid_size = state['grid_size']
        
    
        # Determine the possible moves
        possible_moves = ['up', 'down', 'left', 'right']
        best_move = None
        min_distance = float('inf')

        if not self.initial_move_completed:
            desired_move = 'left' if self.name == 'prey1' else 'right'
            if desired_move in possible_moves:
                self.initial_move_counter += 1
                if self.initial_move_counter <= 5:  # Adjust the number of steps allowed towards the desired direction
                    return desired_move, None, None  # Move directly towards the desired side
                else:
                    self.initial_move_completed = True

        # Once the initial movement is completed, apply the regular strategy
        for move in possible_moves:
            new_position = self.calculate_new_position(prey_pos, move, grid_size)
            if new_position and tuple(new_position) not in obstacles and new_position not in self.recent_positions:
                distance_to_end = abs(new_position[0] - end_pos[0]) + abs(new_position[1] - end_pos[1])
                distance_to_hunter = abs(new_position[0] - hunter_pos[0]) + abs(new_position[1] - hunter_pos[1])

                # Prefer moves that bring the prey closer to the end and farther from the hunter
                if distance_to_end < min_distance and distance_to_hunter > 1:
                    min_distance = distance_to_end
                    best_move = move

        if self.is_adjacent_to_obstacle(prey_pos, obstacles):
            # If no best move is found, move away from nearby obstacles
            safe_moves_from_obstacle = self.is_safe_move_from_obstacle(prey_pos, obstacles, grid_size)
            for move in safe_moves_from_obstacle:
                if move not in self.previous_move_list:
                    self.previous_move_list.append(move)
                    self.previous_move = best_move
                    best_move = move
                    break

        if best_move is None:
            # If no best move is found, move randomly to avoid being caught
            safe_moves = [move for move in possible_moves if self.is_safe_move(prey_pos, move, hunter_pos, obstacles, grid_size)]
            best_move = random.choice(safe_moves) if safe_moves else None

        # Update recent positions
        new_position = self.calculate_new_position(prey_pos, best_move, grid_size)
        if new_position:
            self.recent_positions.append(new_position)
            if len(self.recent_positions) > self.recent_positions_limit:
                self.recent_positions.pop(0)  # Remove the oldest position if limit exceeded

        print(f'{self.name} best move: {best_move}')
        return best_move, None, None

    def alive_strategy_action(self, state):
        prey_pos = state[f'{self.name}_pos']
        hunter_pos = state['hunter_pos']
        obstacles = state['obstacles']
        grid_size = state['grid_size']

        # Determine the possible moves
        possible_moves = ['up', 'down', 'left', 'right']
        best_move = None
        max_distance_to_hunter = float('-inf')

        if not self.initial_move_completed:
            desired_move = 'left' if self.name == 'prey1' else 'right'
            if desired_move in possible_moves:
                self.initial_move_counter += 1
                if self.initial_move_counter <= 5:  # Adjust the number of steps allowed towards the desired direction
                    return desired_move, None, None  # Move directly towards the desired side
                else:
                    self.initial_move_completed = True

        # Calculate distances to hunter for possible moves
        for move in possible_moves:
            new_position = self.calculate_new_position(prey_pos, move, grid_size)
            if new_position and tuple(new_position) not in obstacles and new_position not in self.recent_positions:
                distance_to_hunter = abs(new_position[0] - hunter_pos[0]) + abs(new_position[1] - hunter_pos[1])

                # Prefer moves that increase the distance from the hunter
                if distance_to_hunter > max_distance_to_hunter:
                    max_distance_to_hunter = distance_to_hunter
                    best_move = move

        if best_move is None or self.is_adjacent_to_obstacle(prey_pos, obstacles):
            # If no best move is found or the prey is adjacent to an obstacle, move away from nearby obstacles
            safe_moves_from_obstacle = self.is_safe_move_from_obstacle(prey_pos, obstacles, grid_size)
            for move in safe_moves_from_obstacle:
                new_position = self.calculate_new_position(prey_pos, move, grid_size)
                if new_position and tuple(new_position) not in self.previous_move_list:
                    self.previous_move_list.append(new_position)
                    best_move = move
                    break

        if best_move is None:
            # If no best move is found, move randomly to avoid being caught
            safe_moves = [move for move in possible_moves if self.is_safe_move(prey_pos, move, hunter_pos, obstacles, grid_size)]
            best_move = random.choice(safe_moves) if safe_moves else None

        # Update recent positions
        new_position = self.calculate_new_position(prey_pos, best_move, grid_size)
        if new_position:
            self.recent_positions.append(new_position)
            if len(self.recent_positions) > self.recent_positions_limit:
                self.recent_positions.pop(0)  # Remove the oldest position if limit exceeded

        print(f'{self.name} best move: {best_move}')
        return best_move, None, None
    
    #def killer_strategy_action(self,state):
        
    
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

        distance_to_hunter = abs(new_position[0] - hunter_pos[0]) + abs(new_position[1] - hunter_pos[1])
        return distance_to_hunter > 1
    
    def is_safe_move_from_obstacle(self, prey_pos, obstacles, grid_size):
        valid_moves = []
        
        if prey_pos is not None or tuple(prey_pos) not in obstacles:
            adjacent_positions = [
                {(prey_pos[0], prey_pos[1] - 1): 'up'},  # Up
                {(prey_pos[0], prey_pos[1] + 1): 'down'},  # Down
                {(prey_pos[0] - 1, prey_pos[1]): 'left'},  # Left
                {(prey_pos[0] + 1, prey_pos[1]): 'right'}   # Right
            ]
            print(f'{self.name} prey position: {prey_pos}')
            for pos in adjacent_positions:
                pos_tuple = utils.convert_dicKeys_to_tuple(pos)
                if pos_tuple not in obstacles:
                    if pos not in self.previous_move_list and pos not in valid_moves:
                        valid_moves.append(pos)      
            return utils.extrair_valores(valid_moves)

    def is_adjacent_to_obstacle(self, prey_pos, obstacles):
        adjacent_positions = [
            (prey_pos[0], prey_pos[1] - 1),  # Up
            (prey_pos[0], prey_pos[1] + 1),  # Down
            (prey_pos[0] - 1, prey_pos[1]),  # Left
            (prey_pos[0] + 1, prey_pos[1])   # Right
        ]
        for pos in adjacent_positions:
            if pos in obstacles:
                return True  # Player is adjacent to an obstacle

        return False
