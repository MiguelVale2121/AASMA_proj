import pygame
import sys
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

# Initialize Pygame
pygame.init()


prey1_agent = RandomAgent('prey')
prey2_agent = RandomAgent('prey')
hunter_agent = RandomAgent('hunter')
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()

# Player and Endpoint
prey1_pos = [0, 0]  # Player 1 start position
prey2_pos = [GRID_SIZE - 1, 0]  # Player 2 start position
hunter_pos = [GRID_SIZE // 2, GRID_SIZE - 2]  # Hunter start position
end_pos = [GRID_SIZE // 2, GRID_SIZE - 1]  # Central endpoint

# Active status
prey1_active = True
prey2_active = True
hunter_active = True

# Reach status
prey1_reach = False
prey2_reach = False

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

def draw_player(position, color):
    rect = pygame.Rect(position[0]*CELL_SIZE, position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def move_player(position, direction, active):
    if not active:
        return
    # Bounds checking and move the player
    if direction == 'up' and position[1] > 0:
        position[1] -= 1
    elif direction == 'down' and position[1] < GRID_SIZE - 1:
        position[1] += 1
    elif direction == 'left' and position[0] > 0:
        position[0] -= 1
    elif direction == 'right' and position[0] < GRID_SIZE - 1:
        position[0] += 1

def check_opposite_sides(pos1, pos2, hunter_pos):
    # Check horizontal opposition
    horizontal_opposition = (pos1[0] == hunter_pos[0] - 1 and pos2[0] == hunter_pos[0] + 1) or (pos1[0] == hunter_pos[0] + 1 and pos2[0] == hunter_pos[0] - 1)
    # Check vertical opposition
    vertical_opposition = (pos1[1] == hunter_pos[1] - 1 and pos2[1] == hunter_pos[1] + 1) or (pos1[1] == hunter_pos[1] + 1 and pos2[1] == hunter_pos[1] - 1)
    # Check diagonal opposition
    diagonal_opposition = (pos1[0] == hunter_pos[0] - 1 and pos1[1] == hunter_pos[1] - 1 and pos2[0] == hunter_pos[0] + 1 and pos2[1] == hunter_pos[1] + 1) or \
                          (pos1[0] == hunter_pos[0] + 1 and pos1[1] == hunter_pos[1] + 1 and pos2[0] == hunter_pos[0] - 1 and pos2[1] == hunter_pos[1] - 1)

    return horizontal_opposition or vertical_opposition or diagonal_opposition

def check_win_conditions(prey1_pos, prey2_pos, prey1_active, prey2_active, hunter_active, prey1_reach, prey2_reach, end_pos):
    global hunter_pos

    # Check if preys team up and take down the hunter
    if check_opposite_sides(prey1_pos, prey2_pos, hunter_pos) and hunter_active:
        print("Preys have teamed up and taken down the hunter!")
        print("The hunter has lost!")
        hunter_active = False
        return False

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

    # Check if hunter catches both preys
    if not prey1_active and not prey2_active:
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
        'prey2_reach': prey2_reach
    }

def game_loop():
    global prey1_active, prey2_active, hunter_active
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # Get the game state and let agents choose actions based on it
        state = get_game_state()

        if prey1_active:
            prey1_direction, _, _ = prey1_agent.choose_action(state)
            move_player(prey1_pos, prey1_direction, prey1_active)
        if prey2_active:
            prey2_direction, _, _ = prey2_agent.choose_action(state)
            move_player(prey2_pos, prey2_direction, prey2_active)
        if hunter_active:
            hunter_direction, _, _ = hunter_agent.choose_action(state)
            move_player(hunter_pos, hunter_direction, True)

        screen.fill(WHITE)
        draw_grid()
        if prey1_active:
            draw_player(prey1_pos, GREEN)
        if prey2_active:
            draw_player(prey2_pos, GREEN)
        if hunter_active:
            draw_player(hunter_pos, RED)
        draw_player(end_pos, BLUE)
        pygame.display.flip()

        # Check if hunter catches a prey
        if hunter_pos == prey1_pos:
            prey1_active = False
        if hunter_pos == prey2_pos:
            prey2_active = False

        running = check_win_conditions(prey1_pos, prey2_pos, prey1_active, prey2_active, hunter_active, prey1_reach, prey2_reach, end_pos)
            
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
