from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)


kit.servo[4].actuation_range = 180
kit.servo[5].actuation_range = 180

kit.servo[3].actuation_range = 180
kit.servo[2].actuation_range = 180

kit.servo[1].actuation_range = 120
kit.servo[0].actuation_range = 120

while True:
    passing = False
    while passing == False:
        try:
            position = int(input("ANGLE: "))
            passing = True
        except:
            passing = False
    
    for i in range(9):
        if i != 10 and i != 11:
    	    kit.servo[i].angle = position

