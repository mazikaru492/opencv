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
    elif color == "blue": 
        h_lower = 100
        h_upper = 105

    mask = cv2.inRange(hsv,(h_lower,32,0),(h_upper,255,255))

    contours, hierachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_contours = 0
    max_contours_index = 0

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_contours = cnt
            max_contours_index = i

    x,y,w,h = cv2.boundingRect(max_contours)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)

    cv2.imshow("Contours", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()