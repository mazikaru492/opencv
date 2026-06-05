import numpy as np
import cv2

img_list = []

def onMouse(event,x,y,flags,param):
    global img_list, circle_number

    if event == cv2.EVENT_LBUTTONDOWN:
        print("Miuse_L_Click")
        img = img_list[len(img_list)-1].copy()
        cv2.circle(img, (x,y), 50, (0,255,255), 2)
        img_list.append(img)
        cv2.imshow(param[0], img_list[len(img_list)-1])

    if event == cv2.EVENT_RBUTTONDOWN:
        print("Mouse_R_Click")
        if len(img_list) > 1:
            img_list.pop()
            cv2.imshow(param[0], img_list[len(img_list)-1])
        

def main():
    global img_list

    img = cv2.imread("./ktech.jpg")
    
    img_list.append(img)

    cv2.imshow('Figure', img)

    param = ('Figure',img)

    cv2.setMouseCallback('Figure', onMouse, param)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()