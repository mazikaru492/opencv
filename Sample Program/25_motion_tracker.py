import numpy as np
import cv2
import time

drawing = False
ix,iy = None,None
ex,ey = None,None

def draw_rectangle(event,x,y,flags,param):
    global ix,iy,drawing,ex,ey

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
        ex,ey = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            ex,ey = x,y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

from pathlib import Path

def main():
    global ix,iy,ex,ey,frame,tracker

    base_dir = Path(__file__).resolve().parent
    video_path = base_dir / 'moving_vehicles.mp4'
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print("動画を読み込めません:", video_path)
        return

    cv2.namedWindow("original",cv2.WINDOW_NORMAL)
    param = "original"
    cv2.setMouseCallback("original", draw_rectangle, param)

    avg = None

    pause = False
    track_start = -1

    while True:
        if pause == True:
            frame_d = frame_s.copy()
            cv2.rectangle(frame_d,(ix,iy),(ex,ey),(0,255,255),2)
            cv2.imshow('original',frame_d)
            track_start = 0
        else:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame_s = frame.copy()

            if track_start == 0:
                tracker = cv2.legacy.TrackerMedianFlow_create()
                if ex != None:
                    w = ex-ix
                    h = ey-iy
                    print(ix,iy,w,h)
                    ok = tracker.init(frame,(ix,iy,w,h))
                    track_start = 1

            if track_start == 1:
                track, bbox = tracker.update(frame)
                print(track, bbox)
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame,p1,p2,(0,255,255),2)

            cv2.imshow('original',frame)

        key =cv2.waitKey(30)
        if key == 27:
            break
        elif key == 115:
            pause = True
            ix,iy = None, None
            ex,ey = None, None
            track_start = -1 # トラック状態もリセット
        elif key == 112:
            pause = False

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()