import random
import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import time

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)


# Game Variables
cx, cy = 250, 250
magenta = (255, 0, 255)
score = 0
timeStart = 0
totalTime = 120
lvl1Time = 30
lvl1RangeX = 128 #range in pixels
lvl1RangeY = 72
lvl1Size = 100  #l/2 in px
lvl2Time = 15
lvl2RangeX = 256
lvl2RangeY = 144
lvl2Size= 75
cicleCount = 0

key = 0
setup = 0
#z distance 70cm
#total x pixels / total x at 70cm   1280px/80cm
#total y pixels / total y at 70cm   720px/50cm


# Loop
while key != 27:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if setup == 0:
        #setup
        cvzone.putTextRect(img, 'Setup', (550, 200), scale=4, offset=30, thickness=7)
        cvzone.putTextRect(img, f'Sit at 1m distance from camera', (375, 475), scale=2, offset=20)
        cvzone.putTextRect(img, f'Align your shoulder with the DOT', (370, 550), scale=2, offset=20)
        cvzone.putTextRect(img, 'Press Scacebar to start', (460, 625), scale=2, offset=10)
        cv2.circle(img, (640, 360), 30, magenta, cv2.FILLED)
        cv2.circle(img, (640, 360), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (640, 360), 20, (255, 255, 255), 2)
        cv2.circle(img, (640, 360), 30, (50, 50, 50), 2)
        if key == 32:
            timeStart = time.time()
            score = 0
            setup = 1
            cx = random.randint(640-lvl1RangeX, 640+lvl1RangeX)
            cy = random.randint(360-lvl1RangeY, 360+lvl1RangeY)
    else:
        #game start
        #lvl1
        if score < 5:
            hands = detector.findHands(img, draw=False)
            #draws rectangle
            cv2.rectangle(img, (cx-lvl1Size, cy-lvl1Size), (cx+lvl1Size, cy+lvl1Size), (255, 0, 255), 3)
            if hands:
                lmList = hands[0]['lmList']
                wristX, wristY =lmList[0][:2]
                #draws DOT on wrist position
                cv2.circle(img, (wristX, wristY), 10, magenta, cv2.FILLED)

                #if wrist position fits box, start 2s counDown, after that increase score and reset timers
                if cx-lvl1Size<wristX<cx+lvl1Size and cy-lvl1Size<wristY<cy+lvl1Size:
                    if time.time()-countDown > 2:
                        score +=1
                        countDown=time.time()
                        cx = random.randint(640-lvl1RangeX, 640+lvl1RangeX)
                        cy = random.randint(360-lvl1RangeY, 360+lvl1RangeY)
                else:
                    countDown=time.time()
        #lvl2
        if score >=5:
            print("lvl2")
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        timeStart = time.time()
        score = 0

