"""
sprites.py - Stores classes for different objects
Jan 28th, 2025
"""
import random
import pygame
from settings import *

# buttons in the menu
class Button:
    def __init__(self, x, y, x_len, y_len, text_x_len, text_y_len, width, text):
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)
        self.x, self.y, self.x_len, self.y_len, self.text_x_len, self.text_y_len = x, y, x_len, y_len, text_x_len, text_y_len
        self.width = width
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.x-self.width, self.y-self.width, self.x_len+2*self.width, self.y_len+2*self.width), self.width)
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(self.x, self.y, self.x_len, self.y_len))
        screen.blit(self.my_font.render(self.text, True, (0,0,0)), (self.x+self.text_x_len, self.y+self.text_y_len))

    def is_pressed(self, x, y):
        if self.x <= x <= self.x + self.x_len and self.y <= y <= self.y + self.y_len:
            return True

# tiles in the game
class Tile:
    def __init__(self, x, y, image, type, level, revealed=False, flagged=False):
        self.image = image
        self.type = type
        self.level = level
        self.revealed = revealed
        self.flagged = flagged
        if level == 0:
            self.x, self.y = 180 + x * TILE_SIZE, 20 + y * TILE_SIZE 
        else:
            self.x, self.y = 340 + x * TILE_SIZE, 180 + y * TILE_SIZE 

    def draw(self, screen):
        if not self.flagged and not self.revealed: # not flagged or revealed
            screen.blit(tile_unknown, (self.x, self.y))
        elif self.flagged and not self.revealed: # flagged
            screen.blit(tile_flag, (self.x, self.y))
        elif self.revealed: # revealed 
            screen.blit(self.image, (self.x, self.y))

    def __repr__(self):
        return self.type

# Main menu screen
class Menu:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    def draw_bg(self, screen):
        screen.blit(blahaj_bg, (50,50))
        screen.blit(blahaj_bg2, (735,50))
        screen.blit(self.my_font.render("blahajsweeper!", True, (0,0,0)), (300,150))

    def draw_button(self, screen, button):
        button.draw(screen)

# Difficulty selection menu screen
class Difficulty:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    def draw_bg(self, screen):
        screen.blit(blahaj_bg, (50,50))
        screen.blit(blahaj_bg2, (735,50))
        screen.blit(self.my_font.render("difficulty", True, (0,0,0)), (390,130))
        screen.blit(self.my_font.render("selection!", True, (0,0,0)), (380,190))

    def draw_button(self, screen, button):
        button.draw(screen)

# End screen
class End:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.win = False
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    def draw_bg(self, screen):
        screen.blit(blahaj_bg, (50,50))
        screen.blit(blahaj_bg2, (735,50))
        if self.win:
            screen.blit(self.my_font.render("you win!", True, (0,0,0)), (390,150))
        else:
            screen.blit(self.my_font.render("you lost :(", True, (0,0,0)), (370,150))

    def draw_button(self, screen, button):
        button.draw(screen)

# the game board
class Board:
    def __init__(self, level):
        self.level = level
        self.board_surface = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.board_state = [[Tile(col, row, tile_empty, ".", level) for row in range(ROWS[self.level])] for col in range(COLS[self.level])]
        self.create_mines()
        self.store_adj()
        self.dug = []
        self.flags = NUM_MINES[level]
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 32)

    def create_mines(self):
        for _ in range(NUM_MINES[self.level]):
            while True: # repeatedly tries placing the mine
                # random coordinate
                x = random.randint(0, ROWS[self.level]-1)
                y = random.randint(0, COLS[self.level]-1)

                if self.board_state[x][y].type == ".":
                    self.board_state[x][y].image = tile_mine
                    self.board_state[x][y].type = "X"
                    break

    def store_adj(self):
        for x in range(ROWS[self.level]):
            for y in range(COLS[self.level]):
                if self.board_state[x][y].type != "X":
                    total_mines = self.num_adj(x, y)
                    # if there is at least 1 mine next to it
                    if total_mines > 0:
                        self.board_state[x][y].image = tile_numbers[total_mines-1] # tile has a number on it
                        self.board_state[x][y].type = "N"

    def num_adj(self, x, y):
        mines = 0
        for x_change in range(-1, 2):
            for y_change in range(-1, 2):
                xx = x + x_change
                yy = y + y_change
                if 0 <= xx < ROWS[self.level] and 0 <= yy < COLS[self.level] and self.board_state[xx][yy].type == "X":
                    mines += 1

        return mines

    def draw(self, screen):
        for row in self.board_state:
            for tile in row:
                tile.draw(screen)
        screen.blit(screen, (0, 0))
        screen.blit(self.my_font.render("flags left:" + str(self.flags), True, (0,0,0)), (20,20))

    def dig_tile(self, x, y):
        self.dug.append((x, y))
        if self.board_state[x][y].type == "X":
            self.board_state[x][y].revealed = True
            self.board_state[x][y].image = tile_exploded
            return False
        elif self.board_state[x][y].type == "N":
            self.board_state[x][y].revealed = True
            return True
        else:
            self.board_state[x][y].revealed = True
            for row in range(max(0, x-1), min(ROWS[self.level]-1, x+1) + 1):
                for col in range(max(0, y-1), min(COLS[self.level]-1, y+1) + 1):
                    if (row, col) not in self.dug and self.board_state[row][col].type != "X":
                        self.dig_tile(row, col)
            return True
