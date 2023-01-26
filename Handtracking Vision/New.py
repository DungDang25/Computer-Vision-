import cv2 as cv 
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        ## print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

                # For hand landmark coordinates
                # for id, lm in enumerate(handLms.landmark):
                #     ##print(id, lm)
                #     h, w, c= img.shape
                #     cx, cy = int(lm.x*w), int(lm.y*h)
                #     print(id, cx, cy)
                #     if id == 0:
                #         cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)
        return img

def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)

    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)),(10,70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv.imshow("Image", img)
        cv.waitKey(1)


if __name__ == "__main__":
    main()