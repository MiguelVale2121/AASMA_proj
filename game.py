"""
To play the game Manually:
- Prey 1: W, A, S, D
- Prey 2: I, J, K, L
- Hunter: Arrow keys

Rules:
- Prey wins if they reach the endpoint.
- Hunter wins if they catch all the preys.
- Preys can team up to take down the hunter.
- Hunter loses if preys team up and catch the hunter.
- Preys lose if they are caught by the hunter.

"""


import pygame
import sys

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
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()

# Player and Endpoint
prey1_pos = [0, 0]  # Player 1 start position
prey2_pos  = [GRID_SIZE - 1, 0]  # Player 2 start position
hunter_pos = [0, GRID_SIZE - 1]  # Hunter start position
end_pos = [GRID_SIZE -1 , GRID_SIZE - 1]  # Central endpoint

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
    if check_opposite_sides(prey1_pos, prey2_pos, hunter_pos) and hunter_active:
        print("Preys have teamed up and taken down the hunter!")
        print("The hunter has lost!")
        hunter_active = False

    if prey1_pos == end_pos and not prey1_reach:
        print("Prey 1 has reached the endpoint!")
        prey1_reach = True
    if prey2_pos == end_pos and not prey2_reach:
        print("Prey 2 has reached the endpoint!")
        prey2_reach = True

    if (prey1_reach or prey2_reach) and (not prey1_active or not prey2_active):
        print("Remaining prey has reached the endpoint! Game over.")
        return False

    if not prey1_active and not prey2_active:
        print("Hunter has caught all preys! Hunter wins!")
        return False

    return True

def handle_player_movement(event):
    global prey1_pos, prey2_pos, hunter_pos
    # Prey 1 controls
    if prey1_active:
        if event.key == pygame.K_w:
            move_player(prey1_pos, 'up', prey1_active)
        elif event.key == pygame.K_s:
            move_player(prey1_pos, 'down', prey1_active)
        elif event.key == pygame.K_a:
            move_player(prey1_pos, 'left', prey1_active)
        elif event.key == pygame.K_d:
            move_player(prey1_pos, 'right', prey1_active)
    # Prey 2 controls
    if prey2_active:
        if event.key == pygame.K_i:
            move_player(prey2_pos, 'up', prey2_active)
        elif event.key == pygame.K_k:
            move_player(prey2_pos, 'down', prey2_active)
        elif event.key == pygame.K_j:
            move_player(prey2_pos, 'left', prey2_active)
        elif event.key == pygame.K_l:
            move_player(prey2_pos, 'right', prey2_active)
    # Hunter controls
    if hunter_active:
        if event.key == pygame.K_UP:
            move_player(hunter_pos, 'up', True)
        elif event.key == pygame.K_DOWN:
            move_player(hunter_pos, 'down', True)
        elif event.key == pygame.K_LEFT:
            move_player(hunter_pos, 'left', True)
        elif event.key == pygame.K_RIGHT:
            move_player(hunter_pos, 'right', True)

def game_loop():
    global prey1_active, prey2_active, hunter_active
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_player_movement(event)

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

        running = check_win_conditions(prey1_pos, prey2_pos, prey1_active, prey2_active,hunter_active, prey1_reach, prey2_reach, end_pos)
            
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
