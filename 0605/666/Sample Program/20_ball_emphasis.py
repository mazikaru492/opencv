import numpy as np
import cv2
import time

color = {"pink":{"h_lower":165,"h_upper":180},
        "green":{"h_lower":80,"h_upper":100},
        "blue":{"h_lower":100,"h_upper":110}}

height = None
width = None 

def get_color(img,x,y):

    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h = img_hsv[y][x][0]

    clicked_color = None

    for key in color:
        h_lower = color[key]["h_lower"]
        h_upper = color[key]["h_upper"]

        if h_lower < h and h <h_upper:
            clicked_color = key

    return clicked_color

def get_contour(img, clicked_color, x, y):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_lower = color[clicked_color]["h_lower"]
    h_upper = color[clicked_color]["h_upper"]
    mask = cv2.inRange(hsv,(h_lower,32,0),(h_upper,255,255))

    contours, hierachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        retval = cv2.pointPolygonTest(contour, (x,y), False)
        if retval == 1:
            return contour

    return None


def onMouse(event,x,y,flags,param):
	
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Mouse_L_Click",x,y)
        img = param[1]
        img_gray = param[2]
        img_copy = img.copy()
        #cv2.circle(img_copy,(x,y),5,(0,0,255),-3)
        #
        clicked_color = get_color(img,x,y)

        img_show = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

        if clicked_color != None:
            print(clicked_color)

            contour = get_contour(img, clicked_color, x,y)
            x,y,w,h = cv2.boundingRect(contour)

            for i in range(x,x+width):
                for j in range(h,h+height):
                    retval = cv2.pointPolygonTest(contour, (i,j), False)
                    if retval == 1:
                        img_show[j,i] = img[j,i]

        cv2.imshow(param[0], img_show)

def main():
    global height, width

    img = cv2.imread("./ball.jpg")
    img = cv2.GaussianBlur(img, (3,3), 0)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    height = img.shape[0]
    width = img.shape[1]
    print(height, width)

    cv2.imshow("Image", img)

    param = ('Image', img, img_gray)
    cv2.setMouseCallback('Image', onMouse, param)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()