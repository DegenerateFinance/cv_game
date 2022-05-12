import random
import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import time

import csv


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
lvl1Size = 75  #l/2 in px
lvl2Score = 6
lvl2Time = 20
lvl2RangeX = 256
lvl2RangeY = 144
lvl2Size= 50
cicleCount = 0

key = 0
setup = 0

#setup variables
#z distance 70cm
#total x pixels / total x at 70cm   1280px/80cm
#total y pixels / total y at 70cm   720px/50cm
px2cmX= 1/16
px2cmY= 1/14.4
#support variables
countDown = 0
timeZero = 0
timeOne = 0
wrist0x = 0
wrist0y = 0
wrist1x = 0
wrist1y = 0
maxSpeed = 0
maxAcc = 0
# Game Loop
with open ('file.csv', 'w', newline='') as csvfile:
    fieldnames= ['Score','Time Spent','PositionX(px)','PositionY(px)', 'maxSpeed(cm/s)', 'maxAcceleration(cm/s²)']
    thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    thewriter.writeheader()
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
                maxSpeed = 0
                maxAcc = 0
                cx = random.randint(640-lvl1RangeX, 640+lvl1RangeX)
                cy = random.randint(360-lvl1RangeY, 360+lvl1RangeY)
        if setup == 1:
            #game start
            #lvl1
            if score < lvl2Score:
                hands = detector.findHands(img, draw=False)
                if time.time()-timeStart <= lvl1Time:
                    #draws rectangle
                    cv2.rectangle(img, (cx-lvl1Size, cy-lvl1Size), (cx+lvl1Size, cy+lvl1Size), (255, 0, 255), 3)
                    #game HUD
                    cvzone.putTextRect(img, f'Score: {str(score).zfill(2)}', (60, 75), scale=3, offset=20)
                    cvzone.putTextRect(img, f'Time: {int(lvl1Time+timeStart-time.time())}',
                                       (1000, 125), scale=3, offset=20)
                    if hands:
                        lmList = hands[0]['lmList']
                        wristX, wristY =lmList[0][:2]
                        cicleCount += 1
                        if cicleCount % 3 == 0:
                            timeZero=time.time()
                            wrist0x=wristX
                            wrist0y=wristY
                        if cicleCount % 3 == 1:
                            timeOne=time.time()-timeZero
                            wrist1x=wristX-wrist0x
                            wrist1y=wristY-wrist0y
                            wristOne=math.sqrt((wrist1x*px2cmX)**2+(wrist1y*px2cmY)**2) #distance from points cm
                            speed1=round(wristOne/timeOne, 3)   #speed cm/s
                            if speed1 > maxSpeed:
                                maxSpeed = speed1
                        if cicleCount % 3 == 2:
                            timeTwo=time.time()-timeZero
                            wrist2x=wristX-wrist1x
                            wrist2y=wristY-wrist1y
                            wristTwo=math.sqrt((wrist2x*px2cmX)**2+(wrist2y*px2cmY)**2) #distance from points cm
                            speed2=round(wristTwo/(timeTwo-timeOne), 2)
                            Acceleration = round(abs((speed2-speed1)/(timeTwo-timeOne)),2)   #Acc in cm/s²
                            if Acceleration > maxAcc:
                                maxAcc = Acceleration
                        #draws DOT on wrist position
                        cv2.circle(img, (wristX, wristY), 10, magenta, cv2.FILLED)

                        #if wrist position fits box, start 2s counDown, after that increase score and reset timers
                        if cx-lvl1Size<wristX<cx+lvl1Size and cy-lvl1Size<wristY<cy+lvl1Size:
                            if time.time()-countDown > 2:
                                score +=1
                                #export data
                                print (score, round(time.time()-timeStart, 3), wristX, wristY, maxSpeed, maxAcc)
                                thewriter.writerow({'Score':score,'Time Spent':round(time.time()-timeStart, 3),'PositionX(px)':wristX,'PositionY(px)':wristY, 'maxSpeed(cm/s)':maxSpeed, 'maxAcceleration(cm/s²)':maxAcc})
                                timeStart = time.time()
                                countDown=time.time()
                                maxSpeed = 0
                                maxAcc = 0
                                cx = random.randint(640-lvl1RangeX, 640+lvl1RangeX)
                                cy = random.randint(360-lvl1RangeY, 360+lvl1RangeY)
                                if score >=5:
                                    cx = random.randint(640-lvl2RangeX, 640+lvl2RangeX)
                                    cy = random.randint(360-lvl2RangeY, 360+lvl2RangeY)
                        else:
                            countDown=time.time()
                else:
                    #time is up, game over
                    setup = 2
                    timeStart=time.time()
            #lvl2
            if score >=lvl2Score:
                hands = detector.findHands(img, draw=False)
                if time.time()-timeStart <= lvl2Time:
                    #draws rectangle
                    cv2.rectangle(img, (cx-lvl2Size, cy-lvl2Size), (cx+lvl2Size, cy+lvl2Size), (255, 0, 255), 3)
                    #game HUD
                    cvzone.putTextRect(img, f'Score: {str(score).zfill(2)}', (60, 75), scale=3, offset=20)
                    cvzone.putTextRect(img, f'Time: {int(lvl2Time+timeStart-time.time())}',
                                       (1000, 125), scale=3, offset=20)
                    if hands:
                        lmList = hands[0]['lmList']
                        wristX, wristY =lmList[0][:2]
                        cicleCount += 1
                        if cicleCount % 3 == 0:
                            timeZero=time.time()
                            wrist0x=wristX
                            wrist0y=wristY
                        if cicleCount % 3 == 1:
                            timeOne=time.time()-timeZero
                            wrist1x=wristX-wrist0x
                            wrist1y=wristY-wrist0y
                            wristOne=math.sqrt((wrist1x*px2cmX)**2+(wrist1y*px2cmY)**2) #distance from points cm
                            speed1=round(wristOne/timeOne, 3)   #speed cm/s
                            if speed1 > maxSpeed:
                                maxSpeed = speed1
                        if cicleCount % 3 == 2:
                            timeTwo=time.time()-timeZero
                            wrist2x=wristX-wrist1x
                            wrist2y=wristY-wrist1y
                            wristTwo=math.sqrt((wrist2x*px2cmX)**2+(wrist2y*px2cmY)**2) #distance from points cm
                            speed2=round(wristTwo/(timeTwo-timeOne), 2)
                            Acceleration = round(abs((speed2-speed1)/(timeTwo-timeOne)),2)   #Acc in cm/s²
                            if Acceleration > maxAcc:
                                maxAcc = Acceleration
                        #draws DOT on wrist position
                        cv2.circle(img, (wristX, wristY), 10, magenta, cv2.FILLED)

                        #if wrist position fits box, start 2s counDown, after that increase score and reset timers
                        if cx-lvl2Size<wristX<cx+lvl2Size and cy-lvl2Size<wristY<cy+lvl2Size:
                            if time.time()-countDown > 2:
                                score +=1
                                #export data
                                print (score, round(time.time()-timeStart, 3), wristX, wristY)
                                thewriter.writerow({'Score':score,'Time Spent':round(time.time()-timeStart, 3),'PositionX(px)':wristX,'PositionY(px)':wristY, 'maxSpeed(cm/s)':maxSpeed, 'maxAcceleration(cm/s²)':maxAcc})
                                timeStart = time.time()
                                countDown=time.time()
                                maxSpeed = 0
                                maxAcc = 0
                                cx = random.randint(640-lvl2RangeX, 640+lvl2RangeX)
                                cy = random.randint(360-lvl2RangeY, 360+lvl2RangeY)
                        else:
                            countDown=time.time()
                else:
                    #time is up, game over
                    setup = 2
                    timeStart=time.time()
        if setup == 2:
            cvzone.putTextRect(img, 'Game Over', (400, 400), scale=5, offset=30, thickness=7)
            cvzone.putTextRect(img, f'Your Score: {score}', (450, 500), scale=3, offset=20)
            cvzone.putTextRect(img, 'Press R to restart', (460, 575), scale=2, offset=10)


        cv2.imshow("Image", img)
        key = cv2.waitKey(1)

        if key == ord('r'):
            setup = 0
            score = 0

