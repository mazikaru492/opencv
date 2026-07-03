import numpy as np
import cv2

def main():
    img = cv2.imread("./ball.jpg")

    img_blur = cv2.blur(img, (1,1))
    cv2.imshow('Blur', img_blur)

    img_blur = cv2.blur(img, (5,5))
    cv2.imshow('Blur_5', img_blur)

    img_blur = cv2.blur(img, (29,29))
    cv2.imshow('Blur_29', img_blur)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()