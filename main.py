from reprlib import recursive_repr

import pygame
import sys
import random

# __init__
HEIGHT = 480
WIDTH = 480
FPS = 5
SIZE = 30   # Cell size(square)
W = 5       # Outline thickness
ROWS = 15    #WIDTH // SIZE
COLS = 15    #HEIGHT // SIZE
cells = []

GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


#-------------------------------------------
# FUNCTIONS // CLASSES
class Cell:
    def __init__(self, row, col, lines, visited):
        self.row = row
        self.col = col
        self.lines = lines
        self.visited = visited

    def draw(self):
        rect = pygame.Rect(self.col * SIZE, self.row * SIZE, SIZE, SIZE)
        if self.visited:
            pygame.draw.rect(screen, DARK_GREEN, (self.col*SIZE, self.row*SIZE, SIZE, SIZE))
        if self.lines[0]:
            pygame.draw.line(screen, GREEN, [self.col*SIZE, self.row*SIZE], [self.col*SIZE+SIZE, self.row*SIZE], W)
        if self.lines[1]:
            pygame.draw.line(screen, GREEN, [self.col*SIZE, self.row*SIZE], [self.col*SIZE, self.row*SIZE+SIZE], W)
        if self.lines[2]:
            pygame.draw.line(screen, GREEN, [self.col*SIZE+SIZE, self.row*SIZE], [self.col*SIZE+SIZE, self.row*SIZE+SIZE], W)
        if self.lines[3]:
            pygame.draw.line(screen, GREEN, [self.col*SIZE,self.row*SIZE+SIZE], [self.col*SIZE+SIZE, self.row*SIZE+SIZE], W)

class Explorer:
    def __init__(self, cell: Cell):
        self.row = cell.row
        self.col = cell.col
        self.cell = cell
    def explorer_draw(self):
        pygame.draw.rect(screen, WHITE, (self.col*SIZE+W/2, self.row*SIZE+W/2, SIZE-W/2, SIZE-W/2))

    def move_right(self):
        self.cell.lines[2] = 0
        new_cell = cells[self.row][self.col+1]
        self.__init__(new_cell)
        self.cell.lines[1] = 0
        self.cell.visited = 1
        self.explorer_draw()
    def move_left(self):
        self.cell.lines[1] = 0
        new_cell = cells[self.row][self.col-1]
        self.__init__(new_cell)
        self.cell.lines[2] = 0
        self.cell.visited = 1
        self.explorer_draw()
    def move_up(self):
        self.cell.lines[0] = 0
        new_cell = cells[self.row-1][self.col]
        self.__init__(new_cell)
        self.cell.lines[3] = 0
        self.cell.visited = 1
        self.explorer_draw()
    def move_down(self):
        self.cell.lines[3] = 0
        new_cell = cells[self.row+1][self.col]
        self.__init__(new_cell)
        self.cell.lines[0] = 0
        self.cell.visited = 1
        self.explorer_draw()

class Recursion_Generartion(Explorer):
    def __init__(self, cell: Cell):
        super().__init__(cell)
        try: self.path = self.path
        except: self.path = []

    def neighbour_check(self):
        ans = []
        if self.row!=0:
            if not((cells[self.row - 1][self.col]).visited):
                ans.append(0)
        if self.col!=0:
            if not((cells[self.row][self.col - 1]).visited):
                ans.append(1)
        if self.col!=COLS-1:
            if not((cells[self.row][self.col+1]).visited):
                ans.append(2)
        if self.row!=ROWS-1:
            if not((cells[self.row + 1][self.col]).visited):
                ans.append(3)
        return ans

    def neighbour_goto(self, cellN: Cell):
        rowN, colN = cellN.row, cellN.col
        if self.row == rowN:
            if self.col-1 == colN:
                self.move_left()
            elif self.col+1 == colN:
                self.move_right()
        elif self.col == colN:
            if self.row-1 == rowN:
                self.move_up()
            elif self.row+1 == rowN:
                self.move_down()

    def neighbour_by_ind(self, ind):
        if ind == 0:
            return cells[self.row-1][self.col]
        elif ind == 1:
            return cells[self.row][self.col-1]
        elif ind == 2:
            return cells[self.row][self.col+1]
        elif ind == 3:
            return cells[self.row+1][self.col]

    def path_step_back(self):
        self.path.pop(-1)
        if self.path != []:
            self.neighbour_goto(self.path[-1])

    def path_searching(self):
        neighbours = self.neighbour_check()
        while neighbours != []:
            ind = neighbours[random.randrange(0,len(neighbours))]
            self.neighbour_goto(self.neighbour_by_ind(ind))
            self.path.append(self.cell)
            neighbours = self.neighbour_check()

    def recursion_generation(self):
        k = 0
        self.path.append(self.cell)
        while self.path != []:
            k += 1
            self.path_searching()
            if self.path != []:
                self.path_step_back()
        print("Done!", "Iterations:", k)


def start_data():
    for i in range(0,COLS):
        _row = []
        for j in range(0,ROWS):
            _row.append(Cell(i,j,[1,1,1,1], 0))
        cells.append(_row)

# functions for debug
def fill_grind():
    for x in range(0, COLS*SIZE, SIZE):
        for y in range(0, ROWS*SIZE, SIZE):
            ceil = pygame.Rect(x, y, SIZE, SIZE)
            pygame.draw.rect(screen, GREEN, ceil, W)

def border():
    pygame.draw.line(screen, GREEN, [0,0], [COLS*SIZE,0], W)
    pygame.draw.line(screen, GREEN, [0,0], [0,ROWS*SIZE], W)
    pygame.draw.line(screen, GREEN, [COLS*SIZE,0], [COLS*SIZE,ROWS*SIZE], W)
    pygame.draw.line(screen, GREEN, [0,ROWS*SIZE], [COLS*SIZE,ROWS*SIZE], W)
#---------------------


def main():
    # start settings
    running = True
    screen.fill(BLACK)
    start_data()

    start_cell = cells[0][0]
    end_cell = cells[-1][-1]
    path = [start_cell]
    start_cell.visited = 1

    dot = Recursion_Generartion(start_cell)
    dot.recursion_generation()

    # dot.move_right(); dot.move_down(); dot.move_right(); dot.move_down()
    # dot.move_left(); dot.move_left(); dot.move_up(); dot.move_down(); dot.move_down()

    # start cells grid
    for _col in cells:
        for cell in _col:
            cell.draw()
    dot.explorer_draw()

    # screen update loop
    while running:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
    #---# CODE HERE



    #---# CODE STOP
        pygame.display.update()
        clock.tick(FPS)
#-----------------------------------------------
main()


# TODO LIST:
# 1) Cell update synchronized with screen update (vizualization)
# 2) New maze generation methods
# 3) Maze solvers


