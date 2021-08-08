import random #For generating random numbers 
import sys #we will use sys.exit to exit the program/game
import pygame
from pygame.locals import * # Basic pygame imports 
#Global variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode(SCREENWIDTH, SCREENHEIGHT)
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS= {}
PLAYER = 'flappy/sprites/bird.png'
BACKGROUND = 'flappy/sprites/background.png'
PIPE = 'flappy/sprites/pipe.png'


def welcomeScreen():
    '''
    Shows welcome images on the screen 
    '''

    playerx = int((SCREENWIDTH/5))
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get.height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['player'].get.height())/2)
    messagey = int((SCREENHEIGHT * 0.13))
    basex = 0
    while True:
        for event in pygame.event.get():
            # if the user clicks on the cross button, then close the game.
            if event.type == QUIT or (event.type == KEYDOWN or event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()


            #if the user presses space or up key then start the program for them.

            elif event.type == KEYDOWN and (event.type == K_SPACE or event.type == K_UP):
                return
            
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)






def mainGame():
    score = 0
    playerx = int((SCREENWIDTH/5))
    playery = int((SCREENWIDTH/2))
    basex = 0

    # Create 2 pipes for blitting on the screen.
    newPipe1 = get.RandomPipe()
    newPipe2 = get.RandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping



    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN or event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.type == PACE or event.type == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) #This function will return to if the player is crashed.
        if crashTest:
            return
        
        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f'Your score is: {score}')
                GAME_SOUNDS['point'].play()



            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False
            
            playerHeight = GAME_SPRITES['player'].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

            #move pipes to the left
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX


            #add a new pipe when the first pipe is about to cross to the left part of the screen

            if 0 < upperPipes[0]['x']< 5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])
            
            #lets blit our gamesprites
            SCREEN.blit(GAME_SPRITES['background'],(0,0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):   
                SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))         
            SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
            SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = (SCREENWIDTH-width)/2

            for digit in myDigits:
                Screen.blit(GAME_SPRITES['numbers'][digit],(Xoffset, SCREENHEIGHT*0.12))
                Xoffset  += GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(fps)


            # if the pipe is out of the screen remove it
            if upperpipes[0]['x']  < - GAME_SPRITES['pipe'].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY-25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
        return True
    
    
    for pipe in lowerPipes:
        if (playery < GAME_SPRITES['pipe'][0].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
        return True



            


def getRandomPipe():
    '''
    generate positions of 2 pipes (one bottom straight and top rotated) for blitting on the screen
    '''
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipex = [
        {'x': pipex,'y': -y1}, #upper pipe
        {'x': pipex, 'y': y2} #lower pipe
    ]
    return pipe 




if __name__ == "__main__":
    #This will be the main function where the game will start.
    pygame.init() #Initialises all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("FlappyBird by Manav Notaria")
    GAME_SPRITES['numbers'] = (
        pygame.image.load('flappy/sprites/0.png').convert_alpha(),
        pygame.image.load('flappy/sprites/1.jpeg').convert_alpha(),
        pygame.image.load('flappy/sprites/2.jpeg').convert_alpha(),
        pygame.image.load('flappy/sprites/3.jpeg').convert_alpha(),
        pygame.image.load('flappy/sprites/4.jpeg').convert_alpha(),
        pygame.image.load('flappy/sprites/5.jpeg').convert_alpha(),
        pygame.image.load('flappy/sprites/6.jpeg').convert_alpha(),
        pygame.image.load('flappy/sprites/7.jpeg').convert_alpha(),
        pygame.image.load('flappy/sprites/8.jpeg').convert_alpha(),
        pygame.image.load('flappy/sprites/9.jpeg').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('flappy/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('flappy/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.image.load(PIPE).convert_alpha(),
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha().convert_alpha(), 180),
        )        


    #GAME SOUNDS
    GAME_SOUNDS['die'] = pygame.mixer.Sound('flappy/audio/die.mp3')
    GAME_SOUNDS['wind'] = pygame.mixer.Sound('flappy/audio/wind.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('flappy/audio/hit.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('flappy/audio/swoosh.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('flappy/audio/point.mp3')


    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() #shows welcome screen to the user until he presses the button
        mainGame() #This is the main game function