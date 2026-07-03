import cv2
import numpy as np

img = cv2.imread(r'C:\Users\ktc\Desktop\Opencv\0605\666\book4.jpg')

if img is None:
    print("エラー")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)

contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

c = contours[0]
peri = cv2.arcLength(c, True)

approx = None
ratio = 0.04
while ratio < 0.2:
    temp_approx = cv2.approxPolyDP(c, ratio * peri, True)
    if len(temp_approx) == 4:
        approx = temp_approx
        break
    ratio += 0.01

if approx is None:
    print("エラー: 本の四隅を検出できませんでした")
    exit()

pts = approx.reshape(4, 2).astype(np.float32)

rect = np.zeros((4, 2), dtype=np.float32)
s = pts.sum(axis=1)
rect[0] = pts[np.argmin(s)]
rect[2] = pts[np.argmax(s)]
diff = np.diff(pts, axis=1)
rect[1] = pts[np.argmin(diff)]
rect[3] = pts[np.argmax(diff)]

(tl, tr, br, bl) = rect
widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
maxWidth = max(int(widthA), int(widthB))

heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
maxHeight = max(int(heightA), int(heightB))

dst = np.array([
    [0, 0],
    [maxWidth - 1, 0],
    [maxWidth - 1, maxHeight - 1],
    [0, maxHeight - 1]
], dtype=np.float32)

M = cv2.getPerspectiveTransform(rect, dst)
warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))

cv2.imshow('Original', img)
cv2.imshow('Warped', warped)
cv2.waitKey(0)
cv2.destroyAllWindows()