import cv2
import numpy as np

img = cv2.imread('data/sudoku.jpg',0)
img = np.float32(img)

#harris corner detection
dst = cv2.cornerHarris(img,blockSize=2,ksize=3,k=0.05)

#Genişletme (dts temsil ettiği yerleri genişlet)
dst2 = cv2.dilate(dst,None,iterations=2)
dst2[dst>0.2*dst.max()] = 1

#shi tomsai detection
corners = cv2.goodFeaturesToTrack(img,100,0.01,10)
corners = np.int64(corners)
for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,(0,0,0),cv2.FILLED)
cv2.imshow('img',dst)
cv2.imshow('corners',dst2)
cv2.waitKey(0)