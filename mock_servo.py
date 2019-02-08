class MockServo():
	def __init__(self, name, actuation_range=120):
		self.name = name
		self._actuation_range = actuation_range
		self._angle = 0

	def get_actuation_range(self):
		return self._actuation_range

	def set_actuation_range(self, value):
		self._actuation_range = value

	actuation_range = property(get_actuation_range, set_actuation_range)

	def get_angle(self):
		return self._angle

	def set_angle(self, value):
		print(self.name + ".angle=" + str(value))
		self._angle = value

	angle = property(get_angle, set_angle)

class MockKit():
	def __init__(self, servo):
		self.servo = servo
mock_kit = MockKit([MockServo(str(i)) for i in range(16)])
