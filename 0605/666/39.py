import cv2
import numpy as np

img1 = cv2.imread(r'C:\Users\ktc\Desktop\Opencv\0605\666\Sample Program\book5.jpg')
img2 = cv2.imread(r'C:\Users\ktc\Desktop\Opencv\0605\666\Sample Program\books.jpg')

if img1 is None or img2 is None:
    print("エラー: 画像が読み込めません")
    exit()

akaze = cv2.AKAZE_create()
kps1, des1 = akaze.detectAndCompute(img1, None)
kps2, des2 = akaze.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
matches = bf.knnMatch(des1, des2, k=2)

good_matches = []
ratio = 0.8
for m, n in matches:
    if m.distance < ratio * n.distance:
        good_matches.append(m)

gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (11, 11), 0)
edges = cv2.Canny(blur, 30, 150)
kernel = np.ones((9, 9), np.uint8)
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
contours, _ = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

max_count = 0
best_rect = None

img_h, img_w = img2.shape[:2]

for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    bbox_area = w * h
    if bbox_area < 10000:
        continue

    # 画像全体を覆うような巨大な枠はスキップ
    if w > img_w * 0.9 or h > img_h * 0.9:
        continue

    count = 0
    for m in good_matches:
        pt = kps2[m.trainIdx].pt
        if x <= pt[0] <= x + w and y <= pt[1] <= y + h:
            count += 1

    if count > max_count:
        max_count = count
        best_rect = (x, y, w, h)

if best_rect is not None:
    x, y, w, h = best_rect
    cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 255), 3)
else:
    print("条件に合う本が見つかりませんでした")

cv2.imshow('Book Selection Result', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()