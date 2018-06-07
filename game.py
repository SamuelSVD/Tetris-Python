#Tetris.py
#A simple TETRIS clone

import math
import pygame
import pygame.draw
import time

from pygame.locals import *
from random import randrange

# Colors
DROP_DELAY = 1
KEY_DELAY = 0.1
DOWN = 0
LEFT = 1
RIGHT = 2
X_ = [5]
Y_ = [0]

offsetX = 1
offsetY = 1

shapes = [[[-1,0,0],[0,0,0],[0,-1,0],[1,0,0]], #T
[[0,0,1],[0,-1,1],[1,0,1],[1,1,1]], #S
[[0,0,2],[0,1,2],[1,0,2],[1,-1,2]], #Z
[[0,0,3],[1,0,3],[0,-1,3],[0,-2,3]], #L
[[0,0,4],[-1,0,4],[0,-1,4],[0,-2,4]], #bL
[[0,0,5],[0,1,5],[1,0,5],[1,1,5]], #square
[[0,0,6],[0,-1,6],[0,1,6],[0,2,6]]] #V

GRID_X = 10
GRID_Y = 20


def drawShape(screen, shape):# CHECK!
        for block in shape:
            screen.blit(images[block[2]], ((block[0] + X_[0] + offsetX)*32,(block[1] + Y_[0] + offsetY)*32))

def drawNextShape(screen, shape): #Look this part over...
        for block in shape:
            screen.blit(images[block[2]], ((block[0] + X_[0] + 15)*32,(block[1] + Y_[0] + 2)*32))

def drawGrid(screen, grid): # CHECK!
        for gBlock in grid:
            screen.blit(images[gBlock[2]],((gBlock[0]+offsetX)* 32,(gBlock[1]+offsetY) * 32))

def rotate(shape):
	for block in shape: block[0],block[1] = block[1],-block[0]

def canRotate(shape, grid):
        canRotate_ = True
        for block in shape:
                block[0],block[1]=block[1],-block[0]
        for block in shape:
                if (block[0] + X_[0] < 0 or block[0] + X_[0] >= GRID_X or block[1] + Y_[0] >= GRID_Y):
                        canRotate_ = False
                        break
                for gBlock in grid:
                        if block[0]+X_[0] == gBlock[0] and block[1]+Y_[0] == gBlock[1]:
                                canRotate_ = False
                                break
        
        #Necessary to fix bug where block rotates twice.
        for block in shape:
                block[0],block[1]=-block[1],block[0]

        return canRotate_

def nextShape(Shapes):
        Shapes[0],Shapes[1] = Shapes[1],list(shapes[randrange(0,len(shapes))])
        X_[0] = 5
        Y_[0] = -2
        return Shapes
        
def updateGrid(grid, shape):
        for block in shape:
                coord = list(block)
                coord[0],coord[1] = coord[0]+X_[0],coord[1]+Y_[0]
                grid.append(coord)
        blockCount = [0]*GRID_Y #Creates list of zeros for all rows in grid
        for gblock in grid: #For every block in the grid it will add 1 to the counter
                blockCount[gblock[1]] += 1
        for i in range(GRID_Y): #checks all the row's block count
                if blockCount[i] == 10: # if the block count = 10
                        for n in range(GRID_X): # remove blocks with all the same y value,
                                grid.remove([n,i])
                        for gblock in grid: # for every block above that value, add 1.
                                if gblock[1] < i:
                                        gblock[1] += 1
        return grid

def moveLeft(X_):
        X_[0] += -1

def moveRight(X_):
        X_[0] += 1

def moveDown(Y_):
        Y_[0] += 1

def drop(shape, grid, X_, Y_):
        while canMove(shape,grid,DOWN,X_,Y_):
                moveDown(Y_)
        
def canMove(shape, grid, direction, X_, Y_):
        change_X = 0
        change_Y = 0
        if direction == LEFT:
                change_X = -1
        if direction == RIGHT:
                change_X = 1
        if direction == DOWN:
                change_Y = 1
        
        for block in shape:
                VAR_X = block[0] + X_[0] + change_X
                VAR_Y = block[1] + Y_[0] + change_Y
                for Gblock in grid:
                        if VAR_X == Gblock[0] and VAR_Y == Gblock[1]: return False
                        if VAR_X == GRID_X or VAR_X < 0 or VAR_Y == GRID_Y: return False

        return True
                
class TetrisGameState:
    def __init__(self):
        self.screen = pygame.display.set_mode((800,600))
        self.width = 800; self.height = 600
        self.fullscreen = False
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("TETRIS!")

    def toggleFullscreen(self):
        modes = pygame.display.list_modes()
        if not self.fullscreen: self.screen = pygame.display.set_mode((800,600),FULLSCREEN)
        else: self.screen = pygame.display.set_mode((800,600))
        self.fullscreen = not self.fullscreen
        self.refresh_size()

    def refresh_size(self):
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()



def main():
    currentShapes = [list(shapes[randrange(0,len(shapes))]),list(shapes[randrange(0,len(shapes))])]
    game_grid = [[0,0,1],[0,19,1],[9,19,1],[9,0,1]]
    nextFall = time.time()
    keyDelay = time.time() # used to limit the speed of keys pressed.
    fasterTime = 0

        keys = pygame.key.get_pressed()
        #limit movement left, right and down to 100 ms (or if the timer goes off)
        if(keyDelay - time.time() < 0):
                if keys[K_UP] == True:
                        canRotateL = canRotate(currentShapes[0], game_grid)
                        if canRotateL:
                                rotate(currentShapes[0])
                                keyDelay = time.time() + KEY_DELAY
                elif keys[K_LEFT] == True and canMove(currentShapes[0], game_grid, LEFT, X_, Y_):
                        moveLeft(X_)
                        keyDelay = time.time() + KEY_DELAY
                elif keys[K_RIGHT] == True and canMove(currentShapes[0], game_grid, RIGHT, X_, Y_) :
                        moveRight(X_)
                        keyDelay = time.time() + KEY_DELAY
                elif keys[K_DOWN] == True:
                        drop(currentShapes[0],game_grid,X_,Y_)
                        game_grid = updateGrid(game_grid, currentShapes[0])
                        currentShapes = nextShape(currentShapes)
                        keyDelay = time.time() + KEY_DELAY
                elif keys[K_SPACE] == True:
                        if canMove(currentShapes[0], game_grid, DOWN, X_, Y_): moveDown(Y_)
                        keyDelay = time.time() + KEY_DELAY
        if (nextFall - time.time() < 0):
                nextFall = time.time() + DROP_DELAY + fasterTime;
                if canMove(currentShapes[0],game_grid,DOWN,X_,Y_): moveDown(Y_)
                else:
                        updateGrid(game_grid, currentShapes[0])
                        currentShapes = nextShape(currentShapes)
        drawShape(tgs.screen, currentShapes[0])
        drawNextShape(tgs.screen, currentShapes[1])
        drawGrid(tgs.screen, game_grid)
        pygame.display.flip()
        tgs.clock.tick(100)
