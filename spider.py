
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
		value = (1 - value) if invert else value
		angle = value * (higher - lower) + lower
		self.servo.angle = angle

class Elbow(Joint):
	def up(self):
		self.goto(1)
	def down(self):
		self.goto(-1)
	def middle(self):
		self.goto(0)

class Shoulder(Joint):
	def forward(self):
		self.goto(1)
	def backward(self):
		self.goto(-1)
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

	def middle_all(self):
		self.elbow.middle()
		self.shoulder.middle()

	def to_state(self, state):
		forward, up = state
		if forward:
			self.forward()
		else:
			self.backward()
		if up:
			self.up()
		else:
			self.down()


forward_up = (True, True)
forward_down = (True, False)
backward_up = (False, True)
backward_down = (False, False)

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


	def to_walk_state(self, state):
		"""stage is defined by what the middle does"""
		other_state = opposite(state)
		self.front.to_state(other_state)
		self.middle.to_state(state)
		self.back.to_state(other_state)

class Spider():
	def __init__(self, left, right):
		self.right = right
		self.left = left
