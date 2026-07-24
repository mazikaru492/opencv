import cv2
import numpy as np

img = cv2.imread(r'C:\Users\yukij\Desktop\Opencv\0605\666\ex\ball.jpg')

blur = cv2.blur(img, (5, 5))
hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

lower = np.array([165, 32, 0])
upper = np.array([179, 255, 255])
mask = cv2.inRange(hsv, lower, upper)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))

max_contour = max(contours, key=cv2.contourArea)
x, y, w, h = cv2.boundingRect(max_contour)
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()