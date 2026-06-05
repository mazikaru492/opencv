import numpy as np
import cv2

def multi_rois(window_name, img, showCrossfire, romCenter):
    img_c = img.copy()
    rois = []
    while True:
        roi = None
        roi = cv2.selectROI(window_name, img_c, False, False)
        cv2.destroyWindow(window_name)
        if roi == (0,0,0,0):
             break
        cv2.rectangle(img_c,roi,(255,0,0),2)
        rois.append(roi)

    return rois


def main():
    img = cv2.imread("./roi.jpg")

    rois = multi_rois("Select Rois", img, False, False)
    cv2.destroyWindow("Select Rois")

    for roi in rois:
        print(roi)
        cv2.rectangle(img,roi,(0,255,255),2)

    cv2.imshow('original',img)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()


if __name__ == '__main__':
	main()