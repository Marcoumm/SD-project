import pygame, random, sys
from pygame.locals import *

from FPS import FPS

#program basic setting
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 140, 0)
FPS = 60
BACKGROUNDCOLOR = (210, 255, 200)
#create a variable live, player has 3 lives at the beginning and max 6 lives during the game
LIVES = 3
MAX_LIVES = 6

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
SPOT_DURATION = 5000
BUG_MOVE_DURATION = 3000
BUG_MOVE_INTENSITY = 5

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
				if event.key == K_SPACE:  # Continue only if barre espace is pressed.
					return
				

def drawText(text, font, surface, center_x, center_y):
	textobj = font.render(text, 1, TEXTCOLOR)
	textrect = textobj.get_rect()
	textrect.center = (center_x, center_y)
	surface.blit(textobj, textrect)


def playerHasHitBadFood(playerRect, BadFood):
	global LIVES, MAX_LIVES, doublePointsActive, doublePointsTimer, spotVisible, spotTime, bugMoveActive, bugMoveTimer
	for b in BadFood[:]:
		if isinstance(b, GameElement):
			if playerRect.colliderect(b.rect):
				b.playTouchingSound()
				if b.color == "bonus":  # Check if it's a bonus item
					if LIVES < MAX_LIVES:
						LIVES += 1
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
					LIVES -= 1
				BadFood.remove(b)
				
				if LIVES > 0:
					return False
				break
	return None

		# score with match color good food with player color
def playerHasHitGoodFood(playerRect, GoodFood, currentColor):
	for food in GoodFood:
		if isinstance(food, GameElement):
			if playerRect.colliderect(food.rect) and not food.isTouched():
				food.touch()
				if food.color == currentColor:
					GoodFood.remove(food)
					BonusSound.play()
					return "match"
				
				else:
					GoodFood.remove(food)
					MalusSound.play()
					return "wrong"
	return None

#function malu spot
def applySpotMalusEffect(WindowSurface):
    global spotVisible, spotTime, Spot
    
    if spotVisible and Spot:
        # Calculate how long the effect has been active
        currentTime = pygame.time.get_ticks()
        elapsedTime = currentTime - spotTime
        
        # Check if the effect should still be visible (e.g., for 3 seconds)
        if elapsedTime < SPOT_DURATION:
            # Draw the spotmalus PNG image at the center of the screen (or wherever you want)
            spot_rect = Spot.get_rect(center=(windowSurface.get_width() // 2, windowSurface.get_height() // 2))  # Example: center the spot
            windowSurface.blit(Spot, spot_rect)
        else:
            # Once the time has passed, stop showing the effect
            spotVisible = False
def applyBugMalusEffect(windowSurfacte):
	global bugMoveActive, bugMoveTimer, Malus

	if bugMoveActive :
		currentTime = pygame.time.get_ticks()
		if currentTime - bugMoveTimer >= BUG_MOVE_DURATION:
			bugMoveActive = False


#function for bonus
def update():
    global doublePointsActive, doublePointsTimer
    if doublePointsActive:
        # Check that 5 seconds passed
        if pygame.time.get_ticks() - doublePointsTimer >= 8000:
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
	pygame.display.update()
	
	#wait player to press space
	waitForPlayerToPressKey()
	#stop sound
	gameOverSound.stop()

	return topScore

def draw_lives():
	for i in range(LIVES):
		
		windowSurface.blit(flower, (WINDOWWIDTH - (LIVES * flower_width + (LIVES - 1) * 10) - 20 + i * (flower_width + 10), 20))

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Jungle')
pygame.mouse.set_visible(False)


# Set up sounds.
pygame.mixer.music.load('jungle.wav')
gameOverSound = pygame.mixer.Sound('gameover.wav')
MalusSound = pygame.mixer.Sound("malus.wav")
BonusSound = pygame.mixer.Sound("bonus.wav")
AlligatorSound = pygame.mixer.Sound("Alligator.wav")
EagleSound = pygame.mixer.Sound("Eagle.wav")
OwlSound = pygame.mixer.Sound("Owl.wav")
SnakeSound = pygame.mixer.Sound("snake.wav")

#diminue volume
gameOverSound.set_volume(0.1)
MalusSound.set_volume(0.8)
AlligatorSound.set_volume(0.3)
EagleSound.set_volume(0.3)
OwlSound.set_volume(0.3)
SnakeSound.set_volume(0.3)
# Set up images.
#flower
flower = pygame.image.load("pinkflower.png")
flower = pygame.transform.scale(flower, (40, 40))
flower_width = flower.get_width()
flower_height = flower.get_height()

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

Bonus = pygame.image.load("heart.png")
DoublePointsBonus = pygame.image.load("plus.png")
Malus = pygame.image.load("mushroom.png")
SpotMalus = pygame.image.load("tache.png")
Spot = pygame.image.load("tache.png").convert_alpha()
Spot = pygame.transform.scale(Spot, (600, 600))

#Import Element 
GoodFoodImages = {
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

BadFoodItems = {
    "alligator": AlligatorImages,
    "owl": OwlImages,
    "snake": SnakeImages,
    "eagle": EagleImages,
	"bonus": Bonus,
	"doublebonus": DoublePointsBonus,
	"malus": Malus,
	"spotmalus": SpotMalus
}

BadFoodSound = {
	"alligator": AlligatorSound,
	"owl": OwlSound,
	"snake": SnakeSound,
	"eagle": EagleSound,
	"bonus": BonusSound,
	"doublebonus": BonusSound,
	"malus": MalusSound,
	"spotmalus": MalusSound
}
#upload font type
font = pygame.font.Font("Tropiland.ttf", 48)
small_font = pygame.font.Font("Tropiland.ttf", 35)

#set up background
backgroundImage = pygame.image.load('background.png')

# Resize background image to the screen size
backgroundImage = pygame.transform.scale(backgroundImage, windowSurface.get_size())

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
#insert our background to the screen
windowSurface.blit(backgroundImage, (0,0))
#text element for the game
drawText('Jungle Chameleon', font, windowSurface, 300, 250)
drawText('Press space to start.', font, windowSurface, 300, 300)
pygame.display.update()
waitForPlayerToPressKey()

# Default game values
currentColor = PLAYER_COLOR_GREEN

topScore = 0

speedMultiplier = 1.0

while True:
	
	# Set up the start of the game.
	GoodFood = []
	#BadFood means predators / bonus and malus
	BadFood = []
	LIVES = 3
	score = 0
	doublePointsActive = False
	doublePointsTimer = 0
	spotVisible = False
	bugMoveActive = False
	bugMoveTimer = 0
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
			
			if spotVisible:
				windowSurface.blit(SpotMalus, (0, 0))

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
			newGoodFood = GameElement(WINDOWWIDTH, WINDOWHEIGHT, randomColor, random.randint(0, WINDOWWIDTH - GoodFoodSize), 0 - GoodFoodSize, GoodFoodSize, random.randint(GOODFOODMINSPEED, GOODFOODMAXSPEED), GoodFoodImages[randomColor], BonusSound)


			GoodFood.append(newGoodFood)

		# --------- Adding baddies --------- 
		if not reverseCheat and not slowCheat:
			BadFoodAddCounter += 1

		if BadFoodAddCounter == ADDNEWBADFOODRATE:
			BadFoodAddCounter = 0
			BadFoodSize = random.randint(BADFOODMINSIZE, BADFOODMAXSIZE)
			
			#call class
			randomType = random.choice(list(BadFoodItems.keys()))
			#malus and bonus haven't key color, separate them
			if randomType in ["bonus", "malus", "doublebonus", "spotmalus"]:
				newBadFoodImage = BadFoodItems[randomType]
				sound = BadFoodSound[randomType]
			else:
				randomColor = random.choice(list(BadFoodItems[randomType].keys()))
				sound = BadFoodSound[randomType]
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
		drawText('Score: %s' % (score), small_font, windowSurface, 85, 40)
		drawText('Top Score: %s' % (topScore), small_font, windowSurface, 110, 80)
		draw_lives()

		# Draw each element.
		for b in BadFood:
			windowSurface.blit(b.surface, b.rect)
		for b in GoodFood:
			windowSurface.blit(b.surface, b.rect)

		applySpotMalusEffect(windowSurface)
		applyBugMalusEffect(windowSurface)
		update()

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
			if doublePointsActive:
				score += 2
			else:
				score += 1

		

		mainClock.tick(FPS)

# max 6 vies
# texte sur l'affichage avec les chiffres 1234 liés aux couleurs
	
