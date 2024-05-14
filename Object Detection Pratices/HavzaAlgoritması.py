import cv2
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread('data/coins.jpg')
#Blurring
coin_blur = cv2.medianBlur(image, 15)
#Gray
coin_gray = cv2.cvtColor(coin_blur, cv2.COLOR_BGR2GRAY)
#Binary Threshold
ret, coin_threshold = cv2.threshold(coin_gray, 65, 255, cv2.THRESH_BINARY)

#Kontür işlemleri
contours, hierarchy = cv2.findContours(coin_threshold.copy(), cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(contours)):
    if hierarchy[0][i][3] == -1:
        cv2.drawContours(image, contours, i, (255, 0, 0), 3)

#açılma
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(coin_threshold, cv2.MORPH_OPEN, kernel, iterations=2)

#distance
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)

#resmi küçült
ret, sure_foreground = cv2.threshold(dist_transform, (0.4 * np.max(dist_transform)) , 255, cv2.THRESH_BINARY)
#Arka plan için resmi büyült
sure_background = cv2.dilate(opening, kernel, iterations=2)
sure_foreground = np.uint8(sure_foreground)
unknown = cv2.subtract(sure_background, sure_foreground)
#bağlantı

try:
    ret, marker = cv2.connectedComponents(sure_foreground)
    marker = marker + 1
    marker[unknown == 255] = 0
    marker = np.float32(marker) # Opencv ile çalışması için float türünde 32 bite çevrildi.
    marker = cv2.watershed(coin_blur, marker)
except Exception as e:
    print(f'Hata: {e}')
try:
    contours, hierarchy = cv2.findContours(marker.copy(), cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        if hierarchy[0][i][3] == -1:
            cv2.drawContours(image, contours, i, (255, 0, 0), 3)
except Exception as e:
    print(f'Hata: {e}')
cv2.imshow('Image', image)
cv2.waitKey(0)

"""
Havza Algoritması:
1. Resmin konturlarını bulmak
2. watershed algoritması: küçük nesneleri cv2.morphologyEx ile kaldırma. cv2.distanceTransform ise her pikselin arka plan pikselin arasındaki mesafeyi hesaplar.
3. 
"""