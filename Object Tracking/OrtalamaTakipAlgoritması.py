import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

faceCascade = cv2.CascadeClassifier('Data/haarcascade_frontalface_default.xml')
faceRects = faceCascade.detectMultiScale(frame)

(face_x,face_y,face_w,face_h)=tuple(faceRects[0])
track_Window = (face_x,face_y,face_w,face_h)

roi = frame[face_y:face_y+face_h,face_x:face_x+face_w]
roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([roi_hsv],[0],None,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

term_crit = (cv2.TERM_CRITERIA_MAX_ITER, 5, 1)
while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
    ret, track_Window = cv2.meanShift(dst, track_Window, term_crit)
    x, y, w, h = track_Window
    img2 = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),7)
    cv2.imshow('frame',img2)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()