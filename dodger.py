import pygame, random, sys
from pygame.locals import *

from FPS import FPS

# https://www.w3schools.com/python/python_classes.asp



#program basic setting
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 140, 0)
#font = pygame.font.Font("JungleJunk.ttf", 48)  # Remplacez 'ma_police.ttf' par le chemin de votre fichier de police
FPS = 60
BACKGROUNDCOLOR = (210, 255, 200)
#create a variable live, player has 3 lives at the beginning
LIVES = 3

GOODFOODMINSIZE = 40
GOODFOODMAXSIZE = 60
GOODFOODMINSPEED = 2
GOODFOODMAXSPEED = 4
ADDNEWGOODFOODRATE = 40 

BADFOODMINSIZE = 40
BADFOODMAXSIZE = 60
BADFOODMINSPEED = 1
BADFOODMAXSPEED = 5
ADDNEWBADFOODRATE = 70

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

#create my function

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
				if event.key == K_RETURN:  # Continue only if ENTER is pressed.
					return
				

def drawText(text, font, surface, x, y):
	textobj = font.render(text, 1, TEXTCOLOR)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)


def playerHasHitBadFood(playerRect, BadFood):
	global LIVES
	for b in BadFood:
		if isinstance(b, GameElement):
			if playerRect.colliderect(b.rect):
				LIVES -= 1
				BadFood.remove(b)
				b.playTouchingSound()
				if LIVES > 0:
					return False
				break
	return True

		# score with match color good food with player color
def playerHasHitGoodFood(playerRect, GoodFood, currentColor):
	global LIVES
	for food in GoodFood:
		if isinstance(food, GameElement):
			if playerRect.colliderect(food.rect) and not food.isTouched():
				food.touch()
				if food.color == currentColor:
					GoodFood.remove(food)
					return "match"
				else:
					GoodFood.remove(food)
					food.playTouchingSound()
					return "wrong"
	return None

def GameOver(score, topScore):
	if score > topScore:
		topScore = score

	pygame.mixer.music.stop()
	gameOverSound.play()

	#draw game over screen
	drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
	drawText('Press enter to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
	pygame.display.update()
	
	#wait player to press enter
	waitForPlayerToPressKey()
	#stop sound
	gameOverSound.stop()

	return topScore

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)
# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
pygame.mixer.music.load('jungle.wav')
gameOverSound = pygame.mixer.Sound('gameover.wav')
FoodSound = pygame.mixer.Sound("alluminium.wav")
AlligatorSound = pygame.mixer.Sound("alligator growls.wav")
EagleSound = pygame.mixer.Sound("eagle sound.wav")
OwlSound = pygame.mixer.Sound("hiboux.wav")
SnakeSound = pygame.mixer.Sound("snake.wav")


#diminue volume
gameOverSound.set_volume(0.1)
FoodSound.set_volume(0.1)




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



#Import Element 
GoodFoodImages = {
	PLAYER_COLOR_GREEN: pygame.image.load("grasshoppergreen.png"),
	PLAYER_COLOR_RED: pygame.image.load("grasshopperred.png"),
	PLAYER_COLOR_YELLOW: pygame.image.load("grasshopperyellow.png"),
	PLAYER_COLOR_BLUE: pygame.image.load("grasshopperblue.png"),
}

CheeseImages = {
	PLAYER_COLOR_GREEN: pygame.image.load("cheesegreen.png"),
	PLAYER_COLOR_RED: pygame.image.load("cheesered.png"),
	PLAYER_COLOR_YELLOW: pygame.image.load("cheeseyellow.png"),
	PLAYER_COLOR_BLUE: pygame.image.load("cheeseblue.png"),
}
ChocolateImages = {
	PLAYER_COLOR_GREEN: pygame.image.load("chocoGreen.png"),
	PLAYER_COLOR_RED : pygame.image.load("chocoRed.png"),
	PLAYER_COLOR_YELLOW: pygame.image.load("chocoYellow.png"),
	PLAYER_COLOR_BLUE: pygame.image.load("chocoBlue.png"),
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

BadFoodItems = {
    "cheese": CheeseImages,
    "chocolate": ChocolateImages,
    "alligator": AlligatorImages,
    "owl": OwlImages,
    "snake": SnakeImages,
    "eagle": EagleImages
}

BadFoodSound = {
	"cheese": FoodSound,
	"chocolate": FoodSound,
	"alligator": AlligatorSound,
	"owl": OwlSound,
	"snake": SnakeSound,
	"eagle": EagleSound
}
#upload font type
font = pygame.font.Font("Tropiland.ttf", 48)

#set up background
backgroundImage = pygame.image.load('background.png')

# Resize background image to the screen size
backgroundImage = pygame.transform.scale(backgroundImage, windowSurface.get_size())

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
#insert our background to the screen
windowSurface.blit(backgroundImage, (0,0))
#text element for the game
drawText('Jungle Chameleon', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press enter to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
drawText(f'Lives: {LIVES}', font, windowSurface, WINDOWWIDTH - 150, 10)
pygame.display.update()
waitForPlayerToPressKey()

# Default game values
currentColor = PLAYER_COLOR_GREEN
topScore = 0
speedMultiplier = 1.0
while True:
	
	# Set up the start of the game.
	GoodFood = []
	#BadFood means chocolate and cheese but also predators
	BadFood = []
	LIVES = 3
	score = 0
	playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT -80)
	moveLeft = moveRight = False
	reverseCheat = slowCheat = False
	PredatorAddCounter = 0
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

		#import keys 
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
		
			# call class
			randomColor = random.choice(list(GoodFoodImages.keys()))
			newGoodFood = GameElement(WINDOWWIDTH, WINDOWHEIGHT, randomColor, random.randint(0, WINDOWWIDTH - GoodFoodSize), 0 - GoodFoodSize, GoodFoodSize, random.randint(GOODFOODMINSPEED, GOODFOODMAXSPEED), GoodFoodImages[randomColor], FoodSound)


			GoodFood.append(newGoodFood)

		# --------- Adding baddies --------- 
		if not reverseCheat and not slowCheat:
			BadFoodAddCounter += 1

		if BadFoodAddCounter == ADDNEWBADFOODRATE:
			BadFoodAddCounter = 0
			BadFoodSize = random.randint(BADFOODMINSIZE, BADFOODMAXSIZE)
			
			#call class
			# Randomly pick a type (cheese, chocolate, or animal)
			randomType = random.choice(list(BadFoodItems.keys()))
			# Pick a random color or variant for the selected type
			randomColor = random.choice(list(BadFoodItems[randomType].keys()))
			sound = BadFoodSound[randomType]
			# Get the image corresponding to the type and color
			newBadFoodImage = BadFoodItems[randomType][randomColor]
			# Create the new bad food (or animal) GameElement
			newBadFood = GameElement(WINDOWWIDTH, WINDOWHEIGHT, randomType, random.randint(0, WINDOWWIDTH - BadFoodSize), 0 - BadFoodSize, BadFoodSize, random.randint(BADFOODMINSPEED, BADFOODMAXSPEED), newBadFoodImage, touchingSound=sound)
			
			BadFood.append(newBadFood)
		# --------- Movements ---------

		# Move the player around.
		if moveLeft and playerRect.left > 0:
			playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
		if moveRight and playerRect.right < WINDOWWIDTH:
			playerRect.move_ip(PLAYERMOVERATE, 0)

		# increase speed game due to score
		speedMultiplier = 1 + (score//10) * 0.4
		# Move the baddies down.
		for b in BadFood:
			if not reverseCheat and not slowCheat:
				b.rect.move_ip(0, b.speed*speedMultiplier)
			elif reverseCheat:
				b.rect.move_ip(0, -5)
			elif slowCheat:
				b.rect.move_ip(0, 1)
		for b in GoodFood:
			if not reverseCheat and not slowCheat:
				b.rect.move_ip(0, b.speed*speedMultiplier)
			elif reverseCheat:
				b.rect.move_ip(0, -5)
			elif slowCheat:
				b.rect.move_ip(0, 1)

		# Delete  element that have fallen past the bottom.
		for b in BadFood[:]:
			if b.rect.top > WINDOWHEIGHT:
				BadFood.remove(b)
		for b in GoodFood [:]:
			if b.rect.top > WINDOWHEIGHT:
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


		# Draw the score, top score and lives
		drawText('Score: %s' % (score), font, windowSurface, 10, 0)
		drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
		drawText("Lives: %s" % (LIVES), font, windowSurface, WINDOWWIDTH - 150, 10)

		# Draw each element.
		for b in BadFood:
			windowSurface.blit(b.surface, b.rect)
		for b in GoodFood:
			windowSurface.blit(b.surface, b.rect)

		pygame.display.update()

		# Check if any of the baddies have hit the player.
		if not playerHasHitBadFood(playerRect, BadFood):
			if LIVES <= 0:
				topScore = GameOver(score, topScore)
				break
		# Check if any good food have hit the player
		collision_result = playerHasHitGoodFood(playerRect, GoodFood, currentColor)
		if collision_result == "wrong":
			LIVES -= 1
			if LIVES > 0:
				pass
			elif LIVES <= 0:
				if score > topScore:
					topscore = score
				topScore = GameOver(score, topScore)
				break
		elif collision_result == "match":
			score += 1

		mainClock.tick(FPS)


	
