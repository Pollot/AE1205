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
            line = line[:-1] # Removes the \n
            maze.append(list(line))
    
    pos_guards = []
    pos_player = [0, 0]
    for i, row in enumerate(maze):
        for j, char in enumerate(row):
            if char == "G":
                pos_guards.append([i, j])
                maze[i][j] = " "
            elif char == "P":
                pos_player = [i, j]
                maze[i][j] = " "

    return maze, pos_guards, pos_player

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
