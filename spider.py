import time
from collections import namedtuple

class Joint():
	def __init__(self, kit, channel, actuation_range=120, invert=False, range_limit=None):
		self.servo = kit.servo[channel]
		self.servo.actuation_range = actuation_range
		self.invert = invert
		self.range_limit = range_limit if range_limit else (0, actuation_range)

	def goto(self, value):
		"""value is between -1 and 1"""
		lower = self.range_limit[0]
		higher = self.range_limit[1]
		value = (value + 1)/2
		value = (1 - value) if self.invert else value
		angle = value * (higher - lower) + lower
		self.servo.angle = angle

class Elbow(Joint):
	def up(self):
		self.goto(0.5)
	def down(self):
		self.goto(-0.75)
	def middle(self):
		self.goto(0)

class Shoulder(Joint):
	def forward(self):
		self.goto(0.25)
	def backward(self):
		self.goto(-0.25)
	def middle(self):
		self.goto(0)

class Leg():
	def __init__(self, elbow, shoulder):
		self.elbow = elbow
		self.shoulder = shoulder

	def forward(self):
		self.shoulder.forward()

	def backward(self):
		self.shoulder.backward()

	def up(self):
		self.elbow.up()

	def down(self):
		self.elbow.down()

	def elbow_to(self, value):
		self.elbow.goto(value)

	def shoulder_to(self, value):
		self.shoulder.goto(value)

	def middle_all(self):
		self.elbow.middle()
		self.shoulder.middle()

	def middle_elbow(self):
		self.elbow.middle()

	def middle_shoulder(self):
		self.shoulder.middle()

	def to_state(self, state):
		self.shoulder.goto(state.shoulder)
		self.elbow.goto(state.elbow)


State = namedtuple('State', ['left', 'right'])
SideState = namedtuple('SideState', ['front', 'middle', 'back'])
LegState = namedtuple('LegState', ['elbow', 'shoulder'])
up = 0.5
down = -0.9
back = -0.25
forward = 0.25
point_a = LegState(up, back) 		# up back
point_b = LegState(up, forward) 	# up forward
point_c = LegState(down, forward) 	# down forward
point_d = LegState(down, back) 		# down back

state_1 = SideState(point_c, point_a, point_c)
state_2 = SideState(point_d, point_b, point_d)
state_3 = SideState(point_d, point_c, point_d)
state_4 = SideState(point_a, point_c, point_a)
state_5 = SideState(point_b, point_d, point_b)
state_6 = SideState(point_c, point_d, point_c)

walk_cycle = [state_1, state_2, state_3, state_4, state_5, state_6]


def walk_state_forward(state):
	forward, up = state
	return up, not forward

def walk_state_backward(state):
	forward, up = state
	return not up, forward

def opposite(state):
	forward, up = state
	return not forward, not up

class Side():
	def __init__(self, front, middle, back):
		self.front = front
		self.middle = middle
		self.back = back


	def to_state(self, state):
		self.front.to_state(state.front)
		self.middle.to_state(state.middle)
		self.back.to_state(state.back)

	def middle_elbows(self):
		self.front.middle_elbow()
		self.middle.middle_elbow()
		self.back.middle_elbow()

	def middle_shoulders(self):
		self.front.middle_shoulder()
		self.middle.middle_shoulder()
		self.back.middle_shoulder()

	def middle_all(self):
		self.middle_elbows()
		self.middle_shoulders()

	def elbows_to(self, value):
		self.front.elbow_to(value)
		self.middle.elbow_to(value)
		self.back.elbow_to(value)

	def shoulders_to(self, value):
		self.front.shoulder_to(value)
		self.middle.shoulder_to(value)
		self.back.shoulder_to(value)


class Spider():
	def __init__(self, left, right):
		self.right = right
		self.left = left
		self.left_state = 2
		self.right_state = 5

	def middle_elbows(self):
		self.left.middle_elbows()
		self.right.middle_elbows()

	def middle_shoulders(self):
		self.left.middle_shoulders()
		self.right.middle_shoulders()

	def middle_all(self):
		self.middle_elbows()
		self.middle_shoulders()

	def shoulders_to(self, value):
		self.left.shoulders_to(value)
		self.right.shoulders_to(value)

	def elbows_to(self, value):
		self.left.elbows_to(value)
		self.right.elbows_to(value)

	def walk_once(self):
		left_state = walk_cycle[self.left_state]
		right_state = walk_cycle[self.right_state]
		self.left.to_state(left_state)
		self.right.to_state(right_state)
		self.left_state = (self.left_state + 1) % 6
		self.right_state = (self.right_state + 1) % 6

	def walk(self, states_per_second):
		wait_time = 1 / states_per_second
		while True:
			self.walk_once()
			time.sleep(wait_time)



