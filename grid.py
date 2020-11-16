import pygame
import os

letter_x = pygame.image.load(os.path.join('images', 'X_modified.png'))
letter_o = pygame.image.load(os.path.join('images', 'o_modified.png'))


class Grid:
    def __init__(self):
        self.grid_lines = [((0, 200), (600, 200)),  # first horizontal line
                           ((0, 400), (600, 400)),  # second horizontal line
                           ((200, 0), (200, 600)),  # first vertical line
                           ((400, 0), (400, 600))]  # second vertical line
        # create  a matrix, fill values with 0
        self.grid = [[0 for x in range(3)] for y in range(3)]
        self.switch_player = True
        # N, NW , W, SW, S, SE, E, NE
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0),
                            (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False

    def draw(self, screen):
        for line in self.grid_lines:
            pygame.draw.line(screen, (0, 0, 0), line[0], line[1], 2)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    screen.blit(letter_x, (x*200, y*200))
                elif self.get_cell_value(x, y) == "O":
                    screen.blit(letter_o, (x*200, y*200))

    def get_cell_value(self, posx, posy):
        return self.grid[posy][posx]

    def set_cell_value(self, posx, posy, value):
        self.grid[posy][posx] = value

    def get_mouse(self, posx, posy, player):
        if self.get_cell_value(posx, posy) == 0:
            self.set_cell_value(posx, posy, player)
            self.check_grid(posx, posy, player)

    def is_within_bounds(self, posx, posy):
        return posx >= 0 and posx < 3 and posy >= 0 and posy < 3

    def check_grid(self, posx, posy, player):
        count = 1
        for index, (dirx, diry) in enumerate(self.search_dirs):
            if self.is_within_bounds(posx+dirx, posy+diry) and self.get_cell_value(posx+dirx, posy+diry) == player:
                count += 1
                xx = posx + dirx
                yy = posy + diry

                if self.is_within_bounds(xx + dirx, yy+diry) and self.get_cell_value(xx + dirx, yy+diry) == player:
                    count += 1
                    if count == 3:
                        break
                if count < 3:
                    new_dir = 0
                    # mapping indices to opposite direction
                    if index == 0:
                        new_dir = self.search_dirs[4]  # N to S
                    elif index == 1:
                        new_dir = self.search_dirs[5]  # NW to SE
                    elif index == 2:
                        new_dir = self.search_dirs[6]  # W to E
                    elif index == 3:
                        new_dir = self.search_dirs[7]  # SW to NE
                    elif index == 4:
                        new_dir = self.search_dirs[0]  # S to N
                    elif index == 5:
                        new_dir = self.search_dirs[1]  # SE to NW
                    elif index == 6:
                        new_dir = self.search_dirs[2]  # E to W
                    elif index == 7:
                        new_dir = self.search_dirs[3]  # NE to SW

                    if self.is_within_bounds(posx + new_dir[0], posy + new_dir[1]) \
                            and self.get_cell_value(posx + new_dir[0], posy + new_dir[1]) == player:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1
        if count == 3:
            print(player, "wins!")
            self.game_over = True
        else:
            self.game_over = self.is_grid_full()
            if self.game_over:
                print("Game Draw")

    def is_grid_full(self):
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True

    def reset_game(self):
        self.game_over = False
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)

    def print_grid(self):
        for row in self.grid:
            print(row)
