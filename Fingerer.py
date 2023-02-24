import cv2 as cv
import time
import os
import HandtrackingModuel as htm

wCam , hCam = 1280, 720

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img, HandTypes = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList)

    fingers = []
    if len(lmList) != 0:
        if lmList[tipIds[0]][1] >= lmList[tipIds[0]-1][1] and HandTypes[0] == 'Left':
            fingers.append(1)
        elif lmList[tipIds[0]][1] <= lmList[tipIds[0]-1][1] and HandTypes[0] == 'Right':
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

    print(fingers.count(1))
    #print(HandTypes[0])

    cv.imshow("Image", img)
    cv.waitKey(1)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}', (40,50), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)