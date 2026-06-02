import os
import pygame as pg
import configparser

# Get the directory of the game
game_dir = os.path.dirname(os.path.abspath(__file__))

# Read configuration file using built-in ini parser
config = configparser.ConfigParser()
config.read(os.path.join(game_dir, "config.ini"))

width = config.getint("display", "width", fallback=600)
height = config.getint("display", "height", fallback=400)

# Initialise the PyGame environment
pg.init()

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
    pos_player = [0, 0]
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "G":
                pos_guards.append([x, y])
                maze[y][x] = " "
            elif char == "P":
                pos_player = [x, y]
                maze[y][x] = " "

    return maze, pos_guards, pos_player

# Lists are mutable, so calling this function modifies the caller's maze even without returning the maze
def reveal_maze(maze, pos_player):
    x, y = pos_player
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            idx_y = y + dy
            idx_x = x + dx

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
                screen.blit(brick, screen_pos(x, y)) # Pass the top-left coordinates directly instead of using a rect
            elif char == "d":
                screen.blit(door, screen_pos(x, y))
            elif char == "k":
                screen.blit(gold_key, screen_pos(x, y))

maze, pos_guards, pos_player = load_maze("maze1.txt")
reveal_maze(maze, pos_player)

max_y = len(maze)
max_x = len(maze[0])
scale_y = height//max_y
scale_x = width//max_x

tile_size = min(scale_x, scale_y)

# Converts the world coordinate system (maze coordinates) to screen coordinates
def screen_pos(x, y):
    return x * tile_size, y * tile_size

brick     = pg.transform.scale(brick, (tile_size, tile_size))
brick_lit = pg.transform.scale(brick_lit, (tile_size, tile_size))
door      = pg.transform.scale(door, (tile_size, tile_size))
gold_key  = pg.transform.scale(gold_key, (tile_size, tile_size))
guard     = pg.transform.scale(guard, (tile_size, tile_size))
player    = pg.transform.scale(player, (tile_size, tile_size))

draw_maze(screen, maze)
pg.display.flip()

running = True

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


# Close the game window and properly clean up
pg.quit()
