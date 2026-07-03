import cv2

img1 = cv2.imread(r'C:\Users\ktc\Desktop\Opencv\0605\666\Sample Program\book5.jpg')
img2 = cv2.imread(r'C:\Users\ktc\Desktop\Opencv\0605\666\Sample Program\books.jpg')

if img1 is None or img2 is None:
    print("エラー")
    exit()

akaze = cv2.AKAZE_create()

kps1, dess1 = akaze.detectAndCompute(img1, None)
kps2, dess2 = akaze.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

matches = bf.knnMatch(dess1, dess2, k=2)

ratio = 0.8
good_matches = []
for m, n in matches:
    if m.distance < ratio * n.distance:
        good_matches.append([m])

img_matches = cv2.drawMatchesKnn(img1, kps1, img2, kps2, good_matches, None, flags=2)

cv2.imshow('Book Mapping Result', img_matches)
cv2.waitKey(0)
cv2.destroyAllWindows()