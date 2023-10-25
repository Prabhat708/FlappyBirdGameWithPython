import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * #Basic pygame imports

# Global Variables for the game

FPS = 32
SCRWTH = 288
SCRHGHT = 511
SCREEN = pygame.display.set_mode((SCRWTH, SCRHGHT))
GRNDY = SCRHGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BG = 'gallery/sprites/background2.png'
PIPE = 'gallery/sprites/pipe.png'
def maxscore():
    f = open("highScore.txt","r")
    maxScore = int(f.read())
    f.close()
    return maxScore
def welcomeScreen():
 
   #Shows welcome images on the screen

    plyrx = int(SCRWTH/5)
    plyry = int((SCRHGHT - GAME_SPRITES['player'].get_height())/1.8)
    msgx = int((SCRWTH - GAME_SPRITES['message'].get_width()))
    msgy = 0
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):   
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (plyrx, plyry))    
                SCREEN.blit(GAME_SPRITES['message'], (msgx,msgy ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GRNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def mainGame():
    score = 0
    plyrx = int(SCRWTH/5)
    plyry = int(SCRWTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    

    #List of upper pipes
    upPipes = [
        {'x': SCRWTH+200, 'y':newPipe1[0]['y']},
        {'x': SCRWTH+200+(SCRWTH/2), 'y':newPipe2[0]['y']},
    ]
    #List of lower pipes
    lwPipes = [
        {'x': SCRWTH+200, 'y':newPipe1[1]['y']},
        {'x': SCRWTH+200+(SCRWTH/2), 'y':newPipe2[1]['y']},
    ]
    # All velocity
    pipeVelX = -4
    playerVelY = -8
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if plyry > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(plyrx, plyry, upPipes, lwPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        maxs = maxscore()
        playerMidPos = plyrx + GAME_SPRITES['player'].get_width()/2
        for pipe in upPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                GAME_SOUNDS['point'].play()
                if maxs < score:
                    f1 = open("highScore.txt","w")
                    f1.write(str(score))
                    f1.close()

                    
               
        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        plyry = plyry + min(playerVelY, GRNDY - plyry - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upPipes, lwPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upPipes.append(newpipe[0])
            lwPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upPipes.pop(0)
            lwPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upPipes, lwPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GRNDY))
        SCREEN.blit(GAME_SPRITES['player'], (plyrx, plyry))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCRWTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCRHGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
# for display maximum score 
        maxsc = maxscore()
        myscore = [int(x) for x in list(str(maxsc))]
        width = 0
        for digit in myscore:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCRWTH - width)/1.05

        for digit in myscore:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCRHGHT*0.9))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS) 
        
   # For end the game     

def isCollide(plyrx, plyry, upPipes, lwPipes):
    if plyry> GRNDY - 25  or plyry<0:
        SCREEN.blit(GAME_SPRITES['base1'], (0,150))    
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(plyry < pipeHeight + pipe['y'] and abs(plyrx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            SCREEN.blit(GAME_SPRITES['base1'], (0,150))    
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lwPipes:
        if (plyry + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(plyrx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            SCREEN.blit(GAME_SPRITES['base1'], (0,150))    
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCRHGHT/3
    y2 = offset + random.randrange(0, int(SCRHGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCRWTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe


if __name__ == "__main__":
    # This will be the main point from where our game will start
    #pygame.init() # Initialize all pygame's modules
    
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Prabhat Verma')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    pygame.init()
    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message1.jpg').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['base1'] =pygame.image.load('gallery/sprites/base1.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BG).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 
