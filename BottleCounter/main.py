import cv2
import numpy as np

cap = cv2.VideoCapture("video.mp4")
low_red = np.array([170,50,50], np.uint8)
high_red = np.array([180,255,255], np.uint8)
count = 0
control = False
while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low_red, high_red)
    cv2.line(frame,(700,0),(700,720),(0,0,255),3)
    cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    for cnt in cnts:
        x,y,w,h = cv2.boundingRect(cnt)
        if w>100 and h>200:
            cx = int(x+w/2)
            cy = int(y+h/2)
            if cx>670 and cx<730:
                if cx<700:
                    control = True
                if cx>700 and control:
                    control = False
                    count += 1
                cv2.circle(frame,(cx,cy),20,(0,0,0),-1)
    cv2.putText(frame,f'Counter:{count}',(0,60),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()