import numpy as np
import cv2

def main():
    img = cv2.imread("./ktech.jpg")
    height,width = img.shape[:2]
    print(width,height)

    img_gray_mean = img.mean(axis=2).astype(np.uint8)
    cv2.imshow("Image_Gray_Mean", img_gray_mean)

    img_gray_lumi =0.114*img[:,:,0]+0.587*img[:,:,1]+0.299*img[:,:,2]
    img_gray_lumi = img_gray_lumi.astype(np.uint8)
    cv2.imshow("Image_Gray_Lumi", img_gray_lumi)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()