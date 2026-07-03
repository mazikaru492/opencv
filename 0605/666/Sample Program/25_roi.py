import numpy as np
import cv2

def main():

    cap = cv2.VideoCapture('./moving_vehicles.mp4')

    roi = None

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        if roi != None:
            cv2.rectangle(frame,roi,(0,255,255),2)

        cv2.imshow('original',frame)

        key =cv2.waitKey(10)
        if key == 27:
            break
        if key == ord("s"):
            roi = cv2.selectROI("Select Roi", frame, False, False)
            print(roi)
            cv2.destroyWindow("Select Roi")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()