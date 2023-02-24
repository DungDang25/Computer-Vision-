import cv2 as cv
import time
import numpy as np
import HandtrackingModuel as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

###############################
wCam , hCam = 1280, 720
###############################

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv.circle(img, (x1,y1), 15, (255,0,255), cv.FILLED)
        cv.circle(img, (x2,y2), 15, (255,0,255), cv.FILLED)
        cv.line(img, (x1,y1),(x2,y2), (255,0,255), 3)
        cv.circle(img, (cx,cy), 15, (255,0,255), cv.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)
        #Hand range 50 - 175
        # Volume range -63.5 - 0

        vol = np.interp(length, [25, 100], [-63.5, 0])
        # print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        cv.putText(img, f'Length: {float(length)}', (350,50), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
        if length < 50:
            cv.circle(img, (cx,cy), 15, (0,255,0), cv.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}', (40,50), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    cv.imshow("Img", img)
    cv.waitKey(1)

    