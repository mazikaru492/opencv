import numpy as np
import cv2

def main():
    img = cv2.imread("./ktech.jpg")
    height,width = img.shape[:2]
    print(width,height)

    h1 = 159
    h2 = 350
    w1 = 200
    w2 = 500

    img_cut = img[h1:h2,w1:w2,:]
    cv2.imshow("Image_Cut", img_cut)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()