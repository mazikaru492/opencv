from pathlib import Path
import random
import cv2

TRACKER_TYPE = "MOSSE"
MAX_AREA = 5000
DETECT_SCALE = 1.005
DETECT_NEIGHBORS = 1
DETECT_MIN_SIZE = (1, 1)
VIDEO_PATH = r"C:\Users\ktc\Desktop\消さないでね\授業\授業\moving_peoples.mp4"


def select_tracker(tracker_type):
    legacy = cv2.legacy if hasattr(cv2, "legacy") else cv2

    if tracker_type == "BOOSTING":
        return legacy.TrackerBoosting_create()
    if tracker_type == "MIL":
        return legacy.TrackerMIL_create()
    if tracker_type == "KCF":
        return legacy.TrackerKCF_create()
    if tracker_type == "TLD":
        return legacy.TrackerTLD_create()
    if tracker_type == "MEDIANFLOW":
        return legacy.TrackerMedianFlow_create()
    if tracker_type == "MOSSE":
        return legacy.TrackerMOSSE_create()
    if tracker_type == "CSRT":
        return legacy.TrackerCSRT_create()

    raise ValueError(f"Unsupported tracker type: {tracker_type}")


def create_multi_tracker():
    if hasattr(cv2, "legacy") and hasattr(cv2.legacy, "MultiTracker_create"):
        return cv2.legacy.MultiTracker_create()
    return cv2.MultiTracker_create()


def get_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def box_center(roi):
    x, y, w, h = roi
    return (int(x + w / 2), int(y + h / 2))


def load_cascade(base_dir: Path):
    candidates = [
        base_dir / "haarcascade_fullbody.xml",
        base_dir.parent / "haarcascade_fullbody.xml",
        base_dir.parent / "授業" / "授業" / "haarcascade_fullbody.xml",
    ]

    for path in candidates:
        if path.exists():
            cascade = cv2.CascadeClassifier(str(path))
            if not cascade.empty():
                return cascade

    fallback = Path(cv2.data.haarcascades) / "haarcascade_fullbody.xml"
    if fallback.exists():
        cascade = cv2.CascadeClassifier(str(fallback))
        if not cascade.empty():
            return cascade

    for path in base_dir.parent.rglob("haarcascade_fullbody.xml"):
        cascade = cv2.CascadeClassifier(str(path))
        if not cascade.empty():
            return cascade

    return None


def resolve_video_path(base_dir: Path):
    if VIDEO_PATH:
        explicit = Path(VIDEO_PATH)
        if explicit.exists():
            return explicit

    candidates = [
        base_dir / "moving_peoples.mp4",
        base_dir.parent / "moving_peoples.mp4",
        base_dir.parent / "授業" / "授業" / "moving_peoples.mp4",
    ]

    for path in candidates:
        if path.exists():
            return path

    for path in base_dir.parent.rglob("moving_peoples.mp4"):
        return path

    return None


def main():
    base_dir = Path(__file__).resolve().parent
    video_path = resolve_video_path(base_dir)
    if video_path is None:
        print("Could not find moving_peoples.mp4")
        return

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Could not open video: {video_path}")
        return

    cascade = load_cascade(base_dir)
    if cascade is None:
        print("Could not load haarcascade_fullbody.xml")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps) if fps > 0 else 30

    ret, frame = cap.read()
    if not ret:
        print("Could not read the first frame")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    humans = cascade.detectMultiScale(
        gray,
        scaleFactor=DETECT_SCALE,
        minNeighbors=DETECT_NEIGHBORS,
        minSize=DETECT_MIN_SIZE,
    )

    rois = []
    colors = []
    lines = []
    multi_tracker = create_multi_tracker()

    for (x, y, w, h) in humans:
        if w * h > MAX_AREA:
            continue
        roi = (int(x), int(y), int(w), int(h))
        rois.append(roi)
        colors.append(get_color())
        lines.append([box_center(roi)])
        multi_tracker.add(select_tracker(TRACKER_TYPE), frame, roi)

    if not rois:
        print("No humans detected in the first frame")
        return

    cv2.namedWindow("original", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        _, bboxes = multi_tracker.update(frame)
        for i, (x, y, w, h) in enumerate(bboxes):
            roi = (int(x), int(y), int(w), int(h))
            cv2.rectangle(frame, roi, colors[i], 2)
            lines[i].append(box_center(roi))
            line_points = lines[i]
            for j in range(1, len(line_points)):
                cv2.line(frame, line_points[j - 1], line_points[j], colors[i], 2)

        cv2.imshow("original", frame)
        if cv2.waitKey(delay) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
