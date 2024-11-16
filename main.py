import time
from idlelib.debugobj_r import WrappedObjectTreeItem

import pygame
import sys
import random

# !EXPLOITATION MANUAL!
# Steps: 1) open initialization settings (line16-line25)
#        2) set window size, FPS (var HEIGHT/WIDTH/FPS)
#        3) set count of rows and columns of a maze (var ROWS/COLS)
#        4) set drawing speed (var DRAW_SPEED_MULTIPLIER)
#
#

# INITIALIZATION SETTINGS
HEIGHT = 900   #480
WIDTH = 1000    #480
FPS = 60
ROWS = 100    # WIDTH // SIZE
COLS = 100    # HEIGHT // SIZE
DRAW_SPEED_MULTIPLIER = 0.005     # Speed of drawing
SIZE = (WIDTH*0.8)/max(ROWS,COLS) #8      # Cell size(square)
W = int(SIZE/2.5)         # Outline thickness
cells = []

GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# 1/(15*15) 100(100*100)


#-------------------------------------------
# FUNCTIONS // CLASSES
class Cell:
    def __init__(self, row, col, lines, visited):
        self.row = row
        self.col = col
        self.lines = lines
        self.visited = visited

    def draw(self):
        #rect = pygame.Rect(self.col * SIZE, self.row * SIZE, SIZE, SIZE)
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

    def init_simple(self, cell: Cell):
        self.row = cell.row
        self.col = cell.col
        self.cell = cell

    def move_right(self):
        self.cell.lines[2] = 0
        new_cell = cells[self.col+1][self.row]
        self.__init__(new_cell)
        self.cell.lines[1] = 0
        self.cell.visited = 1
        #self.explorer_draw()
    def move_left(self):
        self.cell.lines[1] = 0
        new_cell = cells[self.col-1][self.row]
        self.__init__(new_cell)
        self.cell.lines[2] = 0
        self.cell.visited = 1
        #self.explorer_draw()
    def move_up(self):
        self.cell.lines[0] = 0
        new_cell = cells[self.col][self.row-1]
        self.__init__(new_cell)
        self.cell.lines[3] = 0
        self.cell.visited = 1
        #self.explorer_draw()
    def move_down(self):
        self.cell.lines[3] = 0
        new_cell = cells[self.col][self.row+1]
        self.__init__(new_cell)
        self.cell.lines[0] = 0
        self.cell.visited = 1
        #self.explorer_draw()

    def move_right_common(self):
        new_cell = cells[self.col + 1][self.row]
        #self.__init__(new_cell)
        self.init_simple(new_cell)
        #self.explorer_draw()
    def move_left_common(self):
            new_cell = cells[self.col - 1][self.row]
            #self.__init__(new_cell)
            self.init_simple(new_cell)
            #self.explorer_draw()
    def move_up_common(self):
        new_cell = cells[self.col][self.row - 1]
        #self.__init__(new_cell)
        self.init_simple(new_cell)
        #self.explorer_draw()
    def move_down_common(self):
            new_cell = cells[self.col][self.row + 1]
            #self.__init__(new_cell)
            self.init_simple(new_cell)
            #self.explorer_draw()

# StartCell --> CurrIsVisible --> CheckNeighbour --> RandomUnvisitedCell -->
# --> DeleteWall_Curr_and_Neighbour --> CurrCell=Neighbour
class Recursion_Generartion(Explorer):
    def __init__(self, cell: Cell, path=[]):
        super().__init__(cell)
        self.path = path

    def neighbour_check(self):
        ans = []
        if self.row!=0:
            if not((cells[self.col][self.row-1]).visited):
                ans.append(0)
        if self.col!=0:
            if not((cells[self.col-1][self.row]).visited):
                ans.append(1)
        if self.col!=COLS-1:
            if not((cells[self.col+1][self.row]).visited):
                ans.append(2)
        if self.row!=ROWS-1:
            if not((cells[self.col][self.row+1]).visited):
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
            return cells[self.col][self.row-1]
        elif ind == 1:
            return cells[self.col-1][self.row]
        elif ind == 2:
            return cells[self.col+1][self.row]
        elif ind == 3:
            return cells[self.col][self.row+1]

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
        print("Creating done!", "Iterations:", k)

# RightHand_Solver(start_cell, end_cell, *start_Direction)
# direction is direction TO NEXT CELL
class RightHand_Solver(Explorer):
    def __init__(self, cell:Cell, end_cell:Cell, direction=0, steps=0):
        super().__init__(cell)
        try: self.path = self.path
        except: self.path = []
        self.direction = direction
        self.end_cell = end_cell
        self.steps = steps

    def counterclockwise_next(self, num):
        return (num+1)%4
    def clockwise_next(self, num):
        return (num-1)%4

    def goto_cell(self, next_cell):
        # attempt without new val
        rowN, colN = next_cell.row, next_cell.col
        if self.row == rowN:
            if self.col-1 == colN:
                self.move_left_common()
            elif self.col+1 == colN:
                self.move_right_common()
        elif self.col == colN:
            if self.row-1 == rowN:
                self.move_up_common()
            elif self.row+1 == rowN:
                self.move_down_common()

    def clockind_to_ind(self, num):
        if num==0: return 0
        elif num==1: return 1
        elif num==2: return 3
        elif num==3: return 2


    def diretcrion_from(self, cellHome:Cell, cellCur:Cell):
        if (cellCur.row-1)==(cellHome.row): return

    # return clocksort array of allowed cells around
    # example: [0, 0, Cell_obj, 0] means that bottom is available
    def allowed_cells_clocksort(self):
        # m[0]=top, m[1]=left, m[2]=right, m[3]=bottom
        allowed_directions = self.cell.lines
        # m[0]=top, m[1]=left, m[2]=bottom, m[3]=right
        # 0=None OR cell:Cell
        allowed_cells_clocksort = [0,0,0,0]
        for i in range(0,4):
            if allowed_directions[i]==0:
                if i==0:
                    allowed_cells_clocksort[0] = (cells[self.col][self.row-1])
                elif i==1:
                    allowed_cells_clocksort[1] = (cells[self.col-1][self.row])
                elif i==2:
                    allowed_cells_clocksort[3] = (cells[self.col+1][self.row])
                elif i==3:
                    allowed_cells_clocksort[2] = (cells[self.col][self.row+1])
        return allowed_cells_clocksort

    def right_algorithm_step(self):
        # STEPS:
        # *0) start direction = any(0 for example)
        # 1) rotate direction arrow counterclockwise (search allowed lines)
        # 2) go to this closest to counterclockwise cell
        allowed_clocksort = self.allowed_cells_clocksort()
        next_counterclock_ind = self.clockwise_next(self.direction)

        # searching in counterclockwise
        while allowed_clocksort[next_counterclock_ind] == 0:
            next_counterclock_ind = self.counterclockwise_next(next_counterclock_ind)
        # next cell is found!
        if (self.cell not in self.path): self.path.append(self.cell)
        #self.direction = self.clockind_to_ind(next_counterclock_ind)
        self.direction = next_counterclock_ind
        self.goto_cell(allowed_clocksort[next_counterclock_ind])
        self.cell.visited = 1; self.steps += 1

    def step_search(self, steps):
        i = 0
        while i<steps and (self.cell != self.end_cell):
            self.right_algorithm_step()
            i+=1
        if self.cell == self.end_cell:
            print("Exit found!", self.col, self.row)

    def full_search(self):
        k = 0
        while self.cell != self.end_cell:
            self.right_algorithm_step()
            k += 1
        print("Solving done!", f'Iterations: {k}')


def start_data():
    for i in range(0,COLS):
        _row = []
        for j in range(0,ROWS):
            _row.append(Cell(j,i,[1,1,1,1], 0))
        cells.append(_row)

# functions for debug
def fill_grind():
    for x in range(0, COLS*SIZE, SIZE):
        for y in range(0, ROWS*SIZE, SIZE):
            ceil = pygame.Rect(x, y, SIZE, SIZE)
            pygame.draw.rect(screen, GREEN, ceil, W)

def attributes()->None:
    print("CURRENT ATTRIBUTES:")
    print(f"Window size: height={HEIGHT}, width={WIDTH}"); print("FPS:", FPS)
    print(f"Rows and columns: rows={ROWS}, columns={COLS}")
    print(f"Cell sizes: cell_size={SIZE}, outline_thickness={W}"); print(" ")

def border():
    pygame.draw.line(screen, GREEN, [0,0], [COLS*SIZE,0], W)
    pygame.draw.line(screen, GREEN, [0,0], [0,ROWS*SIZE], W)
    pygame.draw.line(screen, GREEN, [COLS*SIZE,0], [COLS*SIZE,ROWS*SIZE], W)
    pygame.draw.line(screen, GREEN, [0,ROWS*SIZE], [COLS*SIZE,ROWS*SIZE], W)
#---------------------


def main():
    # start settings
    running = True; find_end = True
    attributes()
    screen.fill(BLACK)
    start_data()
    print("One cell byte size:", sys.getsizeof(cells[0][0]))
    print("All cells size (cell_size * count_of_cells)", (sys.getsizeof(cells[-1][-1])*(len(cells[0]) * len(cells)))/(2**20), "Mbytes")
    print("All cells size (cell_row_size * count_of_rows)", len(cells) * sys.getsizeof(cells[-1]) / (2**20), "Mbytes"); print(" ")

    start_cell = cells[0][0]
    end_cell = cells[-1][-1]
    path = [start_cell]
    start_cell.visited = 1

    dot = Recursion_Generartion(start_cell)
    dot.recursion_generation()
    # Maze has been generated

    solver = RightHand_Solver(start_cell, end_cell)

    # start cells grid
    for _col in cells:
        for cell in _col:
            cell.visited = 0
            cell.draw()
            #solver.explorer_draw()
    start_cell.visited = 1
    pygame.display.update()

    # screen update loop
    while running:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
    #---# CODE HERE
        if solver.steps % int(ROWS * COLS * DRAW_SPEED_MULTIPLIER) == 0:
            # all maze drawing was replaced to redrawing only PATH cells
            # for _col in cells:
            #     for cell in _col:
            #         cell.draw()
            # solver.explorer_draw()
            for _cells in solver.path:
                _cells.draw()
            solver.explorer_draw()


        if solver.cell != end_cell:
            solver.step_search(int(ROWS * COLS * DRAW_SPEED_MULTIPLIER))
        else:
            if find_end == True: print(f"Solving done! Iterations: {solver.steps}")
            for _col in cells:
                for cell in _col:
                    cell.draw()
            solver.explorer_draw()
            find_end = False
        pygame.display.update()

    #---# CODE STOP
        #pygame.display.update()
        clock.tick(FPS)
#-----------------------------------------------
main()


# DO NOT FORGET:
# 1) change "visited" system in creating mode (use "visited" attribute only in searching mode)
# 1_UPD) "visited" is used in generation and solving as well. After generation
#         all cells "visited"=0(not visited), and then it uses in solving process.
# !err 2) __init__ wanna take second argument end_cell
# !err 2_UPD) error was fixed (__init__ was replaced with "init_behaviour" function)

# TODO LIST (IDEAS):
# in process 1) Cell update synchronized with screen update (vizualization)
# probably done 1) visual representation have done. Also added optimized drawing system
# 2) New maze generation methods (at this moment only recursion generation)
# in process 3) Maze solvers
# rightHand done 3) Right hand rule solver done
# 4) Create user keyboard "explorer" control (just an idea)


