import numpy as np
import cv2

def main():
    img = cv2.imread("./ktech.jpg")
    height,width = img.shape[:2]
    print(width,height)

    for i in range(1,width,80):
        cv2.line(img, (i, 0), (i, height), (0,0,0), 1)

    for i in range(1,height,80):
        cv2.line(img, (0, i), (width, i), (0,0,0), 1)

    mean_color = img.mean()
        
    cv2.circle(img, (width//2,height//2), 100, (mean_color,mean_color,mean_color), -1)
    cv2.circle(img, (width//2,height//2), 100, (255,255,255), 1)

    cv2.imshow('Figure', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()