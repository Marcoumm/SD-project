import pygame, random, sys
from pygame.locals import *

from FPS import FPS

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
FPS = 60

BACKGROUNDCOLOR = (255, 255, 255)

BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6

GOODFOODMINSIZE = 10
GOODFOODMAXSIZE = 30
GOODFOODMINSPEED = 1
GOODFOODMAXSPEED = 8

BADFOODMINSIZE = 50
BADFOODMAXSIZE = 80
BADFOODMINSPEED = 2
BADFOODMAXSPEED = 8
ADDNEWBADFOODRATE = 8

PREDATORMINSIZE = 10
PREDATORMAXSIZE = 30
PREDATORMINSPEED = 1
PREDATORMAXSPEED = 8

PLAYERMOVERATE = 5

#color
PLAYER_COLOR_GREEN = 1
PLAYER_COLOR_RED = 2
PLAYER_COLOR_YELLOW = 3
PLAYER_COLOR_BLUE = 4

#type of food: good, toxic and predator
GOODFOOD = "good"
BADFOOD = "bad"
PREDATOR = "predator"

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def playerHasHitBadFood(playerRect, BadFood):
    for b in BadFood:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)
# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('jungle.wav')

# Set up images.
# all our color cameleon
playerImageBlue = pygame.image.load('camblue.png')
playerImageGreen = pygame.image.load('camgreen.png')
playerImageRed = pygame.image.load('camred.png')
playerImageYellow = pygame.image.load('camyellow.png')
#image scale
playerImageGreen = pygame.transform.scale(playerImageGreen, (70, 70))
playerImageBlue = pygame.transform.scale(playerImageBlue, (70, 70))
playerImageRed = pygame.transform.scale(playerImageRed, (70, 70))
playerImageYellow = pygame.transform.scale(playerImageYellow, (70, 70))


playerRect = playerImageGreen.get_rect()

# set up food 
foodGreen = pygame.image.load("grasshoppergreen.png")
foodRed = pygame.image.load("grasshopperred.png")
foodYellow = pygame.image.load("grasshopperyellow.png")
foodBlue = pygame.image.load("grasshopperblue.png")
# image scale 
foodGreen = pygame.transform.scale(foodGreen, (70,70))
foodRed = pygame.transform.scale(foodRed, (70,70))
foodYellow = pygame.transform.scale(foodYellow, (70,70))
foodBlue = pygame.transform.scale(foodBlue, (70,70))

#set up toxic food or predators
baddieImage = pygame.image.load('baddie.png')
badGreen = pygame.image.load("cheesegreen.png")
badRed = pygame.image.load("cheesered.png")
badYellow = pygame.image.load("cheeseyellow.png")
badBlue = pygame.image.load("cheeseblue.png")
#image scale


#set up background
backgroundImage = pygame.image.load('background.png')

# Resize background image to the screen size
backgroundImage = pygame.transform.scale(backgroundImage, windowSurface.get_size())

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
#insert our background to the screen
windowSurface.blit(backgroundImage, (0,0))
drawText('Jungle Chameleon', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

# Default game values
currentColor = PLAYER_COLOR_GREEN
topScore = 0
while True:
    
    # Set up the start of the game.
    GoodFood = []
    BadFood = []
    #create a dictionary
    #chgreen as cheese green, chred as cheese red... tlgreen as chocolate green and so and so..
    BadFoodImages = {
        "chgreen": badGreen,
        "chred": badRed,
        "chyellow": badYellow,
        "chblue": badBlue
    }
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT -70)
    moveLeft = moveRight = False
    reverseCheat = slowCheat = False
    BadFoodAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            # --------- Controls ---------

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True

        #importer keys 
            keys = pygame.key.get_pressed()
                #variables pour les codes couleur des touches
            if keys[pygame.K_1]:
                currentColor = PLAYER_COLOR_GREEN
            if keys[pygame.K_2]:
                currentColor = PLAYER_COLOR_RED
            if keys[pygame.K_3]:
                currentColor = PLAYER_COLOR_YELLOW
            if keys[pygame.K_4]:
                currentColor = PLAYER_COLOR_BLUE


            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False


        # --------- Adding bad guys --------- 

        # Add new bad food at the top of the screen, if needed.
            if not reverseCheat and not slowCheat:
                BadFoodAddCounter += 1

            if BadFoodAddCounter == ADDNEWBADFOODRATE:
                BadFoodAddCounter = 0
                BadFoodSize = random.randint(BADFOODMINSIZE, BADFOODMAXSIZE)
            #take key of the dictionary
                badFoodTypes = list(BadFoodImages.keys())
    
            # chose a random type
                chosenType = random.choice(badFoodTypes)
                newBadFood = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - BadFoodSize), 0 - BadFoodSize, BadFoodSize, BadFoodSize),
                        'speed': random.randint(BADFOODMINSPEED, BADFOODMAXSPEED),
                        'surface': pygame.transform.scale(BadFoodImages[chosenType], (BadFoodSize, BadFoodSize)),
                        'type': chosenType}
                BadFood.append(newBadFood)

        # --------- Movements ---------

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)


        # Move the baddies down.
        for b in BadFood:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # Delete baddies that have fallen past the bottom.
        for b in BadFood[:]:
            if b['rect'].top > WINDOWHEIGHT:
                BadFood.remove(b)

        # --------- Display everything on the window. ---------
        # Window clear
        windowSurface.fill(BACKGROUNDCOLOR)
        # Redraw background image
        windowSurface.blit(backgroundImage, (0,0))

        # Draw player's rectangle
        if currentColor == PLAYER_COLOR_GREEN:
            windowSurface.blit(playerImageGreen, playerRect)
        elif currentColor == PLAYER_COLOR_RED:
            windowSurface.blit(playerImageRed, playerRect)
        elif currentColor == PLAYER_COLOR_YELLOW:
            windowSurface.blit(playerImageYellow, playerRect)
        elif currentColor == PLAYER_COLOR_BLUE:
            windowSurface.blit(playerImageBlue, playerRect)


        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw each baddie.
        for b in BadFood:
            windowSurface.blit(b["surface"], b["rect"])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBadFood(playerRect, BadFood):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
