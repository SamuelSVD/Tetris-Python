# Written by Samuel Vergara
# This is supposed to be a tetris remake (duuh..).
# Tetris song from: http://www.youtube.com/watch?v=NmCCQxVBfyM


import math
import pygame
import pygame.draw
import time

from pygame.locals import *
from random import randrange

images = ['Images\\red.JPG','Images\\orange.JPG','Images\\yellow.JPG','Images\\green.JPG','Images\\light_blue.JPG','Images\\blue.JPG','Images\\purple.JPG','Images\\MainMenu.JPG','Images\\Game.JPG','Images\\GamePaused.JPG','Images\\GameOver.JPG','Images\\Controls.JPG','Images\\HighScores.JPG']

#Block type
RED = 0
ORANGE = 1
YELLOW = 2
GREEN = 3
LIGHT_BLUE = 4
BLUE = 5
PURPLE = 6
#Game States
MAIN_MENU = 7
GAME = 8
CONTROLS = 11
HIGH_SCORES = 12

#Others
GAME_PAUSED = 9
GAME_OVER = 10

# IN GAME VARIABLES
DROP_DELAY = 0.6
KEY_DELAY = 0.1
DOWN = 0
LEFT = 1
RIGHT = 2

# Control location of the gameBlock
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
[[0,0,6],[0,-1,6],[0,1,6],[0,2,6]]]  #Vertical

GRID_X = 10
GRID_Y = 20


#Complete
def loadImages():
    temp = []
    for name in images:
        temp.append(pygame.image.load(name))
    return temp

#Complete
def drawShape(screen, images, shape):
        for block in shape:
            screen.blit(images[block[2]], ((block[0] + X_[0] + offsetX)*32,(block[1] + Y_[0] + offsetY)*32))

#WHY IS THIS ROTATING!?!?!?!
def drawNextShape(screen, images, shape): #Look this part over...
        shapes = [[[-1,0,0],[0,0,0],[0,-1,0],[1,0,0]],  #T      #RED
          [[0,0,1],[-1,0,1],[0,-1,1],[1,-1,1]], #S      #ORANGE
          [[0,0,2],[1,0,2],[0,-1,2],[-1,-1,2]], #Z      #YELLOW
          [[0,0,3],[0,-1,3],[-1,0,3],[-2,0,3]], #L      #GREEN
          [[0,0,4],[0,-1,4],[1,0,4],[2,0,4]],   #bL     #LIGHT_BLUE
          [[0,0,5],[0,1,5],[1,0,5],[1,1,5]],    #square
          [[0,0,6],[-1,0,6],[1,0,6],[2,0,6]]]   #Vertical
        tempShape = shapes[shape[0][2]]
        if shape[0][2] == RED or shape[0][2] == ORANGE or shape[0][2] == YELLOW:
            for block in tempShape:
                screen.blit(images[block[2]], ((block[0] + 14)*32,(block[1] + 2.5)*32))
        elif shape[0][2] == GREEN:
            for block in tempShape:
                screen.blit(images[block[2]], ((block[0] + 15)*32,(block[1] + 2.5)*32))
        elif shape[0][2] == LIGHT_BLUE:
            for block in tempShape:
                screen.blit(images[block[2]], ((block[0] + 13)*32,(block[1] + 2.5)*32))
        elif shape[0][2] == BLUE:
            for block in tempShape:
                screen.blit(images[block[2]], ((block[0] + 13.5)*32,(block[1] + 1.5)*32))
        elif shape[0][2] == PURPLE:
            for block in tempShape:
                screen.blit(images[block[2]], ((block[0] + 13.5)*32,(block[1] + 2)*32))


#Complete
def drawGrid(screen, images, grid):
        for gBlock in grid:
            screen.blit(images[gBlock[2]],((gBlock[0]+offsetX)* 32,(gBlock[1]+offsetY) * 32))

#Complete
def rotate(shape):
	for block in shape: block[0],block[1] = block[1],-block[0]

#Complete
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
        
#        Shapes[0],Shapes[1] = list(Shapes[1]),list(shapes[YELLOW])

        X_[0] = 5
        Y_[0] = -2
        return Shapes


def updateGrid(grid, shape,score):
    isgameover = False
    for block in shape:
            coord = list(block)
            coord[0],coord[1] = coord[0]+X_[0],coord[1]+Y_[0]
            if coord[1] < 0:
                isgameover = True
            grid.append(coord)
    blockCount = [0]*GRID_Y #Creates list of zeros for all rows in grid
    for gblock in grid: #For every block in the grid it will add 1 to the counter
        blockCount[gblock[1]] += 1
    toRemove = []
    numRows = 0
    for i in range(GRID_Y): #checks all the row's block count
        if blockCount[i] == 10: # if the block count = 10
            #print 'removing row:',i
            numRows += 1
            for gBlock in grid:
                #print gBlock,
                if gBlock[1] == i:
                    toRemove.append(list(gBlock))
    for i in range(GRID_Y):
        if blockCount[i] == 10:
            for block in toRemove:
                if (block[1] == i):
                    grid.remove(block)
            for gblock in grid: # for every block above that value, add 1.
                if gblock[1] < i:
                    gblock[1] += 1
    #----------------------------------
    if numRows == 1:
        score += 100
    elif numRows == 2:
        score += 225
    elif numRows == 3:
        score += 375
    elif numRows == 4:
        score += 550
    if isgameover:
        grid.append(isgameover)
    #print 'Score:', score
    return grid,[score,numRows]

#Complete
def moveLeft(X_):
        X_[0] += -1

#Complete
def moveRight(X_):
        X_[0] += 1

#Complete
def moveDown(Y_):
        Y_[0] += 1

#Complete
def drop(shape, grid, X_, Y_):
        while canMove(shape,grid,DOWN,X_,Y_):
                moveDown(Y_)

#Complete
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
        pygame.display.set_icon(pygame.image.load("Images\\img.JPG"))
        self.screen = pygame.display.set_mode((576,768))
        self.width = 576; self.height = 768
        self.fullscreen = False
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("TETRIS!")
        
    

    def toggleFullscreen(self):
        modes = pygame.display.list_modes()
        if not self.fullscreen: self.screen = pygame.display.set_mode((576,768),FULLSCREEN)
        else: self.screen = pygame.display.set_mode((576,768))
        self.fullscreen = not self.fullscreen
        self.refresh_size()

    def refresh_size(self):
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

def main():
    pygame.font.init()
    tgs = TetrisGameState()
    tgs.fullscreen = True
    tgs.toggleFullscreen()
    running = True
    #Load tetris music and begin playing
    pygame.mixer.init()
    music = pygame.mixer.music
    music.load('Tetris.mp3')
    music.play(-1)
    ###
    music.stop()
    ###
    
    #Load images to be used in game
    images = loadImages()
    
#    gameState = MAIN_MENU
    gameState = MAIN_MENU
    # In Game variables
    currentShapes = [list(shapes[randrange(0,len(shapes))]),list(shapes[randrange(0,len(shapes))])] #[current shape, next shape]
    game_grid = []
    nextFall = time.time()
    keyDelay = time.time() # used to limit the speed of keys pressed.
    score = 0
    numRows = 0
    gameover = False
    isPaused = False
    fromGame = False
    font = pygame.font.SysFont('geniso', 16, True, False)
    font2 = pygame.font.SysFont('geniso', 16, True, False)
    
    while running:
        tgs.screen.fill((100,0,0))

        #----------------MAIN MENU---------------#
        if (gameState == MAIN_MENU):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if mousePos[0] > 0 and mousePos[0] <= 32 and mousePos[1] > 0 and mousePos[1] <= 32:
                        print "HEY YOU! YEAH YOU!"
                        print 'Main Menu Screen'
                    #If click lies on 'Play', gameState == GAME
                    elif mousePos[0] > 32 and mousePos[0] <= 32+32*8 and mousePos[1] > 32*11 and mousePos[1] <= 20*32: 
                        gameState = GAME
                        currentShapes = [list(shapes[randrange(0,len(shapes))]),list(shapes[randrange(0,len(shapes))])]
                        game_grid = []
                        fasterTime = 0
                        score = 0
                        numRows = 0
                        X_[0] = 5
                        Y_[0] = -2
                        gameover = False
                        print 'Play pressed'
                        
                    #If click lies on 'Controls', gameState == CONTROLS
                    elif mousePos[0] > 320 and mousePos[0] <= 17*32 and mousePos[1] > 32*11 and mousePos[1] <= 32*15: 
                        gameState = CONTROLS

                    #If click lies on 'High Scores', gameState == HIGH_SCORES
                    elif mousePos[0] > 320 and mousePos[0] <= 17*32 and mousePos[1] > 32*16 and mousePos[1] <= 32*20: 
                        gameState == HIGH_SCORES
                        
            tgs.screen.blit(images[MAIN_MENU],(0,0))

        #----------------IN GAME-----------------#
                
        
        if (gameState == GAME):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    print mousePos
#Resume button
                    if mousePos[0] > 223 and mousePos[0] <= 349 and mousePos[1] > 341 and mousePos[1] <= 379 and isPaused: 
                        isPaused = False
# Controls button
                    elif mousePos[0] > 231 and mousePos[0] <= 335 and mousePos[1] > 393 and mousePos[1] <= 429 and isPaused: 
                        gameState = CONTROLS
                        fromGame = True
# High Scores button
                    elif mousePos[0] > 223 and mousePos[0] <= 341 and mousePos[1] > 445 and mousePos[1] <= 477 and isPaused: 
                        gameState = MAIN_MENU
                        isPaused = False

            # Get keys pressed
            keys = pygame.key.get_pressed()
            #limit movement left, right and rotation to KEY_DELAY (seconds)
            if(keyDelay - time.time() < 0):
# P - Pause
                if keys[K_p] == True and not gameover:
                    isPaused = not isPaused
                    keyDelay = time.time() + KEY_DELAY
                if not isPaused and not gameover:
                    if keys[K_UP] == True:
                        canRotateL = canRotate(currentShapes[0], game_grid)
                        if canRotateL:
                            rotate(currentShapes[0])
                            keyDelay = time.time() + KEY_DELAY
# LEFT
                    elif keys[K_LEFT] == True and canMove(currentShapes[0], game_grid, LEFT, X_, Y_):
                        moveLeft(X_)
                        keyDelay = time.time() + KEY_DELAY
# RIGHT
                    elif keys[K_RIGHT] == True and canMove(currentShapes[0], game_grid, RIGHT, X_, Y_) :
                        moveRight(X_)
                        keyDelay = time.time() + KEY_DELAY
# DOWN
                    elif keys[K_DOWN] == True:
#                    print 'DROPPING'
                        drop(currentShapes[0],game_grid,X_,Y_)
#                    print 'DROPPED'
                        game_grid,r = updateGrid(game_grid, currentShapes[0],score)
                        score = r[0]
                        numRows += r[1]
                        if type(game_grid[len(game_grid)-1]) == bool:
                            gameover = True
                        currentShapes = nextShape(currentShapes)
                        keyDelay = time.time() + KEY_DELAY
                        nextFall = time.time() + DROP_DELAY + fasterTime;
                        
# SPACE
                    elif keys[K_SPACE] == True:
                        if canMove(currentShapes[0], game_grid, DOWN, X_, Y_): moveDown(Y_)
                        keyDelay = time.time() + KEY_DELAY

            if not isPaused and not gameover:
# Update gravity
                if (nextFall - time.time() < 0):
                    nextFall = time.time() + DROP_DELAY**((numRows+2)/2.0) + 0.08;
                    print DROP_DELAY**((numRows+2)/2.0) + 0.08
                    if canMove(currentShapes[0],game_grid,DOWN,X_,Y_): moveDown(Y_)
                    else:
                            game_grid,r = updateGrid(game_grid, currentShapes[0],score)
                            score = r[0]
                            numRows += r[1]
                            if type(game_grid[len(game_grid)-1]) == bool:
                                gameover = True
                            currentShapes = nextShape(currentShapes)
            
                #print 'Playing'
                tgs.screen.blit(images[GAME],(0,0))
                # Draw shapes.
                drawShape(tgs.screen, images, currentShapes[0])
                drawNextShape(tgs.screen, images, currentShapes[1])
                tgs.screen.blit(images[GAME],(0,0),(0,0,576,32))
                tgs.screen.blit(font.render("SCORE:",1,(255,255,255),(0,0,0)),(395,276-32))
                tgs.screen.blit(font.render(str(score),1,(255,255,255),(0,0,0)),(395+60,276-32))

                tgs.screen.blit(font.render("ROWS:",1,(255,255,255),(0,0,0)),(395,325-32))
                tgs.screen.blit(font.render(str(numRows),1,(255,255,255),(0,0,0)),(395+60,325-32))

            
            if not isPaused and not gameover:
                # Draw grid.
                drawGrid(tgs.screen, images, game_grid)
            elif isPaused:
                tgs.screen.blit(images[GAME_PAUSED],(0,0))
            else:
                tgs.screen.blit(images[GAME_OVER],(0,0))
            
        #------------------IN CONTROLS--------------#
        elif (gameState == CONTROLS):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    print mousePos
                    if mousePos[0] > 77 and mousePos[0] <= 161 and mousePos[1] > 650 and mousePos[1] <= 686:
                        gameState = GAME
                        if not fromGame:
                            currentShapes = [list(shapes[randrange(0,len(shapes))]),list(shapes[randrange(0,len(shapes))])]
                            game_grid = []
                            fasterTime = 0
                            score = 0
                            numRows = 0
                            X_[0] = 5
                            Y_[0] = -2
                        else:
                            fromGame = False
                            
                    elif mousePos[0] > 357 and mousePos[0] <= 505 and mousePos[1] > 650 and mousePos[1] <= 686: 
                        gameState = MAIN_MENU
                        if isPaused:
                            isPaused = False
                        fromGame = False
            #print 'Controls Screen'
            tgs.screen.blit(images[CONTROLS],(0,0))
            
        #----------------IN HIGH SCORES-------------#
        elif (gameState == HIGH_SCORES) :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    print mousePos
            print 'High Scores Screen'

        
        #HOW TO DRAW AN IMAGE ON SCREEN!
        #tgs.screen.blit(images[MAIN_MENU],(0,0))


        pygame.display.flip()
        tgs.clock.tick(1000)
main()
