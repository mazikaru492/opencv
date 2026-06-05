import numpy as np
import cv2

def main():
    img = cv2.imread("./ktech.jpg")
    height,width = img.shape[:2]
    print(width,height)

    img_nega = 255-img

    cv2.imshow("Image", img_nega)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()