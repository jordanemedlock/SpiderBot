from spider import *
from sys import argv

try:
	from adafruit_servokit import ServoKit
	kit = ServoKit(channels=16)
except ImportError:
	from mock_servo import mock_kit
	kit = mock_kit

left_front_elbow = Elbow(kit, 8)
left_front_shoulder = Shoulder(kit, 9)
left_middle_elbow = Elbow(kit, 10, invert=True)
left_middle_shoulder = Shoulder(kit, 11)
left_back_elbow = Elbow(kit, 12, invert=True)
left_back_shoulder = Shoulder(kit, 13)

right_front_elbow = Elbow(kit, 0, invert=True)
right_front_shoulder = Shoulder(kit, 1, invert=True)
right_middle_elbow = Elbow(kit, 2)
right_middle_shoulder = Shoulder(kit, 3, invert=True)
right_back_elbow = Elbow(kit, 4)
right_back_shoulder = Shoulder(kit, 5, invert=True)

left_front = Leg(left_front_elbow, left_front_shoulder)
left_middle = Leg(left_middle_elbow, left_middle_shoulder)
left_back = Leg(left_back_elbow, left_back_shoulder)

right_front = Leg(right_front_elbow, right_front_shoulder)
right_middle = Leg(right_middle_elbow, right_middle_shoulder)
right_back = Leg(right_back_elbow, right_back_shoulder)

left = Side(left_front, left_middle, left_back)
right = Side(right_front, right_middle, right_back)

spider = Spider(left, right)


