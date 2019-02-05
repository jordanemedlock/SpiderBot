from adafruit_servokit import ServoKit
from spider import *

kit = ServoKit(channels=16)

left_front_elbow = Elbow(kit, 8)
left_front_shoulder = Shoulder(kit, 9)
left_middle_elbow = Elbow(kit, 10)
left_middle_shoulder = Shoulder(kit, 11)
left_back_elbow = Elbow(kit, 12)
left_back_shoulder = Shoulder(kit, 13)

right_front_elbow = Elbow(kit, 0)
right_front_shoulder = Shoulder(kit, 1)
right_middle_elbow = Elbow(kit, 2)
right_middle_shoulder = Shoulder(kit, 3)
right_back_elbow = Elbow(kit, 4)
right_back_shoulder = Shoulder(kit, 5)

left_front = Leg(left_front_elbow, left_front_shoulder)
left_middle = Leg(left_middle_elbow, left_middle_shoulder)
left_back = Leg(left_back_elbow, left_back_shoulder)

right_front = Leg(right_front_elbow, right_front_shoulder)
right_middle = Leg(right_middle_elbow, right_middle_shoulder)
right_back = Leg(right_back_elbow, right_back_shoulder)

left = Side(left_front, left_middle, left_back)
right = Side(right_front, right_middle, right_back)

spider = Spider(left, right)

