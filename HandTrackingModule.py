import cv2
import mediapipe as mp
import numpy as np
import time
import math


class HandDetector():
    def __init__(self, mode=False, maxHands=2):
        self.mode = mode
        self.maxHands = maxHands
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIDS = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        try:
            if self.results.multi_hand_landmarks:
                for handLm in self.results.multi_hand_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(img, handLm, self.mpHands.HAND_CONNECTIONS)
            return img
        except Exception as e:
            print(f'Hand not found!!')

    def findPosition(self, img, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHands = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHands.landmark):
                h, w, c = img.shape
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        try:
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox.append([xmin, ymin, xmax, ymax])
        except Exception as e:
            return None, None
        return self.lmList, bbox

    def fingerUp(self):
        finger = []
        if self.lmList[self.tipIDS[0]][1] > self.lmList[self.tipIDS[0] - 1][1]:
            finger.append(1)
        else:
            finger.append(0)
        for i in range(1,5):
            if self.lmList[self.tipIDS[i]][2] > self.lmList[self.tipIDS[i] - 2][2]:
                finger.append(1)
            else:
                finger.append(0)
        return finger

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    detector = HandDetector()
    pTime = 0
    array = []
    distance = []
    while True:
        ret, frame = cap.read()
        frame = detector.findHands(frame)
        lmList, bbox = detector.findPosition(frame)
        if lmList:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            print(distance)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame,f'fps:{str(int(fps))}',(0,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

main()