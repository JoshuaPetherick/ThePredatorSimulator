#The file will hold all the main methods and bring the program together
# TODO: Random spawning - within an area (Prey and Predators)

# Additional files
from predator import Predator
from prey import Prey

# GUI
import sys 
import pygame
import random
pygame.init()

# Global Variables
window_size = width, height = 640, 480
screen = pygame.display.set_mode(window_size)
screen_colour = 34, 177, 76
my_font = pygame.font.SysFont("monospace", 16)

preyList = [] # List of Prey
predList = [] # List of Predators
labels = [] # List of Labels
buttons = [] # List of Buttons

def init(tempPreyList, tempPredList, match_percentage):
	#Load Window
	pygame.display.set_caption('The Predator Simulator')
	pygame.mouse.set_visible(1) #Debateable on whether it's neccesary
	# Load Assets
	## Objects
	new_prey()
	new_predator()
	## Labels
	labels.append(Label("#Simulation 1" , (480, 356)))
	labels.append(Label("Prey        " + str(tempPreyList), (480, 378)))
	labels.append(Label("Predators   " + str(tempPredList), (480, 400)))
	labels.append(Label("Match     " + str(match_percentage) + "%", (480, 422)))
	# Buttons
	buttons.append(Button("Start", (480,450)))
	buttons.append(Button("<", (578,378))) # Prey
	buttons.append(Button(">", (615,378)))
	buttons.append(Button("<", (578,400))) # Predators
	buttons.append(Button(">", (615,400)))
	buttons.append(Button("<", (558,422))) # Match Percentage
	buttons.append(Button(">", (615,422)))
	
def logic():
	# Logic
	for predator in predList:
		predator.move(preyList)
		for prey in preyList:
			prey.check_nearby(predator)
	for prey in preyList:
		prey.move()
		
def draw():
	# Render
	## Draw order
	screen.fill(screen_colour)
	### Objects
	for predator in predList:
		predator.draw(screen)
	for prey in preyList:
		prey.draw(screen)
	for label in labels:
		label.draw(screen)
	for button in buttons:
		button.draw(screen)
	## Actual Draw
	pygame.display.update()
	pygame.time.delay(33) # AVG 30FPS
		
def main():	
	running = True
	start = False
	simulation = 1
	
	tempPreyList = 1
	tempPredList = 1
	match_percentage = 80
	init(tempPreyList, tempPredList, match_percentage)
	
	while(running):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
				# Cycle through buttons
				if (check_collision(mouse_pos, buttons[0].get_pos())):
					if (start):
						for pred in predList:
							pred.reset(tempPredList, tempPreyList, match_percentage)
						for prey in preyList:
							prey.reset()
						updateArrays(tempPredList, tempPreyList)
						start = False
					else:
						# Technically start game
						for pred in predList:
							pred.select_logic(len(predList), len(preyList), match_percentage)
						start = True
				# Update Prey
				elif (check_collision(mouse_pos, buttons[1].get_pos())):
					if (start == False):
						if (len(preyList) > 1):
							preyList.remove(preyList[0])
					tempPreyList -= 1
					if (tempPreyList < 1):
						tempPreyList = 1
				elif (check_collision(mouse_pos, buttons[2].get_pos())): 
					if (start == False):
						new_prey()
					tempPreyList += 1
					if (tempPreyList > 9):
						tempPreyList = 9
				# Update Predators
				elif (check_collision(mouse_pos, buttons[3].get_pos())): 
					if (start == False):
						if (len(predList) > 1):
							predList.remove(predList[0])
					tempPredList -= 1
					if (tempPredList < 1):
						tempPredList = 1
				elif (check_collision(mouse_pos, buttons[4].get_pos())): 
					if (start == False):
						new_predator()
					tempPredList += 1
					if (tempPredList > 9):
						tempPredList = 9
				# Update Match Percentage
				elif (check_collision(mouse_pos, buttons[5].get_pos())):
					match_percentage -= 1
				elif (check_collision(mouse_pos, buttons[6].get_pos())):
					match_percentage += 1
				# Update label values
				labels[1].update("Prey        " + str(tempPreyList))
				labels[2].update("Predators   " + str(tempPredList))
				labels[3].update("Match     " + str(match_percentage) + "%")
			if event.type == pygame.QUIT: 
				# Stops the program running
				sys.exit()
				running = False
		
		if (start):
			logic()
			if(check_end_condition()):
				simulation = next_simulation(simulation, match_percentage, tempPreyList, tempPredList)
				updateArrays(tempPredList, tempPreyList)	
		draw()

class Label(object):
	def __init__(self, text, pos):
		self.pos = pos
		self.obj = my_font.render(text, 1, (0,0,0))
	
	def update(self, text):
		self.obj = my_font.render(text, 1, (0,0,0))
	
	def draw(self, screen):
		screen.blit(self.obj, self.pos)
		
class Button(object):
	def __init__(self, text, pos):
		size = len(text)*20
		self.text = my_font.render(text, 1, (0,0,0))
		self.pos = (pos[0]+(size/4), pos[1])
		self.rect = (pos[0],pos[1],size,18)
	
	def get_pos(self):
		return self.rect
	
	def draw(self, screen):
		pygame.draw.rect(screen, (212,208,200), self.rect)
		pygame.draw.rect(screen, (0,0,0), self.rect, 1)
		screen.blit(self.text, self.pos)
		
def check_collision(obj1, obj2):
	if((obj1[0] + obj1[2]) > obj2[0] and (obj1[1] + obj1[3]) > obj2[1] and
	obj1[0] < (obj2[0] + obj2[2]) and obj1[1] < (obj2[1] + obj2[3])):
		return True
	return False

def check_end_condition():
	for prey in preyList:
		temp_pos = prey.get_pos()
		for pred in predList:
			if (check_collision(prey.get_pos(), pred.get_pos())):
				return True
	for prey in preyList:	
		temp_pos = prey.get_pos()
		if (temp_pos[0] > 0 and temp_pos[1] > 0 and 
		temp_pos[0] < window_size[0] and temp_pos[1] < window_size[1]):
			return False
	return True

def updateArrays(tempPredList, tempPreyList):
		while (len(predList) < tempPredList):
			new_predator()
			predList[(len(predList)-1)].select_logic(tempPredList, tempPreyList, match_percentage)
		while (len(predList) > tempPredList):
			predList.remove(predList[(len(predList)-1)])
		while (len(preyList) < tempPreyList):
			new_prey()
		while (len(preyList) > tempPreyList):
			preyList.remove(preyList[(len(preyList)-1)])
	
def next_simulation(simulation, match_percentage, tempPreyList, tempPredList):
	labels[0].update("#Simulation " + str(simulation + 1)) # Move when required
	for pred in predList:
		result = False
		for prey in preyList:
			if (check_collision(prey.get_pos(), pred.get_pos())):
				result = True
		# Need to check result before adding
		pred.add_new_case(len(predList), len(preyList), result)
		pred.reset(tempPredList, tempPreyList, match_percentage)
	for prey in preyList:
		prey.reset()
	return simulation + 1

def new_predator():
	if (len(predList) < 9):
		x = random.randrange((window_size[0] - 40))
		y = random.randrange((window_size[1] - 40))
		while (y < 380):
			y = random.randrange((window_size[1] - 40))
		predList.append(Predator(pygame.image.load("images/predator.png").convert(), [x, y], window_size))

def new_prey():
	if (len(preyList) < 9):
		x = random.randrange((window_size[0] - 40))
		y = random.randrange((window_size[1] - 40))
		while (y > 300):
			y = random.randrange(window_size[1])
		preyList.append(Prey(pygame.image.load("images/prey.png").convert(), [x, y]))	
	
main()
