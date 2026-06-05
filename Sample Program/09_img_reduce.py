import numpy as np
import cv2

def main():
    img = cv2.imread("./ktech.jpg")
    height,width = img.shape[:2]
    print(width,height)

    reducde_ratio = 2

    img_reduce = img[::reducde_ratio,::reducde_ratio,:]
    cv2.imshow("Image_Reduce", img_reduce)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()