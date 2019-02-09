# A wrapper library written to easily interface a sixAxis (ps3) controller to a system with pygame installed

import pygame
import time
import os

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ['SDL_VIDEODRIVER'] = 'dummy'



class SixAxis:
	connected = False
	
	def __init__(self):
		errorStr = "no sixAxis controller initialized. Check to make sure it is connected and correctly paired."
		searchStr = ""
		
		# init pygame
		pygame.init()
		pygame.display.set_mode((1,1))
		
		numJoysticks = pygame.joystick.get_count()
		for i in range(0, numJoysticks):
			name = pygame.joystick.Joystick(i).get_name()
			if (name.find(searchStr) != -1):
				pygame.joystick.Joystick(i).init()
				print(pygame.joystick.Joystick(i).get_name() + " initialized")
				self.connected = True
				return
		# no sixAxis controller can be found
		print(errorStr)
		pygame.joystick.quit()
	
	# button map
	buttons = {
		0: 'x',
		1: 'o',
		2: 'triangle',
		3: 'square',
		4: 'L1',
		5: 'R1',
		6: 'unknown 1',
		7: 'unknown 2',
		8: 'select',
		9: 'start',
		10: 'ps',
		11: 'L3',
		12: 'R3',
		13: 'dpad_up',
		14: 'dpad_down',
		15: 'dpad_left',
		16: 'dpad_right'
	}

	# axis map
	# up and right are positive for analog sticks L3 and r3
	# tilting forward/right is positive
	# button axes are force sensors with values 0-1, 0 being when lightly pressed, 1 when pressed in fully
	# axis 7 seems unused...
	axes = {
		0: ['L3_horizontal', 1],
		1: ['L3_vertical', -1],
		2: ['L2', 1],
		3: ['R3_horizontal', -1],
		4: ['R3_vertical', 1], # value 0 when controller is level. this is rotation along axis going through centre of controller front to back
		5: ['R2', 1], # value 0 when controller is level. this is rotation along axis going through centre of controller left to right
		6: ['unknown 3', -1], # value -1 when level, 1 when flipped. this just combines axes 4 and 5
		8: ['unknown 4', 1],
		9: ['unknown 5', 1],
		10: ['unknown 6', 1],
		11: ['unknown 7', 1],
		12: ['unknown 8', 1],
		13: ['unknown 9', 1],
		14: ['unknown 10', 1],
		15: ['unknown 11', 1],
		16: ['unknown 12', 1],
		17: ['unknown 13', 1],
		18: ['unknown 14', 1],
		19: ['unknown 15', 1]
	}
	
	def get_events(self):
		eventList = {}
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.JOYBUTTONDOWN:
				eventList[self.buttons[event.button]] = { 'axisValue': -1 }
			if event.type == pygame.JOYAXISMOTION:
				eventList[self.axes[event.axis][0]] = { 'axisValue': self.axes[event.axis][1] * event.value }
		return eventList
		

# example output
'''
while True:
	events = sixAxis.getEvents()
	if events != None:
		for buttonName in events:
			print "button: " + buttonName + " axisValue: " + str(events[buttonName]['axisValue'])
	time.sleep(0.1)
'''
