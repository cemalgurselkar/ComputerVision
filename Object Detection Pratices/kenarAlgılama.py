import cv2
import numpy as np

img = cv2.imread("data/london.jpg")
img = cv2.resize(img,(1280,720)) # Resmin boyutu
blurred_img = cv2.blur(img,(7,7)) # Resmi blurlamak (kenar tespiti için önemli)
median_val = np.median(img)
low = int(median_val*0.8) # Threshold değerleri oluşturmak (canny için)
high = int(median_val*1.2) # Threshold değerleri oluşturmak (canny için)
print(low,high)
edges = cv2.Canny(blurred_img,low,high) # kenarları çıkarma.
cv2.imshow("image", edges)
cv2.waitKey(0)

"""
Burada, blurlama ve canny işlemleri üzerine çalışım. Amaç bir fotoğrafın iskelet yapsını çıkarmak. Gürültüleri azaltmak için blurlama tekniği, iskelet yapısı içise canny tekniği kullandım.Kenarları algılamak için uygulanabilir bir yöntem.
"""