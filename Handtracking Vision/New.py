import cv2 as cv 
import time
import os 
from Modules import HandTrackingModule as HTM
from spotify_local import SpotifyLocal

#####################
wCam, hCam = 640, 480
#####################

pTime = 0
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = HTM.handDetector(maxHands=2,detectionCon=0.8)

while True:
    success, img = cap.read()
    img, handsType = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)

    
    if len(lmList) != 0:

        countFingers = detector.countFingers(lmList, handsType)

        fingersUp = countFingers.count(1)
        print(fingersUp)
            

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}',(10,70), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    cv.imshow("Image", img)
    cv.waitKey(1)