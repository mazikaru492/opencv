import numpy as np
import cv2

def onMouse(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print("Miuse_L_Click")
        cv2.circle(param[2], (x, y), 5, (0, 0, 255), -3)
        cv2.imshow(param[0], param[2])

        r = param[1][y,x,2]
        g = param[1][y,x,1]
        b = param[1][y,x,0]

        print("R=",r,"G=",g,"B=",b)
    
        h = param[3][y,x,0]
        s = param[3][y,x,1]
        v = param[3][y,x,2]

        print("H=",h,"S=",s,"V=",v)
        print()
		
def main():
    img = cv2.imread("./ball.jpg")

    img_copy = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
    cv2.imshow('Ball', img)

    param = ('Ball',img,img_copy,hsv)
    cv2.setMouseCallback('Ball', onMouse, param)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()