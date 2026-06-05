import numpy as np
import cv2

def main():
    img = cv2.imread("./ktech.jpg")
    height,width = img.shape[:2]
    print(width,height)

    mean = img.mean()

    img[150:250,200:500,:] = mean
    cv2.imshow("Image_Mask", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()