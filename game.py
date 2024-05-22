import pygame
import sys
import random
import argparse
from QLearningAgent import QLearningAgent
from preyAgent import PreyAgent
from hunterAgent import HunterAgent
from randomAgent import RandomAgent

# Constants
GRID_SIZE = 30
CELL_SIZE = 20
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)

# Number of obstacles
NUM_OBSTACLES = 50

# Initialize Pygame
pygame.init()

# Argument parser setup
parser = argparse.ArgumentParser(description="Prey and Hunter Game")
parser.add_argument('--prey1_strategy', type=str, choices=["runner", "killer", "alive"], required=True, help='Strategy for prey1')
parser.add_argument('--prey2_strategy', type=str, choices=["runner", "killer", "alive"], required=True, help='Strategy for prey2')
args = parser.parse_args()

# Initialize agents based on user input
prey1_agent = PreyAgent('prey1', args.prey1_strategy)
prey2_agent = PreyAgent('prey2', args.prey2_strategy)
hunter_agent = HunterAgent()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()

# Set initial positions
prey1_pos = [0, 0]
prey2_pos = [0, GRID_SIZE - 1]
hunter_pos = [GRID_SIZE - 1, GRID_SIZE // 2]
end_pos = [GRID_SIZE - 1, GRID_SIZE // 2]

# Active status
prey1_active = True
prey2_active = True
hunter_active = True
combined_prey_active = False

# Reach status
prey1_reach = False
prey2_reach = False

# Dead status
prey1_dead = False
prey2_dead = False

# Function to generate random obstacles
def generate_random_obstacles(num_obstacles, grid_size):
    obstacles = set()
    while len(obstacles) < num_obstacles:
        x = random.randint(1, grid_size - 1)
        y = random.randint(1, grid_size - 2)
        if (x, y) not in obstacles and (x, y) not in [tuple(prey1_pos), tuple(prey2_pos), tuple(hunter_pos), tuple(end_pos)]:
            obstacles.add((x, y))
    return list(obstacles)

# Generate obstacles
obstacles = generate_random_obstacles(NUM_OBSTACLES, GRID_SIZE)

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

def draw_player(position, color):
    if position is not None:
        rect = pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)

def draw_obstacles():
    for obstacle in obstacles:
        rect = pygame.Rect(obstacle[0] * CELL_SIZE, obstacle[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GRAY, rect)

def is_within_bounds(position):
    return 0 <= position[0] < GRID_SIZE and 0 <= position[1] < GRID_SIZE

def is_not_obstacle(position):
    return tuple(position) not in obstacles

def move_player(position, direction, active):
    if not active:
        return
    print(f"Moving player {position} {direction}")
    new_position = position[:]
    if direction == 'up':
        new_position[1] -= 1
    elif direction == 'down':
        new_position[1] += 1
    elif direction == 'left':
        new_position[0] -= 1
    elif direction == 'right':
        new_position[0] += 1
    print(f"New position: {new_position}")

    if is_within_bounds(new_position) and is_not_obstacle(new_position):
        position[:] = new_position

def is_adjacent_to_hunter(prey_pos, hunter_pos):
        adjacent_positions = [
            (hunter_pos[0], hunter_pos[1] - 1),  # Up
            (hunter_pos[0], hunter_pos[1] + 1),  # Down
            (hunter_pos[0] - 1, hunter_pos[1]),  # Left
            (hunter_pos[0] + 1, hunter_pos[1])   # Right
        ]
        
        return tuple(prey_pos) in adjacent_positions

def check_win_conditions(prey1_pos, prey2_pos, hunter_active, prey1_reach, prey2_reach, end_pos, prey1_dead, prey2_dead, combined_prey_pos):
    global hunter_pos, prey1_active, prey2_active

    # Check if prey1 reaches the endpoint
    if prey1_pos == end_pos and not prey1_reach:
        print("Prey 1 has reached the endpoint!")
        prey1_reach = True
        prey1_active = False

    # Check if prey2 reaches the endpoint
    if prey2_pos == end_pos and not prey2_reach:
        print("Prey 2 has reached the endpoint!")
        prey2_reach = True
        prey2_active = False

    # Check if both preys reach the endpoint
    if prey1_reach and prey2_reach:
        print("Both preys have reached the endpoint! Game over.")
        return False

    if prey1_dead and prey2_reach:
        print("Prey 2 has reached the endpoint! Game over.")
        return False

    if prey2_dead and prey1_reach:
        print("Prey 1 has reached the endpoint! Game over.")
        return False

    # Check if hunter catches both preys
    if prey1_dead and prey2_dead and hunter_active:
        print("Hunter has caught both preys! Hunter wins!")
        return False

    return True

def get_game_state():
    return {
        'prey1_pos': prey1_pos,
        'prey2_pos': prey2_pos,
        'hunter_pos': hunter_pos,
        'end_pos': end_pos,
        'prey1_active': prey1_active,
        'prey2_active': prey2_active,
        'hunter_active': hunter_active,
        'prey1_reach': prey1_reach,
        'prey2_reach': prey2_reach,
        'obstacles': obstacles,
        'grid_size': GRID_SIZE,
        'combined_prey_active': combined_prey_active,
        'combined_prey_pos': None
    }

def remove_player(player):
    global prey1_pos, prey2_pos, hunter_pos, prey1_active, prey2_active, hunter_active
    if player == 'prey1':
        prey1_pos = None
        prey1_active = False
    elif player == 'prey2':
        prey2_pos = None
        prey2_active = False
    elif player == 'hunter':
        hunter_pos = None
        hunter_active = False

def hunter_catches_prey(hunter_pos, prey_pos):
    if prey_pos is None:
        return False
    return (
        (hunter_pos[0] == prey_pos[0] and abs(hunter_pos[1] - prey_pos[1]) == 1) or
        (hunter_pos[1] == prey_pos[1] and abs(hunter_pos[0] - prey_pos[0]) == 1)
    )

def game_loop():
    global prey1_active, prey2_active, hunter_active, prey1_reach, prey2_reach, prey1_dead, prey2_dead, combined_prey_active
    combined_prey_pos = None
    running = True
    start_time = pygame.time.get_ticks()
    time_limit = 30 * 1000  # 30 seconds in milliseconds
    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time >= time_limit:
            print("Time's up! Game over.")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_grid()
        if not combined_prey_active:
            draw_player(prey1_pos, GREEN)
            draw_player(prey2_pos, BLUE)
        else:
            draw_player(state['combined_prey_pos'], PURPLE)
        draw_player(hunter_pos, RED)
        draw_player(end_pos, BLACK)
        draw_obstacles()

        state = get_game_state()
        
        if prey1_active and prey2_active and prey1_pos == prey2_pos:
            combined_prey_active = True
            prey1_active = False
            prey2_active = False
            
        if combined_prey_active:
            combined_prey_action, _, _ = prey1_agent.choose_action(state)
            move_player(state['combined_prey_pos'], combined_prey_action, combined_prey_active)
            if is_adjacent_to_hunter(state['combined_prey_pos'], hunter_pos):
                remove_player('hunter')
                hunter_active = False
                print("Combined prey has caught the hunter!")
                running = False

        else:
            if prey1_active:
                prey1_action, _, _ = prey1_agent.choose_action(state)
                move_player(prey1_pos, prey1_action, prey1_active)

            if prey2_active:
                prey2_action, _, _ = prey2_agent.choose_action(state)
                move_player(prey2_pos, prey2_action, prey2_active)
                
        if hunter_active:
            hunter_action, _, _ = hunter_agent.choose_action(state)
            move_player(hunter_pos, hunter_action, hunter_active)
            if hunter_catches_prey(hunter_pos, prey1_pos):
                remove_player('prey1')
                print("Hunter has caught Prey 1!")
                prey1_dead = True
                prey1_active = False
            elif hunter_catches_prey(hunter_pos, prey2_pos):
                remove_player('prey2')
                print("Hunter has caught Prey 2!")
                prey2_dead = True
                prey2_active = False

        if not check_win_conditions(prey1_pos, prey2_pos, hunter_active, prey1_reach, prey2_reach, end_pos, prey1_dead, prey2_dead, combined_prey_pos):
            running = False

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game_loop()
