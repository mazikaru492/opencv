import numpy as np
import cv2
import random

Tracker_type = 'MOSSE'
width = None
height = None

def s_tracker(trackerType):

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

def get_color():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)

    return (r,g,b)


def roi_to_rect(roi):
    pt1 = (int(roi[0]),int(roi[1]))
    pt2 = (int(roi[0]+roi[2]),int(roi[1]+roi[3]))

    return pt1,pt2

def box_center(p1,p2):
    x = int((p1[0]+p2[0])/2)
    y = int((p1[1]+p2[1])/2)

    return (x,y)

def in_window(p1,p2):
    global width, height

    pt = box_center(p1,p2)

    if pt[0] <= 10 or pt[1] <= 10:
        return False

    if pt[0] > width-10 or pt[1] > height-10:
        return False
    else:
        return True


def main():
    global width, height

    cap = cv2.VideoCapture('./moving_peoples.mp4')

    cv2.namedWindow("original",cv2.WINDOW_NORMAL)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    finish = False
    liness = []

    while True:

        lines = []
        color = []
        valid = []

        first = True

        rois = []

        cnt = 0
        r_cnt = 100

        multiTracker = cv2.legacy.MultiTracker_create()

        while True:

            cnt+=1
            if cnt == r_cnt:
                break

            if first == True:

                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue

                img = frame.copy()

                cascade_path = './haarcascade_fullbody.xml'
                cascade = cv2.CascadeClassifier(cascade_path)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                humans = cascade.detectMultiScale(gray,scaleFactor=1.005, minNeighbors=1, minSize=(1,1))

                for x, y, w, h in humans:
                    if w*h < 5000:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
                        roi = (x,y,w,h)
                        rois.append(roi)

                first = False

                for roi in rois:
                    pt1, pt2 = roi_to_rect(roi)
                    col = get_color()
                    color.append(col)
                    cv2.rectangle(frame,
                            pt1,
                            pt2,
                            color=col,
                            thickness=1)
                    lin = []
                    lin.append(box_center(pt1,pt2))
                    lines.append(lin)
                    valid.append(True)

                for roi in rois:
                    multiTracker.add(s_tracker(Tracker_type),frame,roi)

            else:
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue

                track, bboxes = multiTracker.update(frame)
                for i, bbox in enumerate(bboxes):
                    pt1,pt2 = roi_to_rect(bbox)
                    if in_window(pt1,pt2) == True:
                        if valid[i] == True:
                            cv2.rectangle(frame,pt1,pt2,color[i],2)
                            lines[i].append(box_center(pt1,pt2))
                    else:
                        valid[i] = False

                liness.append(lines)

                for lins in liness:
                    for j,lin in enumerate(lins):
                        for i in range(1,len(lin)):
                            cv2.line(frame,lin[i-1],lin[i],(0,0,255),2)

                cv2.imshow('Human Track',frame)
                cv2.moveWindow('Human Track', 600, 200)

            key =cv2.waitKey(30)
            if key == 27:
                finish = True
                break

        if finish == True:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()