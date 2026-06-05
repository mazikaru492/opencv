import numpy as np
import cv2

def main():
    img = cv2.imread("./ktech.jpg")
    height,width = img.shape[:2]
    print(width,height)

    img_v_flip = img[::-1,:,:]	
    cv2.imshow("Image_V_Flip", img_v_flip)

    img_h_flip = img[:,::-1,:]	
    cv2.imshow("Image_H_Flip", img_h_flip)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()