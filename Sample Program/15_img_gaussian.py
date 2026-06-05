import numpy as np
import cv2

def main():
    img = cv2.imread("./ball.jpg")

    img_gauss = cv2.GaussianBlur(img, (1,1), 0)
    cv2.imshow('Gaussian_1', img_gauss)

    img_gauss = cv2.GaussianBlur(img, (5,5), 0)
    cv2.imshow('Gaussian_5', img_gauss)

    img_gauss = cv2.GaussianBlur(img, (15,15), 0)
    cv2.imshow('Gaussian_15', img_gauss)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()