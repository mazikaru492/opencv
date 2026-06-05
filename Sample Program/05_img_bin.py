import numpy as np
import cv2

def main():
    img = cv2.imread("./ktech.jpg")
    height,width = img.shape[:2]
    print(width,height)

    img_gray = img.mean(axis=2).astype(np.uint8)

    img_bin = np.where(img_gray > 127, 255, 0).astype(np.uint8)

    cv2.imshow("Image_Bin", img_bin)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()