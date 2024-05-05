import cv2
import numpy as np

def forImage():
    image = cv2.imread('data/barcelona.jpg', 0)
    face_cascade = cv2.CascadeClassifier('CasCade/haarcascade_frontalface_default.xml')
    face_rect = face_cascade.detectMultiScale(image, minNeighbors=7, minSize=(30, 30))
    for (x, y, w, h) in face_rect:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 10)
    cv2.imshow('Barcelona', image)
    cv2.waitKey(0)

def forVİdeo():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    while True:
        ret, frame = cap.read()
        faceDetect = cv2.CascadeClassifier('CasCade/haarcascade_frontalface_default.xml')
        face_rect = faceDetect.detectMultiScale(frame, minNeighbors=15 ,minSize=(30, 30)) #minNeighbors = birçok nesnenin olduğu yerde doğru sonucu arttırmak için kullanılır. artması doğru sonucu pozitif yönde etkiler.
        for (x, y, w, h) in face_rect:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 10)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

forVİdeo()