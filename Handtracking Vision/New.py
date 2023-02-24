import cv2 as cv 
import time
import os 
from Modules import HandTrackingModule as HTM

#####################
wCam, hCam = 640, 480
#####################

pTime = 0
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = HTM.handDetector(maxHands=2,detectionCon=0.8)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img, handsType = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)

    
    if len(lmList) != 0:
        fingers = []

        if (len(handsType) <= 1):
            if (handsType[0] == 'Right'):
                # Thumb 
                if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            if (handsType[0] == 'Left'):
                # Thumb 
                if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        fingersUp = fingers.count(1)
        print(fingersUp)
            


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}',(10,70), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    cv.imshow("Image", img)
    cv.waitKey(1)