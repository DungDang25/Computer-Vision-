import cv2 as cv 
import mediapipe as mp
import time
import HandtrackingModuel as htm

pTime = 0
cTime = 0
cap = cv.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    
    if len(lmList) != 0:
        print(lmList[0])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)),(10,70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv.imshow("Image", img)
    cv.waitKey(1)