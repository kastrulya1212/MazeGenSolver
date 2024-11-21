# MazeGenSolver
#### Programs that creates maze row:columns with various algorithms and solve it as well.


## The main topics.
- User exploitation manual
- Coordinate system
- Screen update principle



### User exploitation manual.
The main logic of program locate in the 'main.py'. To generate new maze you should know some
important attributes which you can see in the 'steps' part. The maze
generation and solving processes automatically, and it is always randomly
generated.

Steps:
1) open initialization settings in main.py (line16-line25)
2) set window size, FPS (var HEIGHT/WIDTH/FPS)
3) set count of rows and columns of a maze (var ROWS/COLS)
4) set drawing speed (var DRAW_SPEED_MULTIPLIER)
5) go to the def main() and choose maze generation method (Recursion, Prims)
           and maze solving method (Right hand method). Choose them according to the
           instructions.

At this moment there are 2 maze generation algorithms and 1 maze solving method. 

Maze generation algorithms: 
- 1. Recursion algorithm
- 2. Prim's algorithm

Solving methods:
- 1. Right hand method
   


### Coordinate system and cell's important attributes.
The program uses objects of the class 'Cell' to create a grid, and each 'cell' has it's own 
settings like X,Y coordinates and etc. 'Cell' is a square, therefore, at the start
each of them has 4 walls (up, bottom, left, right), so during the execution of program
walls can be deleted, so it is the main principle of the maze generation. 

This program uses 2 quite similar coordinate systems - casual and clockwise/counterclockwise.
According to these systems, 'cell' can store it's walls(borders/lines) as 
array that looks like [0, 0, 0, 0]. Each position equals wall on the one of the sides.
- '0' - equals absence of the wall.
- '1' - equals existing of the wall

**First system example:** lines=[0,0,0,0]  -  (ind0-topside; ind1-left side;
ind2-RIGHT side; ind3-BOTTOM side)

**Second system example:** lines=[0,0,0,0]  -  (ind0-topside; ind1-left side;
ind2-BOTTOM side; ind3-RIGHT side). So as you noticed, this one similar to
counterclockwise system.

Also, 'cell' has attribute 'visited'(num between 0 and 1).
- '0' - was not visited.
- '1' - was visited.



### Screen update principle.
The main loop has optimized display. The first step is generating and drawing the maze,
so its execute once. Then we calculate size of the maze and depending on that, the
program sets values for drawing speed and steps (1 step - one offset, so this attribute
equals how many steps we can skip during drawing. But calculation of steps continue
inside program).
Because of this, we significantly reduce drawing time, because we have not to draw
the full maze again, but only changed 'cells' which were visited.


