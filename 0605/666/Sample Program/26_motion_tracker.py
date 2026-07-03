import numpy as np
import cv2
def select_tracker():

    trackers = ["BOOSTING","MIL","KCF","TLD","MEDIANFLOW","GOTURN","MOSSE","CSRT"]

    print("==========")
    print("Please input algorithm number")
    for i,item in enumerate(trackers):
        print(f'{i+1}: {item}')

    while True:
        num = int(input("> "))
        if 1<=num  and num<=8:
            break

    trackerType = trackers[num-1]

    if trackerType == 'BOOSTING':
        tracker = cv2.legacy.TrackerBoosting_create()
    elif trackerType == 'MIL':
        tracker = cv2.legacy.TrackerMIL_create()
    elif trackerType == 'KCF':
        tracker = cv2.legacy.TrackerKCF_create()
    elif trackerType == 'TLD':
        tracker = cv2.legacy.TrackerTLD_create()
    elif trackerType == 'MEDIANFLOW':
        tracker = cv2.legacy.TrackerMedianFlow_create()
    elif trackerType == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    elif trackerType == 'MOSSE':
        tracker = cv2.legacy.TrackerMOSSE_create()
    elif trackerType == 'CSRT':
        tracker = cv2.legacy.TrackerCSRT_create()

    return tracker, trackerType

def main():

    cap = cv2.VideoCapture('./moving_vehicles.mp4')
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    print(f"Frame Rate: {frame_rate}")

    delay = int(1000/frame_rate)

    tracker, trackerType = select_tracker()

    track_start = -1
    roi = None
    f_frame = None
    play = True

    while True:
        if play == True:
            ret, frame = cap.read()
            if not ret:
                break

            if track_start == 0:
                ok = tracker.init(frame,roi)
                track_start = 1

            if track_start == 1:
                track, (x,y,w,h) = tracker.update(frame)
                roi = (int(x),int(y),int(w),int(h))
                print(f'{trackerType}：{track}, {roi}')
                if track == True:
                    cv2.rectangle(frame,roi,(0,255,255),2)

            f_frame = frame.copy()
            cv2.imshow('original',frame)

        key =cv2.waitKey(delay)
        if key == 27:
            break
        if key == ord("s"):
            play = False
            if track_start == -1:
                play = True
                roi = cv2.selectROI("Select Roi", frame, False, False)
                cv2.destroyWindow("Select Roi")
                if roi != (0,0,0,0):
                    track_start = 0
        if key == ord("p"):
            play = True


    cv2.imshow("original",f_frame)
    key =cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()