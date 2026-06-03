import os
import pygame as pg
import configparser
import random

# Get the directory of the game
GAME_DIR = os.path.dirname(os.path.abspath(__file__))

# Read configuration file using built-in ini parser
config = configparser.ConfigParser()
config.read(os.path.join(GAME_DIR, "config.ini"))

# Display settings
WIDTH   = config.getint("display", "width", fallback=600)
HEIGHT  = config.getint("display", "height", fallback=400)
BACKGROUND_COLOR = tuple(int(x) for x in config.get(
    "display", "background_color", fallback="0, 0, 0"
).split(","))

# Gameplay settings
SPEED = config.getfloat("gameplay", "speed", fallback=3.0)  # Cells per second
RENDER_DISTANCE = config.getint("gameplay", "render_distance", fallback=2)
GUARD_RENDER_DISTANCE = config.getfloat("gameplay", "guard_render_distance", fallback=3.0)
GUARD_CATCH_RANGE = config.getfloat("gameplay", "guard_catch_range", fallback=0.5)

# Simulation settings
FPS = config.getint("simulation", "fps", fallback=60)
DT_MAX = config.getfloat("simulation", "dt_max", fallback=0.1)

def load_maze(filename):
    maze = []
    with open(os.path.join(GAME_DIR, filename)) as f:
        for line in f:
            line = line.rstrip("\n")
            maze.append(list(line))
    
    guard_positions = []
    player_pos = (0, 0)
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "G":
                guard_positions.append((x, y))
                maze[y][x] = " "
            elif char == "P":
                player_pos = (x, y)
                maze[y][x] = " "

    return maze, guard_positions, player_pos

# Modifies the maze list in-place (no return needed since lists are mutable)
def reveal_maze(maze, player_pos):
    x, y = player_pos
    grid_x = round(x)
    grid_y = round(y)
    for dy in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
        for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            idx_y = grid_y + dy
            idx_x = grid_x + dx

            if 0 <= idx_y < len(maze) and 0 <= idx_x < len(maze[idx_y]):
                if maze[idx_y][idx_x] == "#":
                    maze[idx_y][idx_x] = "*"
                elif maze[idx_y][idx_x] == "D":
                    maze[idx_y][idx_x] = "d"
                elif maze[idx_y][idx_x] == "K":
                    maze[idx_y][idx_x] = "k"

# Converts the world coordinate system (maze coordinates) to screen coordinates
def screen_pos(maze_pos):
    x, y = maze_pos
    return round(x * tile_size), round(y * tile_size)

def draw_maze(screen, maze):
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "*":
                screen.blit(brick, screen_pos((x, y)))  # Pass the top-left coordinates directly instead of using a rect
            elif char == "d":
                screen.blit(door, screen_pos((x, y)))
            elif char == "k":
                screen.blit(gold_key, screen_pos((x, y)))

def move(old_position, direction, speed, dt):
    if direction == (0, 0):
        return old_position

    x, y = old_position
    direction_x, direction_y = direction

    new_x = round(x) if direction_x == 0 else x + direction_x * speed * dt
    new_y = round(y) if direction_y == 0 else y + direction_y * speed * dt

    return new_x, new_y

def check_wall(maze, position, direction, can_open_door):
    x, y = position
    direction_x, direction_y = direction

    boundary_x = round(x + direction_x * 0.5)
    boundary_y = round(y + direction_y * 0.5)
    target_cell = maze[boundary_y][boundary_x]

    # Return True for a wall or a door without a key
    return target_cell in "#*" or (target_cell in "Dd" and not can_open_door)

def random_direction():
    direction = random.choice([
        (1, 0),   # right
        (-1, 0),  # left
        (0, 1),   # down
        (0, -1)   # up
    ])
    return direction

def guard_move(maze, position, direction, speed, dt):
    while check_wall(maze, position, direction, False):
        direction = random_direction()

    position = move(position, direction, speed, dt)

    return position, direction

def draw_guard(screen, guard_pos, player_pos):
    if abs(player_pos[0] - guard_pos[0]) < GUARD_RENDER_DISTANCE \
        and abs(player_pos[1] - guard_pos[1]) < GUARD_RENDER_DISTANCE:
        screen.blit(guard, screen_pos(guard_pos))

def guard_collision(player_pos, guard_pos):
    player_x, player_y = player_pos
    guard_x, guard_y = guard_pos

    distance_squared = ((player_x - guard_x)**2 + (player_y - guard_y)**2)
    return distance_squared < GUARD_CATCH_RANGE**2

def end_game(screen, text, color):
        font = pg.font.Font(None, HEIGHT // 5)  # Creates a font object with default font and size height // 5
        text = font.render(text, True, color, "black")  # Creates a text surface object (True for anti-aliasing)
        textrect = text.get_rect()
        textrect.center = (WIDTH // 2, HEIGHT //2)

        screen.blit(text, textrect)
        pg.display.flip()

        pg.time.wait(2000)
        return False

if __name__ == "__main__":
    # Initialise the PyGame environment
    pg.init()

    # Set the PyGame window title
    pg.display.set_caption("Castle Escape - AE1205")

    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # Load all assets
    brick     = pg.image.load(os.path.join(GAME_DIR, "brick.png"))
    brick_lit = pg.image.load(os.path.join(GAME_DIR, "brick_lit.png"))
    door      = pg.image.load(os.path.join(GAME_DIR, "door.png"))
    gold_key  = pg.image.load(os.path.join(GAME_DIR, "gold_key.png"))
    guard     = pg.image.load(os.path.join(GAME_DIR, "guard.png"))
    player    = pg.image.load(os.path.join(GAME_DIR, "player.png"))

    maze, guard_positions, player_pos = load_maze("maze1.txt")
    reveal_maze(maze, player_pos)

    max_y = len(maze)
    max_x = len(maze[0])
    scale_y = HEIGHT // max_y
    scale_x = WIDTH // max_x

    tile_size = min(scale_x, scale_y)

    brick     = pg.transform.scale(brick, (tile_size, tile_size))
    brick_lit = pg.transform.scale(brick_lit, (tile_size, tile_size))
    door      = pg.transform.scale(door, (tile_size, tile_size))
    gold_key  = pg.transform.scale(gold_key, (tile_size, tile_size))
    guard     = pg.transform.scale(guard, (tile_size, tile_size))
    player    = pg.transform.scale(player, (tile_size, tile_size))

    guard_directions = [random_direction() for _ in guard_positions]

    # Used for variable dt with an FPS cap
    # Because the player moves at a constant velocity, a higher dt resulting from slowdowns doesn't affect the movement speed
    # However, dt_max is implemented to avoid potential collision detection issues
    clock = pg.time.Clock()
    running = True
    dt = 0
    has_key = False

    while running:
        for event in pg.event.get():
            # Check if the user clicked the window's close button
            if event.type == pg.QUIT:
                running = False
            # Check if a key was pressed on the keyboard
            elif event.type == pg.KEYDOWN:
                # Check if the specific key pressed was the Escape key
                if event.key == pg.K_ESCAPE:
                    running = False

        keys = pg.key.get_pressed()  # pg.event.get() already pumps the event queue

        if keys[pg.K_UP]:
            direction = (0, -1)
        elif keys[pg.K_DOWN]:
            direction = (0, 1)
        elif keys[pg.K_LEFT]:
            direction = (-1, 0)
        elif keys[pg.K_RIGHT]:
            direction = (1, 0)
        else:
            direction = (0, 0)

        if not check_wall(maze, player_pos, direction, has_key):
            player_pos = move(player_pos, direction, SPEED, dt)

        reveal_maze(maze, player_pos)

        x, y = player_pos
        grid_x, grid_y = round(x), round(y)
        if maze[grid_y][grid_x].lower() == "k":
            has_key = True
            maze[grid_y][grid_x] = " "

        if maze[grid_y][grid_x].lower() == "d" and has_key:
            running = end_game(screen, "You escaped!", (255, 215, 0))

        # Drawing routine
        screen.fill(BACKGROUND_COLOR)
        draw_maze(screen, maze)
        screen.blit(player, screen_pos(player_pos))

        for idx, pos in enumerate(guard_positions):
            direction = guard_directions[idx]
            new_pos, new_direction = guard_move(maze, pos, direction, SPEED, dt)
            guard_positions[idx] = new_pos
            guard_directions[idx] = new_direction
            draw_guard(screen, new_pos, player_pos)
            if guard_collision(player_pos, new_pos):
                running = end_game(screen, "You were caught!", (138, 7, 7))

        pg.display.flip()

        dt = clock.tick(FPS) / 1000  # Limits FPS and returns the elapsed time since the last frame in seconds
        dt = min(dt, DT_MAX)  # Prevents large dt if there's a significant slowdown/freeze

    # Close the game window and properly clean up
    pg.quit()
