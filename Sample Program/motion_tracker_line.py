from pathlib import Path
import numpy as np
import cv2

drawing = False
ix, iy = None, None
ex, ey = None, None

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, ex, ey

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        ex, ey = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            ex, ey = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

def box_center(p1, p2):
    x = int((p1[0] + p2[0]) / 2)
    y = int((p1[1] + p2[1]) / 2)
    return (x, y)

def main():
    global ix, iy, ex, ey, frame, tracker

    base_dir = Path(__file__).resolve().parent
    video_path = base_dir / "moving_vehicles.mp4"
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print("Cannot open video:", video_path)
        return

    cv2.namedWindow("original", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("original", draw_rectangle, "original")

    pause = False
    track_start = -1
    line_points = []

    while True:
        if pause:
            frame_d = frame_s.copy()
            cv2.rectangle(frame_d, (ix, iy), (ex, ey), (0, 255, 255), 2)
            cv2.imshow("original", frame_d)
            track_start = 0
        else:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame_s = frame.copy()

            if track_start == 0:
                tracker = cv2.legacy.TrackerMedianFlow_create()
                if ex is not None:
                    w = ex - ix
                    h = ey - iy
                    tracker.init(frame, (ix, iy, w, h))
                    track_start = 1
                    line_points.append(box_center((ix, iy), (ex, ey)))

            if track_start == 1:
                track, bbox = tracker.update(frame)
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 255), 2)

                if track:
                    line_points.append(box_center(p1, p2))

                if len(line_points) > 1:
                    pts = np.array(line_points, np.int32).reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], isClosed=False, color=(0, 255, 255), thickness=2)

            cv2.imshow("original", frame)

        key = cv2.waitKey(30)
        if key == 27:
            break
        elif key == ord('s'):
            pause = True
            ix, iy = None, None
            ex, ey = None, None
            line_points = []
            track_start = -1
        elif key == ord('p'):
            pause = False

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
