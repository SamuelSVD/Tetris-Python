# Written by Samuel Vergara
# This is supposed to be a tetris remake (duuh..).
# Tetris song from: http://www.youtube.com/watch?v=NmCCQxVBfyM


import math
import pygame
import pygame.draw
import time


images = ['Images\\red.JPG','Images\\orange.JPG','Images\\yellow.JPG','Images\\green.JPG','Images\\light_blue.JPG','Images\\blue.JPG','Images\\purple.JPG','Images\\MainMenu.JPG','Images\\Game.JPG']

#Block type
RED = 0
ORANGE = 1
YELLOW = 2
GREEN = 3
LIGNT_BLUE = 4
BLUE = 5
PURPLE = 6
#Game States
MAIN_MENU = 7
GAME = 8
CONTROLS = 9
HIGH_SCORES = 10

def loadImages():
    temp = []
    for name in images:
        temp.append(pygame.image.load(name))
    return temp

class TetrisGameState:
    def __init__(self):
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
    pygame.display.init()
    pygame.display.set_icon(pygame.image.load("Images\\img.JPG"))
    tgs = TetrisGameState()
    tgs.fullscreen = True
    tgs.toggleFullscreen()
    running = True
    #Load tetris music and begin playing
    pygame.mixer.init()
    music = pygame.mixer.music
    music.load('Tetris.mp3')
    music.play()
    
    #Load images to be used in game
    images = loadImages()
    
    gameState = MAIN_MENU
    
    while running:
        tgs.screen.fill((100,0,0))
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
                    elif mousePos[0] > 32 and mousePos[0] <= 64 and mousePos[1] > 0 and mousePos[1] <= 32: 
                        gameState = GAME
                        print 'gameButton pressed'
                        
                    #If click lies on 'Controls', gameState == CONTROLS
                    elif mousePos[0] > 10 and mousePos[0] <= 20 and mousePos[1] > 20 and mousePos[1] <= 30: 
                        gameState = CONTROLS

                    #If click lies on 'High Scores', gameState == HIGH_SCORES
                    elif mousePos[0] > 10 and mousePos[0] <= 20 and mousePos[1] > 10 and mousePos[1] <= 20: 
                        gameState == HIGH_SCORES
                        
            tgs.screen.blit(images[MAIN_MENU],(0,0))
                                    
        elif (gameState == GAME):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if mousePos[0] > 10 and mousePos[0] <= 20 and mousePos[1] > 10 and mousePos[1] <= 20 and gamePused: 
                        gameState = CONTROLS
                        fromGame = True
                if mousePos[0] > 10 and mousePos[0] <= 20 and mousePos[1] > 10 and mousePos[1] <= 20 and gamePused: 
                        gameState = MAIN__MENU
                        fromGame = False
            # Get keys pressed
            # Update gravity
            print 'Playing'
            tgs.screen.blit(images[GAME],(0,0))
            # Draw shapes.
            # Draw grid.
            tgs.screen.blit(images[GAME],(0,0),(0,0,576,32))
            
            
        elif (gameState == CONTROLS):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
            print 'Controls Screen'


        elif (gameState == HIGH_SCORES) :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
            print 'High Scores Screen'

        
        #HOW TO DRAW AN IMAGE ON SCREEN!
        #tgs.screen.blit(images[MAIN_MENU],(0,0))


        pygame.display.flip()
        tgs.clock.tick(1000)
