import pygame
import sys
import random
import argparse
from QLearningAgent import QLearningAgent
from preyAgent import PreyAgent
from hunterAgent import HunterAgent
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from randomAgent import RandomAgent

# Constants
GRID_SIZE = 30
CELL_SIZE = 20
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
FPS = 1000

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
parser.add_argument('--prey1_strategy', type=str, choices=["runner", "killer", "alive", "random","mixed"], required=True, help='Strategy for prey1')
parser.add_argument('--prey2_strategy', type=str, choices=["runner", "killer", "alive", "random","mixed"], required=True, help='Strategy for prey2')
args = parser.parse_args()

# Initialize agents based on user input
if args.prey1_strategy == random and args.prey2_strategy == random:
    prey1_agent = RandomAgent('prey1')
    prey2_agent = RandomAgent('prey2')
else:
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
    if position is None:
        return
    new_position = position[:]
    if direction == 'up':
        new_position[1] -= 1
    elif direction == 'down':
        new_position[1] += 1
    elif direction == 'left':
        new_position[0] -= 1
    elif direction == 'right':
        new_position[0] += 1

    if is_within_bounds(new_position) and is_not_obstacle(new_position):
        position[:] = new_position

def is_adjacent_to_hunter(prey_pos, hunter_pos):
        if prey_pos is None or hunter_pos is None:
            return False
        adjacent_positions = [
            (hunter_pos[0], hunter_pos[1] - 1),
            (hunter_pos[0], hunter_pos[1] + 1),
            (hunter_pos[0] - 1, hunter_pos[1]),
            (hunter_pos[0] + 1, hunter_pos[1])
        ]
        return tuple(prey_pos) in adjacent_positions or tuple(prey_pos) == tuple(hunter_pos)

def check_win_conditions():
    global hunter_pos, prey1_active, prey2_active, prey1_pos, prey2_pos, hunter_active, prey1_reach, prey2_reach, end_pos, prey1_dead, prey2_dead

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



def reset_game_state():
    global prey1_pos, prey2_pos, hunter_pos, end_pos, prey1_active, prey2_active, hunter_active
    global combined_prey_active, combined_prey_pos, prey1_reach, prey2_reach, prey1_dead, prey2_dead
    prey1_pos = [0, 0]
    prey2_pos = [0, GRID_SIZE - 1]
    hunter_pos = [GRID_SIZE - 1, GRID_SIZE // 2]
    end_pos = [GRID_SIZE - 1, GRID_SIZE // 2]
    prey1_active = True
    prey2_active = True
    hunter_active = True
    combined_prey_active = False
    combined_prey_pos = None
    prey1_reach = False
    prey2_reach = False
    prey1_dead = False
    prey2_dead = False
    obstacles.clear()
    obstacles.extend(generate_random_obstacles(NUM_OBSTACLES, GRID_SIZE))

def game_loop():
    global prey1_active, prey2_active, hunter_active, prey1_reach, prey2_reach, prey1_dead, prey2_dead, combined_prey_active
    combined_prey_pos = None
    running = True
    start_time = pygame.time.get_ticks()
    time_limit = 30 * 1000  # 30 seconds in milliseconds
    frames_ran = 0
    frames_limit = 200
    prey1moves = 0
    prey2moves = 0
    huntermoves = 0
    combinedPreyMoves = 0

    while running:
        frames_ran+=1
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time >= time_limit:
            print("Time's up! Game over.")
            running = False
        
        if frames_ran >= frames_limit:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_grid()
        if not combined_prey_active and prey1_active:
            draw_player(prey1_pos, GREEN)
        if not combined_prey_active and prey2_active:
            draw_player(prey2_pos, BLUE)
        if combined_prey_active:
            draw_player(state['combined_prey_pos'], PURPLE)
        draw_player(hunter_pos, RED)
        draw_player(end_pos, BLACK)
        draw_obstacles()

        state = get_game_state()
        
        if prey1_active and prey2_active and prey1_pos == prey2_pos:
            combined_prey_active = True
            prey1_active = False
            prey2_active = False
        
        if args.prey1_strategy == 'killer' and args.prey2_strategy == 'killer' and combined_prey_active:
            combined_prey_action, _, _ = prey1_agent.choose_action(state)
            move_player(state['combined_prey_pos'], combined_prey_action, combined_prey_active)
            combinedPreyMoves += 1
            if is_adjacent_to_hunter(state['combined_prey_pos'], hunter_pos):
                remove_player('hunter')
                hunter_active = False
                print("Combined prey has caught the hunter!")
                running = False

        else:
            if prey1_active:
                prey1_action, _, _ = prey1_agent.choose_action(state)
                move_player(prey1_pos, prey1_action, prey1_active)
                prey1moves += 1

            if prey2_active:
                prey2_action, _, _ = prey2_agent.choose_action(state)
                move_player(prey2_pos, prey2_action, prey2_active)
                prey2moves += 1
                
        if hunter_active:
            hunter_action, _, _ = hunter_agent.choose_action(state)
            move_player(hunter_pos, hunter_action, hunter_active)
            huntermoves += 1
            if is_adjacent_to_hunter(prey1_pos,hunter_pos):
                print("Hunter has caught Prey 1!")
                prey1_dead = True
                prey1_active = False
                remove_player('prey1')
            if is_adjacent_to_hunter(prey2_pos,hunter_pos):
                print("Hunter has caught Prey 2!")
                prey2_dead = True
                prey2_active = False
                remove_player('prey2')

        if not check_win_conditions():
            running = False
        

        pygame.display.flip()
        clock.tick(FPS)

        hunterwins = 0
        onepreysurvives = 0
        preywins = 0
        combined_prey_wins = 0
        print("##########################################")
        print("PREY1")
        print("Prey 1 dead: ", prey1_dead)
        print("Prey 1 pos: ", prey1_pos)
        print("Prey 1 active: ", prey1_active)
        print("Prey 1 reach: ", prey1_reach)
        print("PREY2")
        print("Prey 2 dead: ", prey2_dead)
        print("Prey 2 pos: ", prey2_pos)
        print("Prey 2 active: ", prey2_active)
        print("Prey 2 reach: ", prey2_reach)
        print("##########################################")
        if not prey1_dead and not prey2_dead and not combined_prey_active:
            preywins = 1
        elif prey1_reach or prey2_reach:
            onepreysurvives = 1
        elif not hunter_active and combined_prey_active:
            combined_prey_wins = 1
        else: 
            hunterwins = 1

    return (prey1moves, prey2moves, huntermoves, preywins, onepreysurvives, hunterwins, combined_prey_wins, combinedPreyMoves)

if __name__ == "__main__":
    data = (0,0,0,0,0,0,0,0)
    stepsprey1 = []
    stepsprey2 = []
    stepshunter = []
    stepsCombinedPrey = []

    for i in range(100):
        run = game_loop()
        data = tuple(map(lambda i, j: i + j, data, run))
        stepsprey1 += [run[0]]
        stepsprey2 += [run[1]]
        stepshunter += [run[2]]
        stepsCombinedPrey += [run[7]]

        reset_game_state()

    print(data)
    print("prey1moves =", data[0], "prey2moves =", data[1], "huntermoves =", data[2], "preywins =", data[3], "onepreysurvives =", data[4], "hunterwins =", data[5], "combined_prey_wins =", data[6], "combined_prey_moves =", data[7])

    # Prepare the data for moves
    moves_data = {
        'Character': ['Prey1', 'Prey2', 'Hunter', 'Combined Prey'],
        'Moves': [data[0], data[1], data[2], data[7]]
    }

    moves_df = pd.DataFrame(moves_data)

    # Create the bar plot for moves
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 6))
    moves_plot = sns.barplot(x='Character', y='Moves', data=moves_df, palette='viridis', hue="Character", legend=False)

    # Add the exact numbers on the bars
    for index, value in enumerate(moves_df['Moves']):
        plt.text(index, value + 1, str(value), ha='center')

    moves_plot.set_title('Moves of Characters')
    plt.savefig(f'moves_plot_{args.prey1_strategy}.png')  # Save the plot as a PNG file
    plt.close()

    # Prepare the data for wins
    wins_data = {
        'Outcome': ['Prey Wins', 'One Prey Survives', 'Hunter Wins', 'Combined Prey Wins'],
        'Count': [data[3], data[4], data[5], data[6]]
    }

    wins_df = pd.DataFrame(wins_data)

    # Create the bar plot for wins
    plt.figure(figsize=(8, 6))
    wins_plot = sns.barplot(x='Outcome', y='Count', data=wins_df, palette='viridis', hue="Outcome", legend=False)

    # Add the exact numbers on the bars
    for index, value in enumerate(wins_df['Count']):
        plt.text(index, value + 0.05, str(value), ha='center')

    wins_plot.set_title('Game Outcomes')
    plt.savefig(f'wins_plot_{args.prey1_strategy}.png')  # Save the plot as a PNG file
    plt.close()


    if (args.prey1_strategy == 'alive' and args.prey2_strategy == 'alive') or (args.prey1_strategy == 'runner' and args.prey2_strategy == 'runner') or (args.prey1_strategy == 'random' and args.prey2_strategy == 'random') or (args.prey1_strategy == 'mixed' and args.prey2_strategy == 'mixed'):
        # Plot the data
        agent_steps = {
            'Prey 1': stepsprey1,
            'Prey 2': stepsprey2,
            'Hunter': stepshunter
        }
        
    elif args.prey1_strategy == 'killer' and args.prey2_strategy == 'killer':
        agent_steps = {
            'Prey 1': stepsprey1,
            'Prey 2': stepsprey2,
            'Hunter': stepshunter,
            'Combined Prey': stepsCombinedPrey
        }
        

    avg_steps = {agent: sum(steps) / len(steps) for agent, steps in agent_steps.items()}
    errors = {agent: (max(steps) - min(steps)) / 2 for agent, steps in agent_steps.items()}

    fig, ax = plt.subplots()
    bars = ax.bar(avg_steps.keys(), avg_steps.values(), yerr=errors.values(), capsize=5, color=['green', 'blue', 'red'])

    ax.set_ylabel('Avg. Steps Per Episode')
    ax.set_title('Average Steps Per Episode for Each Agent')

    for bar, steps in zip(bars, avg_steps.values()):
        height = bar.get_height()
        ax.annotate(f'{steps:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    plt.savefig(f'wins_plot_again_{args.prey1_strategy}.png')  # Save the plot as a PNG file
    plt.close()

