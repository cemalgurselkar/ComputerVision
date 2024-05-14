import cv2
import numpy as np

image = cv2.imread('data/cat_img1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
CatCascade = cv2.CascadeClassifier('CasCade/haarcascade_frontalcatface.xml')
face_rect = CatCascade.detectMultiScale(gray)
for (x,y,w,h) in face_rect:
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),5)

cv2.imshow('image',image)
cv2.waitKey(0)

"""
Buradak Cascade kullanımı ile ilgili bir araştırma ve pratik yaptım. Nesne tespiti için (eğer hsv yöntemine gerek yoksa) gray üzerinden işlemler yapılacağı. 
"""