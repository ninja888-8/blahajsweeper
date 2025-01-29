"""
blahajsweeper.py - Main program
Eric Ning
December 30th, 2024
Description: runs a blahaj themed/designed minesweeper game!
"""

# importing packages
import pygame
from settings import *
from sprites import *

# Game class
class Game:
    # initializing
    def __init__(self, state, generated_board, buttons):
        self.screen = pygame.display.set_mode((WINDOW_LENGTH,WINDOW_HEIGHT))
        self.state = state
        self.generated_board = generated_board
        self.buttons = buttons
        self.menu = Menu()
        self.difficulty = Difficulty()
        self.end = End()
        self.easy = 0
        self.new_board()
        pygame.display.set_caption("blahajsweeper!!!")
        
    # create new board and displays it
    def new_board(self):
        self.board = Board(self.easy)

    # main program loop
    def run(self):
        while self.state != "quit":
            if self.state == "menu":
                self.main_menu_events()
                self.draw_menu()
                self.generated_board = False
            elif self.state == "difficulty":
                self.difficulty_events()
                self.draw_difficulty()
            elif self.state == "playing" or self.state == "waiting":
                self.playing_events()
                self.draw_tiles()
            elif self.state == "results":
                self.end_screen_events()
                self.draw_end_screen()

    # checks if all the non-mines are already dug
    def check_win(self):
        for row in self.board.board_state:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

    # displays the menu
    def draw_menu(self):
        self.screen.fill(COLOUR)
        self.menu.draw_bg(self.screen)
        self.menu.draw_button(self.screen, self.buttons[0])
        self.menu.draw_button(self.screen, self.buttons[1])
        pygame.display.flip()

    # displays the difficulty select screen
    def draw_difficulty(self):
        self.screen.fill(COLOUR)
        self.difficulty.draw_bg(self.screen)
        self.difficulty.draw_button(self.screen, self.buttons[4])
        self.difficulty.draw_button(self.screen, self.buttons[5])
        pygame.display.flip()

    # draws all the minesweeper tiles
    def draw_tiles(self):
        self.screen.fill(COLOUR)
        self.board.draw(self.screen)
        if self.state == "waiting":
            self.buttons[3].draw(self.screen)
        pygame.display.flip()

    # draws all the minesweeper tiles
    def draw_end_screen(self):
        self.screen.fill(COLOUR)
        self.end.draw_bg(self.screen)
        self.end.draw_button(self.screen, self.buttons[2])
        self.end.draw_button(self.screen, self.buttons[1])
        pygame.display.flip()

    # deals with user events in the main menu
    def main_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                ex, ey = pygame.mouse.get_pos()

                if event.button == 1 and self.state == "menu":
                    if self.buttons[0].is_pressed(ex, ey):
                        self.state = "difficulty"

                    if self.buttons[1].is_pressed(ex, ey):
                        pygame.quit()
                        quit(0)

    # deals with user events in the difficulty selection menu
    def difficulty_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                ex, ey = pygame.mouse.get_pos()

                if event.button == 1 and self.state == "difficulty":
                    if self.buttons[4].is_pressed(ex, ey):
                        self.state = "playing"
                        self.easy = 1
                        self.new_board()

                    if self.buttons[5].is_pressed(ex, ey):
                        self.state = "playing"
                        self.easy = 0
                        self.new_board()

    # deals with user events in the actual minesweeper game field
    def playing_events(self):
        for event in pygame.event.get():
            # quitting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            # mouse click during game
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == "playing":
                ex, ey = pygame.mouse.get_pos()
                if self.easy == 0:
                    ex -= 180
                    ey -= 20
                else:
                    ex -= 340
                    ey -= 180
                ex //= TILE_SIZE
                ey //= TILE_SIZE

                if event.button == 1 and self.state == "playing":
                    if not self.board.board_state[ex][ey].flagged:
                        while not self.generated_board:
                            game.new_board()
                            if self.board.board_state[ex][ey].type == ".":
                                self.generated_board = True
                        if not self.board.dig_tile(ex, ey):
                            for row in self.board.board_state:
                                for tile in row:
                                    if tile.flagged and tile.type != "X":
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = tile_not_mine
                                    elif tile.type == "X":
                                        tile.revealed = True
                            self.state = "waiting"

                if event.button == 3 and self.state == "playing":
                    if not self.board.board_state[ex][ey].revealed:
                        if self.board.board_state[ex][ey].flagged:
                            self.board.board_state[ex][ey].flagged = False
                            self.board.flags += 1
                        else:
                            self.board.board_state[ex][ey].flagged = True
                            self.board.flags -= 1

                if self.check_win():
                    self.end.win = True
                    self.state = "waiting"
                    self.board.flags = 0
                    self.end.win = True
                    for row in self.board.board_state:
                        for tile in row:
                            if not tile.revealed:
                                tile.flagged = True

            if event.type == pygame.MOUSEBUTTONDOWN and self.state == "waiting":
                ex, ey = pygame.mouse.get_pos()

                if self.buttons[3].is_pressed(ex, ey):
                    self.state = "results"


    # displays the end screen
    def end_screen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                ex, ey = pygame.mouse.get_pos()

                if event.button == 1 and self.state == "results":
                    if self.buttons[2].is_pressed(ex, ey):
                        self.state = "menu"

                    if self.buttons[1].is_pressed(ex, ey):
                        pygame.quit()
                        quit(0)

# creates new game
game = Game("menu", False, [Button(200,350,600,100,235,20,5,"start!"), Button(200,500,600,100,245,20,5,"quit?"), Button(200,350,600,100,25,20,5,"return to main menu!"), Button(200,675,600,75,185,10,5,"continue"), Button(200,350,600,100,250,20,5,"easy"), Button(200,500,600,100,250,20,5,"hard")])
game.run()