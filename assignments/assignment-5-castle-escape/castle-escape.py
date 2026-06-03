import os
import pygame as pg
import configparser
import time

# Get the directory of the game
game_dir = os.path.dirname(os.path.abspath(__file__))

# Read configuration file using built-in ini parser
config = configparser.ConfigParser()
config.read(os.path.join(game_dir, "config.ini"))

width   = config.getint("display", "width", fallback=600)
height  = config.getint("display", "height", fallback=400)
r, g, b = config.get("display", "background_color", fallback="0, 0, 0").split(",")
background_color = (int(r.strip()), int(g.strip()), int(b.strip()))

speed = config.getfloat("gameplay", "speed", fallback=3)  # Cells per second

fps = config.getint("simulation", "fps", fallback=60)
dt_max = config.getfloat("simulation", "dt_max", fallback=0.1)

# Initialise the PyGame environment
pg.init()

# Set the PyGame window title
pg.display.set_caption("Castle Escape - AE1205")

screen = pg.display.set_mode((width, height))

# Load all assets
brick     = pg.image.load(os.path.join(game_dir, "brick.png"))
brick_lit = pg.image.load(os.path.join(game_dir, "brick_lit.png"))
door      = pg.image.load(os.path.join(game_dir, "door.png"))
gold_key  = pg.image.load(os.path.join(game_dir, "gold_key.png"))
guard     = pg.image.load(os.path.join(game_dir, "guard.png"))
player    = pg.image.load(os.path.join(game_dir, "player.png"))

def load_maze(filename):
    maze = []
    with open(os.path.join(game_dir, filename)) as f:
        for line in f:
            line = line.rstrip("\n")
            maze.append(list(line))
    
    pos_guards = []
    pos_player = (0, 0)
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "G":
                pos_guards.append((x, y))
                maze[y][x] = " "
            elif char == "P":
                pos_player = (x, y)
                maze[y][x] = " "

    return maze, pos_guards, pos_player

# Lists are mutable, so calling this function modifies the caller's maze even without returning the maze
def reveal_maze(maze, pos_player):
    x, y = pos_player
    grid_x = round(x)
    grid_y = round(y)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            idx_y = grid_y + dy
            idx_x = grid_x + dx

            if 0 <= idx_y < len(maze) and 0 <= idx_x < len(maze[idx_y]):
                if maze[idx_y][idx_x] == "#":
                    maze[idx_y][idx_x] = "*"
                elif maze[idx_y][idx_x] == "D":
                    maze[idx_y][idx_x] = "d"
                elif maze[idx_y][idx_x] == "K":
                    maze[idx_y][idx_x] = "k"

def draw_maze(screen, maze):
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "*":
                screen.blit(brick, screen_pos((x, y)))  # Pass the top-left coordinates directly instead of using a rect
            elif char == "d":
                screen.blit(door, screen_pos((x, y)))
            elif char == "k":
                screen.blit(gold_key, screen_pos((x, y)))

maze, pos_guards, pos_player = load_maze("maze1.txt")

max_y = len(maze)
max_x = len(maze[0])
scale_y = height//max_y
scale_x = width//max_x

tile_size = min(scale_x, scale_y)

# Converts the world coordinate system (maze coordinates) to screen coordinates
def screen_pos(maze_pos):
    x, y = maze_pos
    return round(x * tile_size), round(y * tile_size)

brick     = pg.transform.scale(brick, (tile_size, tile_size))
brick_lit = pg.transform.scale(brick_lit, (tile_size, tile_size))
door      = pg.transform.scale(door, (tile_size, tile_size))
gold_key  = pg.transform.scale(gold_key, (tile_size, tile_size))
guard     = pg.transform.scale(guard, (tile_size, tile_size))
player    = pg.transform.scale(player, (tile_size, tile_size))

def move(old_position, direction, speed, dt):
    if direction == (0, 0):
        return old_position
    x, y = old_position
    
    direction_x, direction_y = direction

    if direction_x == 0:
        x = round(x)
        y += direction_y * speed * dt

    if direction_y == 0:
        y = round(y)
        x += direction_x * speed * dt

    return x, y

def check_wall(maze, position, direction, can_open_door):
    x, y = position
    direction_x, direction_y = direction

    boundary_x = round(x + direction_x * 0.5)
    boundary_y = round(y + direction_y * 0.5)

    if maze[boundary_y][boundary_x] == "*":
        return True
    elif maze[boundary_y][boundary_x] == "d" and not can_open_door:
        return True
    else:
        return False

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

    if not check_wall(maze, pos_player, direction, has_key):
        pos_player = move(pos_player, direction, speed, dt)

    reveal_maze(maze, pos_player)

    x, y = pos_player
    grid_x, grid_y = round(x), round(y)
    if maze[grid_y][grid_x] == "k":
        has_key = True
        maze[grid_y][grid_x] = " "

    if maze[grid_y][grid_x] == "d" and has_key:
        font = pg.font.Font(None, height // 5)  # Creates a font object with default font and size height // 5
        text = font.render("You escaped!", True, (255, 215, 0), "black")  # Creates a text surface object (True for anti-aliasing)
        textrect = text.get_rect()
        textrect.center = (width // 2, height //2)

        screen.blit(text, textrect)
        pg.display.flip()

        time.sleep(2)
        running = False

    # Drawing routine
    screen.fill(background_color)
    draw_maze(screen, maze)
    screen.blit(player, screen_pos(pos_player))
    pg.display.flip()

    dt = clock.tick(fps) / 1000  # Limits FPS and returns the elapsed time since the last frame in seconds
    dt = min(dt, dt_max)  # Prevents large dt if there's a significant slowdown/freeze

# Close the game window and properly clean up
pg.quit()
