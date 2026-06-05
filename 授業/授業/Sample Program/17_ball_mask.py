import numpy as np
import cv2

def main():
    img = cv2.imread("./ball.jpg")
    img_gauss = cv2.GaussianBlur(img, (5,5), 0)
    hsv = cv2.cvtColor(img_gauss,cv2.COLOR_BGR2HSV)
    cv2.imshow("Image", img)

    while True:
        color = input("Please input color name(pink/blue/green) > ")
        if color == "pink" or color == "green" or color == "blue":
            break

    if color == "pink":
        h_lower = 165
        h_upper = 180
    elif color == "green":
        h_lower = 80
        h_upper = 100
    else: 
        h_lower = 100
        h_upper = 110

    mask = cv2.inRange(hsv,(h_lower,32,0),(h_upper,255,255))

    cv2.imshow("Mask", mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()