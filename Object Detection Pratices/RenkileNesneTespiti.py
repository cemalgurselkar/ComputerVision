import cv2
import numpy as np
from collections import deque

#BU ÇOK ÖNEMLİ ÇALIŞILACAK!!!

#nesne merkezini depolayacak veri tipi
buffer_size = 16
pts = deque(maxlen=buffer_size)

#mavi renk aralığı HSV
blueLower = (84,98,0)
blueUpper = (179,255,255)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret:
        blurred = cv2.GaussianBlur(frame,(11,11),0)
        hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, blueLower, blueUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        contours, hierarch = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # sadece iki parametresi vardır.
        if contours is not None:
            print("Kontür bulunamadı")
        center = None
        if len(contours) > 0:
            # en büyük kontörü al
            c = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(c)
            ((x,y),(width,height), rotation) = rect
            s = 'x: {}, y: {}, width: {}, height: {}'.format(np.round(x),np.round(y),np.round(width),np.round(height))
            print(s)

            box = cv2.boxPoints(rect)
            box = np.int64(box)
            M = cv2.moments(box)
            center = (int(M['m10']/M['m00']),int(M['m01']/M['m00']))
            cv2.drawContours(frame,[box],0,(0,255,255),2)
            cv2.circle(frame,center,5,(0,0,255),-1)
            cv2.putText(frame,s,(50,50),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)

        pts.appendleft(center)
        for i in range(1, len(pts)):
            if pts[i-1] is None or pts[i] is None: continue
            cv2.line(frame,pts[i-1],pts[i],(0,255,0),3)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

"""
En önemli algoritmalardan birisidir. Burada, belirlediğimiz nesneyi rengi sayesinde tespit edebiliriyorz. HSV ve Kontur işlemleri sayesinde.
Görüntüyü mavi renk için alt ve üst sınırlar belirleyip binary mask kullandık. Ardından beliren nesne için kontur işlemleri uyguladık.
Ardından, nesnenin ortasına bir nokta yerleştirdik ve sonrasında her hareketini takip etmek için bir line çizdik. amaç, merkez her hareket ettiğinde  arkasından yeşil bir çizgi çizilecek, bu sayede nesne hareketi takip edilecek.

"""