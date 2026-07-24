import cv2

path = r'C:\Users\yukij\Desktop\Opencv\0605\666\ex\ball.jpg'
img = cv2.imread(path)

if img is None:
    print("画像が読み込めませんでした。パスを確認してください。")
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    cv2.imshow('MASK', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()