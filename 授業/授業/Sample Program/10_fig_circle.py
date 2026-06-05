import numpy as np
import cv2

def main():
    img = np.full((960, 1280, 3), (255,255,255), np.uint8)
    height,width = img.shape[:2]
    print(width,height)


    for i in range(1,width,80):
        cv2.line(img, (i, 0), (i, height), (0,0,0), 1)

    for i in range(1,height,80):
        cv2.line(img, (0, i), (width, i), (0,0,0), 1)
        
    cv2.circle(img, (width//2,height//2), 200, (0,255,255), -1)
    cv2.circle(img, (width//2,height//2), 200, (255,0,0), 2)

    cv2.imshow('Figure', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()