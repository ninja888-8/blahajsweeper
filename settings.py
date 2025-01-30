"""
settings.py - Stores the configuration of the minesweeper game
December 30th, 2024
"""

import pygame
import os

TILE_SIZE = 32 # in pixels
ROWS = [20, 10] # number of rows
COLS = [20, 10]
NUM_MINES = [50, 12]
WINDOW_LENGTH = TILE_SIZE * 20 + 360 # in pixels
WINDOW_HEIGHT = TILE_SIZE * 20 + 120 # in pixels
COLOUR = (173, 216, 230)

# main menu blahaj background 
blahaj_bg = pygame.image.load(os.path.join("images", "blahaj_bg.png"))
blahaj_bg2 = pygame.image.load(os.path.join("images", "blahaj_bg2.png"))

# minesweeper tile numbers
tile_numbers = []
for i in range(1, 9):
    tile_numbers.append(pygame.image.load(os.path.join("images", f"tile_{i}.png")))

# minesweeper tile dug but empty
tile_empty = pygame.image.load(os.path.join("images", "tile_empty.png"))

# minesweeper tile dug but exploded D:
tile_exploded = pygame.image.load(os.path.join("images", "tile_exploded.png"))

# minesweeper tile flagged
tile_flag = pygame.image.load(os.path.join("images", "tile_flag.png"))

# minesweeper tile was mine (game end)
tile_mine = pygame.image.load(os.path.join("images", "tile_mine.png"))

# minesweeper tile unknown / not touched
tile_unknown = pygame.image.load(os.path.join("images", "tile.png"))

# minesweeper tile is not a mine (game end)
tile_not_mine = pygame.image.load(os.path.join("images", "tile_not_mine.png"))
