import numpy as np
import cv2
import random
import time

def select_tracker2(trackerType):

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

    return tracker

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

color_num = -1

def get_color():
    global color_num

    color = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
    color_num += 1
    if color_num == len(color):
        color_num = 0
    
    return  color[color_num]

def box_center(roi):
    (x,y,w,h) = roi
    cx = int(x+w/2)
    cy = int(y+h/2)

    return (cx,cy)

def main():

    cap = cv2.VideoCapture('./moving_peoples.mp4')
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    print(f"Frame Rate: {frame_rate}")

    delay = int(1000/frame_rate)

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

    track_start = -1
    rois = []
    color = []
    f_frame = None
    play = True
    lines = []

    multiTracker = cv2.legacy.MultiTracker_create()

    while True:
        s_time = time.time()
        if play == True:
            ret, frame = cap.read()
            if not ret:
                break

            if track_start == 0:
                for roi in rois:
                    print(roi)
                    color.append(get_color())
                    lines.append([])
                    tracker = select_tracker2(trackerType)
                    multiTracker.add(tracker,frame,roi)
                    track_start = 1

            if track_start == 1:
                track, bboxs = multiTracker.update(frame)
                if track == True:
                    for i,(x,y,w,h) in enumerate(bboxs):
                        roi = (int(x),int(y),int(w),int(h))
                        print(f'{i+1}：{trackerType}：{track}, {roi}, {color[i]}')
                        pt = box_center(roi)
                        line_point = lines[i]
                        line_point.append(pt)
                        cv2.rectangle(frame,roi,color[i],2)
                        for j,c_pt in enumerate(line_point):
                            if j != 0:
                                cv2.line(frame,line_point[j-1],c_pt,color[i],2)

            f_frame = frame.copy()
            cv2.imshow('original',frame)

        e_time = time.time()
        d_time = int((e_time-s_time)*1000)
        w_time = delay-d_time
        if w_time <= 0:
            w_time = 1
        print(w_time)
        key =cv2.waitKey(w_time)
        if key == 27:
            break
        if key == ord("s"):
            play = False
            if track_start == -1:
                play = True
                rois = multi_rois("Select Roi", frame, False, False)
                print(len(rois))
                cv2.destroyWindow("Select Roi")
                if len(rois) != 0:
                    track_start = 0
        if key == ord("p"):
            play = True


    cv2.imshow("original",f_frame)
    key =cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()