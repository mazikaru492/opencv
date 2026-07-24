import cv2

img = cv2.imread('ball.jpg')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('HSV', hsv)

bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
cv2.imshow('BGR', bgr)

cv2.waitKey(0)
cv2.destroyAllWindows()