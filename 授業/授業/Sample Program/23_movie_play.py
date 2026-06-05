import numpy as np
import cv2

def main():

    cap = cv2.VideoCapture('./people_move.mp4')

    play = True

    while True:
        if play == True:
            ret, frame = cap.read()
            cv2.imshow('camera' , frame)

        key =cv2.waitKey(10)
        if key == 27:
            break
        if key == 115:
            play = False
        if key == 112:
            play = True
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()