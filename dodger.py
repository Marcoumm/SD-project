import pygame, random, sys
from pygame.locals import *

from FPS import FPS

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 200, 0)
FPS = 60

BACKGROUNDCOLOR = (255, 255, 255)

GOODFOODMINSIZE = 50
GOODFOODMAXSIZE = 80
GOODFOODMINSPEED = 2 
GOODFOODMAXSPEED = 8
ADDNEWGOODFOODRATE = 40 

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

		# score with match color good food with player color
def playerHasHitGoodFood(playerRect, GoodFood, currentColor):
	for food in GoodFood:
		if playerRect.colliderect(food["rect"]) and not food.get("touched", False):
			if food["type"] == currentColor:
				# show that the food has been touched
				food["touched"] = True
				GoodFood.remove(food)
				return "match"
			else:
				food["touched"] = True
				return "wrong"
	return None

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
playerImageGreen = pygame.transform.scale(playerImageGreen, (80, 80))
playerImageBlue = pygame.transform.scale(playerImageBlue, (80, 80))
playerImageRed = pygame.transform.scale(playerImageRed, (80, 80))
playerImageYellow = pygame.transform.scale(playerImageYellow, (80, 80))


playerRect = playerImageGreen.get_rect()

# set up food 
foodGreen = pygame.image.load("grasshoppergreen.png")
foodRed = pygame.image.load("grasshopperred.png")
foodYellow = pygame.image.load("grasshopperyellow.png")
foodBlue = pygame.image.load("grasshopperblue.png")
# image scale 
#foodGreen = pygame.transform.scale(foodGreen, (70,70))
#foodRed = pygame.transform.scale(foodRed, (70,70))
#foodYellow = pygame.transform.scale(foodYellow, (70,70))
#foodBlue = pygame.transform.scale(foodBlue, (70,70))

#set up toxic food
badGreen = pygame.image.load("cheesegreen.png")
badRed = pygame.image.load("cheesered.png")
badYellow = pygame.image.load("cheeseyellow.png")
badBlue = pygame.image.load("cheeseblue.png")

ChocoGreen = pygame.image.load("chocoGreen.png")
ChocoRed = pygame.image.load("chocoRed.png")
ChocoYellow = pygame.image.load("chocoYellow.png")
ChocoBlue = pygame.image.load("chocoGreen.png")
# predators
#aligator
AliGreen = pygame.image.load("aligreen.png")
AliRed = pygame.image.load("alired.png")
AliYellow = pygame.image.load("aliyellow.png")
AliBlue = pygame.image.load("aliblue.png")
#eagle
EagleGreen = pygame.image.load("eaglegreen.png")
EagleRed = pygame.image.load("eaglered.png")
EagleYellow = pygame.image.load("eagleyellow.png")
EagleBlue = pygame.image.load("eagleblue.png")
#owl
OwlGreen = pygame.image.load("owlgreen.png")
OwlRed = pygame.image.load("owlred.png")
OwlYellow = pygame.image.load("owlyellow.png")
OwlBljue = pygame.image.load("owlblue.png")
#snake
SnakeGreen = pygame.image.load("snakegreen.png")
SnakeRed = pygame.image.load("snakered.png")
SnakeYellow = pygame.image.load("snakeyellow.png")
SnakeBlue = pygame.image.load("snakeblue.png")


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
	#grgreen as grasshopper green, grred as grasshopper red...
	GoodFoodImages = {
		PLAYER_COLOR_GREEN: foodGreen,
		PLAYER_COLOR_RED: foodRed,
		PLAYER_COLOR_YELLOW: foodYellow,
		PLAYER_COLOR_BLUE: foodBlue
	}
	#chgreen as cheese green, chred as cheese red... tlgreen as chocolate green and so and so..
	BadFoodImages = {
		"chgreen": badGreen,
		"chred": badRed,
		"chyellow": badYellow,
		"chblue": badBlue,
		"chocgreen": ChocoGreen,
		"chocred" : ChocoRed, 
		"chocyellow": ChocoYellow,
		"chocblue": ChocoBlue
	}
	score = 0
	playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT -80)
	moveLeft = moveRight = False
	reverseCheat = slowCheat = False
	GoodFoodAddCounter = 0
	BadFoodAddCounter = 0
	pygame.mixer.music.play(-1, 0.0)

	while True: # The game loop runs while the game part is playing. 

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

		# --------- Adding good food ---------
		if not reverseCheat and not slowCheat:
				GoodFoodAddCounter += 1

		if GoodFoodAddCounter == ADDNEWGOODFOODRATE:
			GoodFoodAddCounter = 0
			GoodFoodSize = random.randint(GOODFOODMINSIZE, GOODFOODMAXSIZE)
			#take key of the dictionary
			GoodFoodTypes = list(GoodFoodImages.keys())
	
			# chose a random type
			chosenType1 = random.choice(GoodFoodTypes)
			newGoodFood = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - GoodFoodSize), 0 - GoodFoodSize, GoodFoodSize, GoodFoodSize),
					'speed': random.randint(GOODFOODMINSPEED, GOODFOODMAXSPEED),
					'surface': pygame.transform.scale(GoodFoodImages[chosenType1], (GoodFoodSize, GoodFoodSize)),
					'type': chosenType1}
			GoodFood.append(newGoodFood)

		# --------- Adding bad food --------- 
			if not reverseCheat and not slowCheat:
				BadFoodAddCounter += 1

			if BadFoodAddCounter == ADDNEWBADFOODRATE:
				BadFoodAddCounter = 0
				BadFoodSize = random.randint(BADFOODMINSIZE, BADFOODMAXSIZE)
			#take key of the dictionary
				badFoodTypes = list(BadFoodImages.keys())
	
			# chose a random type
				chosenType2 = random.choice(badFoodTypes)
				newBadFood = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - BadFoodSize), 0 - BadFoodSize, BadFoodSize, BadFoodSize),
						'speed': random.randint(BADFOODMINSPEED, BADFOODMAXSPEED),
						'surface': pygame.transform.scale(BadFoodImages[chosenType2], (BadFoodSize, BadFoodSize)),
						'type': chosenType2}
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
		for b in GoodFood:
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
		for b in GoodFood [:]:
			if b["rect"].top > WINDOWHEIGHT:
				GoodFood.remove(b)

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
		for b in GoodFood:
			windowSurface.blit(b["surface"], b["rect"])

		pygame.display.update()

		# Check if any of the baddies have hit the player.
		if playerHasHitBadFood(playerRect, BadFood):
			if score > topScore:
				topScore = score # set new top score
			break

		# Check if any good food have hit the player
		collision_result = playerHasHitGoodFood(playerRect, GoodFood, currentColor)
		if collision_result == "wrong":
			if score > topScore:
				topScore = score
			break
		elif collision_result == "match":
			score += 1

		mainClock.tick(FPS)

	# Stop the game and show the "Game Over" screen.
	pygame.mixer.music.stop()
	gameOverSound.play()

	drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
	drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
	pygame.display.update()
	waitForPlayerToPressKey()

	gameOverSound.stop()
