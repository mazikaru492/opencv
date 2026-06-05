import numpy as np
import cv2

def onMouse(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		print("Miuse_L_Click")
		cv2.circle(param[1], (x,y), 50, (0,0,255), 2)
		cv2.imshow(param[0], param[1])
	
	if event == cv2.EVENT_RBUTTONDOWN:
		print("Mouse_R_Click")
		cv2.circle(param[1], (x,y), 50, (255,0,0), 2)
		cv2.imshow(param[0], param[1])	

def main():
    img = cv2.imread("./ktech.jpg")
    height,width = img.shape[:2]
    print(width,height)

    cv2.imshow('Figure', img)

    param = ('Figure', img)

    cv2.setMouseCallback('Figure', onMouse, param)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()