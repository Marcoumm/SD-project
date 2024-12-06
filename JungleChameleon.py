import pygame, random, sys
from pygame.locals import *

from FPS import FPS

# ------ basic settings -----
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 140, 0)
FPS = 60
BACKGROUNDCOLOR = (210, 255, 200)

GOODFOODMINSIZE = 40
GOODFOODMAXSIZE = 60
GOODFOODMINSPEED = 2
GOODFOODMAXSPEED = 4
ADDNEWGOODFOODRATE = 40 

BADFOODMINSIZE = 40
BADFOODMAXSIZE = 60
BADFOODMINSPEED = 2
BADFOODMAXSPEED = 5
ADDNEWBADFOODRATE = 40

PLAYERMOVERATE = 5
DOUBLEPOINTSBONUS_DURATION = 8000
SPOT_DURATION = 5000
BUG_MOVE_DURATION = 3000

#color
PLAYER_COLOR_GREEN = 1
PLAYER_COLOR_RED = 2
PLAYER_COLOR_YELLOW = 3
PLAYER_COLOR_BLUE = 4


class GameElement:
    
	def __init__(self, windowWidth, windowHeight, color, left, top, size, speed, image, touchingSound=None):
		self.color = color
		self.rect = pygame.Rect(random.randint(0, windowWidth - size), 0 - size, size, size)
		self.speed = speed
		self.surface = pygame.transform.scale(image, (size, size))
		self.touched = False
		self.touchingSound = touchingSound

	def touch(self):
		self.touched = True

	def isTouched(self):
		return self.touched

	def playTouchingSound(self):
		if self.touchingSound:
			self.touchingSound.play()

# ----- functions -----

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
				if event.key == K_SPACE:  # Continue only if barre espace is pressed.
					return
				

def drawText(text, font, surface, center_x, center_y):
	textobj = font.render(text, 1, TEXTCOLOR)
	textrect = textobj.get_rect()
	textrect.center = (center_x, center_y)
	surface.blit(textobj, textrect)


def playerHasHitBadFood(playerRect, BadFood):
	global lives, maxLives, doublePointsActive, doublePointsTimer, spotVisible, spotTime, bugMoveActive, bugMoveTimer
	for b in BadFood[:]:
		if isinstance(b, GameElement):
			if playerRect.colliderect(b.rect):
				b.playTouchingSound()
				if b.color == "bonus":  # Check if it's a bonus item
					if lives < maxLives:
						lives += 1
				elif b.color == "doublebonus":
					doublePointsActive = True
					doublePointsTimer = pygame.time.get_ticks()

				elif b.color == "spotmalus":
					spotVisible = True
					spotTime = pygame.time.get_ticks()
					
				elif b.color == "malus":
					bugMoveActive = True
					bugMoveTimer = pygame.time.get_ticks()
			
				else: 
					lives -= 1
				BadFood.remove(b)
				
				if lives > 0:
					return False
				break
	return None

		# check if it's a match between food's color and player's color
def playerHasHitGoodFood(playerRect, GoodFood, currentColor):
	for food in GoodFood:
		if isinstance(food, GameElement):
			if playerRect.colliderect(food.rect) and not food.isTouched():
				food.touch()
				GoodFood.remove(food)
				if food.color == currentColor:
					BonusSound.play()
					return "match"
				else:
					MalusSound.play()
					return "wrong"
	return None

#function malus spot
def applySpotMalusEffect():
    global spotVisible, spotTime, Spot
    
    if spotVisible and Spot:
        # calculate time during the spot has been active
        currentTime = pygame.time.get_ticks()
        elapsedTime = currentTime - spotTime
        
        # Check if the effect should still be visible  (max 5000)
        if elapsedTime < SPOT_DURATION:
            # Draw the spotmalus image at the center
            spot_rect = Spot.get_rect(center=(windowSurface.get_width() // 2, windowSurface.get_height() // 2)) 
            windowSurface.blit(Spot, spot_rect)
        else:
            # erase the spot
            spotVisible = False

#function Bug malus
def applyBugMalusEffect():
	global bugMoveActive, bugMoveTimer
	if bugMoveActive :
		currentTime = pygame.time.get_ticks()
		if currentTime - bugMoveTimer >= BUG_MOVE_DURATION:
			bugMoveActive = False


#function for bonus
def applyDoublePointsBonus():
	global doublePointsActive, doublePointsTimer
	if doublePointsActive:
		timer = pygame.time.get_ticks()
		if timer - doublePointsTimer >= DOUBLEPOINTSBONUS_DURATION:
			doublePointsActive = False


#gameover function
def GameOver(score, topScore):
	if score > topScore:
		topScore = score

	pygame.mixer.music.stop()
	gameOverSound.play()

	#draw game over screen
	drawText('GAME OVER', font, windowSurface, 300, 250)
	drawText('Press space to play again.', font, windowSurface, 300, 300)
	drawLives(lives)
	pygame.display.update()
	
	#wait player to press space
	waitForPlayerToPressKey()
	#stop sound
	gameOverSound.stop()

	return topScore

# draw Lives on the screen
def drawLives(lives):
	for i in range(lives):
		windowSurface.blit(flower, (WINDOWWIDTH - (lives * flowerWidth + (lives - 1) * 10) - 20 + i * (flowerWidth + 10), 20))


# --------- Import element ---------

# Set up the game and the screen
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Jungle')
pygame.mouse.set_visible(False)


# Set up sound of the game and the game-over sound
pygame.mixer.music.load('jungle.wav')
gameOverSound = pygame.mixer.Sound('gameover.wav')
#diminue volume
gameOverSound.set_volume(0.1)


# Set up images
#illustration of lives: flowers
flower = pygame.image.load("pinkflower.png")
flower = pygame.transform.scale(flower, (40, 40))
flowerWidth = flower.get_width()
flowerHeight = flower.get_height()

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

#define the player as a rect.
playerRect = playerImageGreen.get_rect()

#import design of bonus/malus
Bonus = pygame.image.load("heart.png")
DoublePointsBonus = pygame.image.load("plus.png")
Malus = pygame.image.load("mushroom.png")
SpotMalus = pygame.image.load("tache.png")
Spot = pygame.image.load("tache.png").convert_alpha()
Spot = pygame.transform.scale(Spot, (600, 600))

#Import Element of each color
goodFoodImages = {
	PLAYER_COLOR_GREEN: pygame.image.load("grasshoppergreen.png"),
	PLAYER_COLOR_RED: pygame.image.load("grasshopperred.png"),
	PLAYER_COLOR_YELLOW: pygame.image.load("grasshopperyellow.png"),
	PLAYER_COLOR_BLUE: pygame.image.load("grasshopperblue.png"),
}

AlligatorImages = {
	PLAYER_COLOR_GREEN: pygame.image.load("aligreen.png"),
	PLAYER_COLOR_RED: pygame.image.load("alired.png"),
	PLAYER_COLOR_YELLOW: pygame.image.load("aliyellow.png"),
	PLAYER_COLOR_BLUE: pygame.image.load("aliblue.png"),
}
EagleImages = {
	PLAYER_COLOR_GREEN: pygame.image.load("eaglegreen.png"),
	PLAYER_COLOR_RED: pygame.image.load("eaglered.png"),
	PLAYER_COLOR_YELLOW: pygame.image.load("eagleyellow.png"),
	PLAYER_COLOR_BLUE: pygame.image.load("eagleblue.png"),
}
OwlImages = {
	PLAYER_COLOR_GREEN: pygame.image.load("owlgreen.png"),
	PLAYER_COLOR_RED: pygame.image.load("owlred.png"),
	PLAYER_COLOR_YELLOW: pygame.image.load("owlyellow.png"),
	PLAYER_COLOR_BLUE: pygame.image.load("owlblue.png"),
}
SnakeImages = {
	PLAYER_COLOR_GREEN: pygame.image.load("snakegreen.png"),
	PLAYER_COLOR_RED: pygame.image.load("snakered.png"),
	PLAYER_COLOR_YELLOW: pygame.image.load("snakeyellow.png"),
	PLAYER_COLOR_BLUE: pygame.image.load("snakeblue.png"),
}

badFoodItems = {
    "alligator": AlligatorImages,
    "owl": OwlImages,
    "snake": SnakeImages,
    "eagle": EagleImages,
	"bonus": Bonus,
	"doublebonus": DoublePointsBonus,
	"malus": Malus,
	"spotmalus": SpotMalus
}

#set up sound for each type of content
MalusSound = pygame.mixer.Sound("malus.wav")
BonusSound = pygame.mixer.Sound("bonus.wav")

badFoodSound = {
	"alligator": pygame.mixer.Sound("Alligator.wav"),
	"owl": pygame.mixer.Sound("Owl.wav"),
	"snake": pygame.mixer.Sound("snake.wav"),
	"eagle": pygame.mixer.Sound("Eagle.wav"),
	"bonus": BonusSound,
	"doublebonus": BonusSound,
	"malus": MalusSound,
	"spotmalus": MalusSound
}
#set up volumes for these sound
badFoodSound["alligator"].set_volume(0.3)
badFoodSound["eagle"].set_volume(0.3)
badFoodSound["owl"].set_volume(0.3)
badFoodSound["snake"].set_volume(0.3)
MalusSound.set_volume(0.8)

#upload font type
font = pygame.font.Font("Tropiland.ttf", 48)
smallFont = pygame.font.Font("Tropiland.ttf", 35)

#set up background
backgroundImage = pygame.image.load('background.png')

# Resize background image to the screen size
backgroundImage = pygame.transform.scale(backgroundImage, windowSurface.get_size())

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
#insert our background to the screen
windowSurface.blit(backgroundImage, (0,0))

#set up values
# Default game values
currentColor = PLAYER_COLOR_GREEN
lives = 3
maxLives = 6
topScore = 0

#text element for the game
drawText('Jungle Chameleon', font, windowSurface, 300, 230)
drawText('Press space to start.', font, windowSurface, 300, 300)
drawText("1 for green", smallFont, windowSurface, 300, 360)
drawText("2 for red", smallFont, windowSurface, 300, 400)
drawText("3 for yellow", smallFont, windowSurface, 300, 440)
drawText("4 for blue", smallFont, windowSurface, 300, 480)
drawText("Lives:",smallFont, windowSurface, 390, 40)
drawLives(lives)
pygame.display.update()
waitForPlayerToPressKey()

#increase the speed of the game with the score
speedMultiplier = 1.0

while True:
	
	# Set up the start of the game.
	goodFood = []
	#BadFood means predators / bonus and malus
	badFood = []
	lives = 3
	score = 0
	doublePointsActive = False
	doublePointsTimer = 0
	spotVisible = False
	bugMoveActive = False
	bugMoveTimer = 0
	playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT -80)
	moveLeft = moveRight = False
	reverseCheat = slowCheat = False
	goodFoodAddCounter = 0
	badFoodAddCounter = 0
	pygame.mixer.music.play(-1, 0.0)

	# --------- Game loop ---------

	while True: # The game loop runs while the game part is playing. 

		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			
			if spotVisible:
				windowSurface.blit(SpotMalus, (0, 0))

			# --------- Controls ---------

			if event.type == KEYDOWN:
				if event.key == K_z:
					reverseCheat = True
				if event.key == K_x:
					slowCheat = True
				# you can also use a or d to move
				if event.key == K_LEFT or event.key == K_a:
					moveRight = False
					moveLeft = True
				if event.key == K_RIGHT or event.key == K_d:
					moveLeft = False
					moveRight = True
			
		#import keys (1,2,3,4)
			keys = pygame.key.get_pressed()
				#keys linked to color
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
					# if you want to reverse the game direction or make the game slower, you lose max 30 points
					if score >= 30:
						score -= 30
					else:
						score = 0
				if event.key == K_x:
					slowCheat = False
					if score >= 30:
						score -=30
					else:
						score = 0
				if event.key == K_ESCAPE:
					terminate()

				if event.key == K_LEFT or event.key == K_a:
					moveLeft = False
				if event.key == K_RIGHT or event.key == K_d:
					moveRight = False

		# --------- Adding good food ---------
		if not reverseCheat and not slowCheat:
				goodFoodAddCounter += 1

		if goodFoodAddCounter == ADDNEWGOODFOODRATE:
			goodFoodAddCounter = 0
			goodFoodSize = random.randint(GOODFOODMINSIZE, GOODFOODMAXSIZE)
		
			# call class
			randomColor = random.choice(list(goodFoodImages.keys()))
			newGoodFood = GameElement(WINDOWWIDTH, WINDOWHEIGHT, randomColor, random.randint(0, WINDOWWIDTH - goodFoodSize), 0 - goodFoodSize, goodFoodSize, random.randint(GOODFOODMINSPEED, GOODFOODMAXSPEED), goodFoodImages[randomColor], BonusSound)


			goodFood.append(newGoodFood)

		# --------- Adding baddies "bad food" --------- 
		if not reverseCheat and not slowCheat:
			badFoodAddCounter += 1

		if badFoodAddCounter == ADDNEWBADFOODRATE:
			badFoodAddCounter = 0
			BadFoodSize = random.randint(BADFOODMINSIZE, BADFOODMAXSIZE)
			
			#call class Game element
			randomType = random.choice(list(badFoodItems.keys()))
			#malus and bonus haven't key color, separate them
			if randomType in ["bonus", "malus", "doublebonus", "spotmalus"]:
				newBadFoodImage = badFoodItems[randomType]
				sound = badFoodSound[randomType]
			else:
				randomColor = random.choice(list(badFoodItems[randomType].keys()))
				sound = badFoodSound[randomType]
				newBadFoodImage = badFoodItems[randomType][randomColor]
			# Create the new bad food (or animal) GameElement
			newBadFood = GameElement(WINDOWWIDTH, WINDOWHEIGHT, randomType, random.randint(0, WINDOWWIDTH - BadFoodSize), 0 - BadFoodSize, BadFoodSize, random.randint(BADFOODMINSPEED, BADFOODMAXSPEED), newBadFoodImage, touchingSound=sound)
			
			badFood.append(newBadFood)

		# --------- Movements ---------

		# Move the player around.
		if moveLeft and playerRect.left > 0:
			playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
		if moveRight and playerRect.right < WINDOWWIDTH:
			playerRect.move_ip(PLAYERMOVERATE, 0)

		#the bug move active make the player's movement jerky
		if bugMoveActive:
			elapsedTime = pygame.time.get_ticks() - bugMoveTimer
			if elapsedTime <BUG_MOVE_DURATION:
				jitter_x = random.randint(-8, 8)
				playerRect.move_ip(jitter_x, 0)
			else:
				bugMoveActive = False

		# increase speed game due to score
		speedMultiplier = 1 + (score//10) * 0.2

		# Move the baddies down.
		for b in badFood:
			if not reverseCheat and not slowCheat:
				b.rect.move_ip(0, b.speed*speedMultiplier)
			elif reverseCheat:
				b.rect.move_ip(0, -5)
			elif slowCheat:
				b.rect.move_ip(0, 1)
		for b in goodFood:
			if not reverseCheat and not slowCheat:
				b.rect.move_ip(0, b.speed*speedMultiplier)
			elif reverseCheat:
				b.rect.move_ip(0, -5)
			elif slowCheat:
				b.rect.move_ip(0, 1)

		# Delete  element that have fallen past the bottom.
		for b in badFood[:]:
			if b.rect.top > WINDOWHEIGHT:
				badFood.remove(b)
		for b in goodFood [:]:
			if b.rect.top > WINDOWHEIGHT:
				goodFood.remove(b)

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


		# Draw the score, top score and lives
		drawText('Score: %s' % (score), smallFont, windowSurface, 85, 40)
		drawText('Top Score: %s' % (topScore), smallFont, windowSurface, 110, 80)
		drawLives(lives)

		# Draw each element.
		for b in badFood:
			windowSurface.blit(b.surface, b.rect)
		for b in goodFood:
			windowSurface.blit(b.surface, b.rect)

		# Draw the malus 
		applySpotMalusEffect()
		applyBugMalusEffect()
		applyDoublePointsBonus()

		pygame.display.update()

		# Check if any of the bad food have hit the player and check the lives
		if not playerHasHitBadFood(playerRect, badFood):
			if lives <= 0:
				if score > topScore:
					topScore = score
				topScore = GameOver(score, topScore)
				break
		
		# Check if any good food have hit the player and check the lives
		# check if the collisution is a matching color between player and good food
		collision_result = playerHasHitGoodFood(playerRect, goodFood, currentColor)
		if collision_result == "wrong":
			lives -= 1
			if lives > 0:
				pass
			elif lives <= 0:
				if score > topScore:
					topScore = score
				topScore = GameOver(score, topScore)
				break
		elif collision_result == "match":
			if doublePointsActive:
				score += 2
			else:
				score += 1

		

		mainClock.tick(FPS)


	
