import cv2
import numpy as np

img = cv2.imread(r'C:\Users\ktc\Desktop\Opencv\0605\666\Sample Program\books.jpg')

if img is None:
    print("エラー")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (11, 11), 0)
edges = cv2.Canny(blur, 30, 150)

kernel = np.ones((9, 9), np.uint8)
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    if cv2.contourArea(c) > 10000:
        cv2.drawContours(img, [c], -1, (0, 255, 255), 3)

cv2.imshow('Improved Book Extraction', img)
cv2.waitKey(0)
cv2.destroyAllWindows()