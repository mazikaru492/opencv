import numpy as np
import cv2

def main():
    img = cv2.imread("./ball.jpg")
    img_gauss = cv2.GaussianBlur(img, (5,5), 0)
    hsv = cv2.cvtColor(img_gauss,cv2.COLOR_BGR2HSV)
    cv2.imshow("Image", img)

    color = "blue"

    if color == "pink":
        h_lower = 165
        h_upper = 180
    elif color == "green":
        h_lower = 80
        h_upper = 100
    elif color == "blue": 
        h_lower = 100
        h_upper = 110

    mask = cv2.inRange(hsv,(h_lower,32,0),(h_upper,255,255))

    contours, hierachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours, -1, (0,255,255), 2)

    cv2.imshow("Contours", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()