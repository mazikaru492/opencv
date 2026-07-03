import cv2

img = cv2.imread('poster_2.png')

if img is None:
    print("エラー")
    exit()

akaze = cv2.AKAZE_create()
kps, des = akaze.detectAndCompute(img, None)
img_akaze = cv2.drawKeypoints(img, kps, None, flags=4)

cv2.imshow('Feature Points Result', img_akaze)
cv2.waitKey(0)
cv2.destroyAllWindows()