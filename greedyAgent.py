import random

class GreedyAgent:
    def __init__(self, role):
        self.role = role

    def choose_action(self, state):
        if self.role == 'prey1' or self.role == 'prey2':
            return self._choose_prey_action(state)
        elif self.role == 'hunter':
            return self._choose_hunter_action(state)

    def _choose_prey_action(self, state):
        prey_pos = state[f'{self.role}_pos']
        end_pos = state['end_pos']
        hunter_pos = state['hunter_pos']
        other_prey_pos = state['prey2_pos'] if self.role == 'prey1' else state['prey1_pos']
        
        # Check if preys can team up to take down the hunter
        if self._can_team_up_to_take_down_hunter(prey_pos, other_prey_pos, hunter_pos):
            return 'attack', 0, 0

        directions = ['up', 'down', 'left', 'right']
        best_direction = random.choice(directions)  # Default to a random choice
        min_distance = float('inf')

        for direction in directions:
            new_pos = self._get_new_position(prey_pos, direction)
            if self._is_valid_position(new_pos):
                distance = self._calculate_distance(new_pos, end_pos)
                if distance < min_distance and new_pos != hunter_pos:
                    min_distance = distance
                    best_direction = direction

        return best_direction, 0, 0

    def _choose_hunter_action(self, state):
        hunter_pos = state['hunter_pos']
        prey1_pos = state['prey1_pos']
        prey2_pos = state['prey2_pos']
        prey1_active = state['prey1_active']
        prey2_active = state['prey2_active']

        directions = ['up', 'down', 'left', 'right']
        best_direction = random.choice(directions)  # Default to a random choice
        min_distance = float('inf')

        for direction in directions:
            new_pos = self._get_new_position(hunter_pos, direction)
            if self._is_valid_position(new_pos):
                if prey1_active:
                    distance = self._calculate_distance(new_pos, prey1_pos)
                    if distance < min_distance:
                        min_distance = distance
                        best_direction = direction
                if prey2_active:
                    distance = self._calculate_distance(new_pos, prey2_pos)
                    if distance < min_distance:
                        min_distance = distance
                        best_direction = direction

        return best_direction, 0, 0

    def _can_team_up_to_take_down_hunter(self, prey_pos, other_prey_pos, hunter_pos):
        if not prey_pos or not other_prey_pos or not hunter_pos:
            return False

        # Check if both preys are within 3 blocks of the hunter
        distance_to_hunter = self._calculate_distance(prey_pos, hunter_pos)
        distance_to_hunter_other_prey = self._calculate_distance(other_prey_pos, hunter_pos)
        
        return distance_to_hunter <= 3 and distance_to_hunter_other_prey <= 3

    def _get_new_position(self, position, direction):
        if direction == 'up':
            return [position[0], position[1] - 1]
        elif direction == 'down':
            return [position[0], position[1] + 1]
        elif direction == 'left':
            return [position[0] - 1, position[1]]
        elif direction == 'right':
            return [position[0] + 1, position[1]]

    def _is_valid_position(self, position):
        return 0 <= position[0] < 30 and 0 <= position[1] < 30

    def _calculate_distance(self, pos1, pos2):
        if pos1 is None or pos2 is None:
            return float('inf')  # Return a very high distance if one of the positions is None
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
