# import random
#
# class Test:
#     def __init__(self, mass, heigth):
#         self.mass = mass
#         self.height = heigth
#     def update(self):
#         self.__init__(50,7.5)
#
# a1 = Test(100, 15)
# a1.update()
# print(a1.mass, a1.height)
#
# a = [1,2,3]
# a.pop(-1)
# print(a)

import pygame
import sys
import random

# INITIALIZATION SETTINGS
HEIGHT = 480
WIDTH = 480
FPS = 5
W = 5



GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (30, 150, 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Cell:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color
    def draw_lines(self):
        left_top = self.rect.topleft
        left_bottom = self.rect.bottomleft
        right_bottom = self.rect.bottomright
        right_top = self.rect.topright

        pygame.draw.line(screen, GREEN, left_top, right_top, W)
        pygame.draw.line(screen, GREEN, left_top, left_bottom, W)
        pygame.draw.line(screen, GREEN, right_bottom, left_bottom, W)
        pygame.draw.line(screen, GREEN, right_bottom, right_top, W)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        self.draw_lines()

def main():
    # start settings
    running = True
    screen.fill(BLACK)

    rect1 = pygame.Rect(100, 100, 100, 100)
    rect2 = pygame.Rect(300, 100, 100, 100)
    a1 = Cell(rect1, DARK_GREEN); a2 = Cell(rect2, LIGHT_GREEN)
    a1.draw(); a2.draw();

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