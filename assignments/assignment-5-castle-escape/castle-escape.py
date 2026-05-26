import os
import pygame as pg

# Get the directory of the game
game_dir = os.path.dirname(os.path.abspath(__file__))

# Initialise the PyGame environment
pg.init()

resolution = (1920, 1080)
screen = pg.display.set_mode(resolution)

# Load all assets
brick     = pg.image.load(os.path.join(game_dir, "brick.png"))
brick_lit = pg.image.load(os.path.join(game_dir, "brick_lit.png"))
door      = pg.image.load(os.path.join(game_dir, "door.png"))
gold_key  = pg.image.load(os.path.join(game_dir, "gold_key.png"))
guard     = pg.image.load(os.path.join(game_dir, "guard.png"))
player    = pg.image.load(os.path.join(game_dir, "player.png"))

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
