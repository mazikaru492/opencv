from collections import deque
from pathlib import Path

import cv2


next_tracker_id = 1


def _get_tracker_factory(factory_name):
 legacy = getattr(cv2, "legacy", None)
 for owner in (legacy, cv2):
  if owner is not None and hasattr(owner, factory_name):
   return getattr(owner, factory_name)
 return None


def _get_multitracker_factory():
 legacy = getattr(cv2, "legacy", None)
 for owner in (legacy, cv2):
  if owner is not None and hasattr(owner, "MultiTracker_create"):
   return getattr(owner, "MultiTracker_create")
 return None


TRACKER_SPECS = [
 (1, "MedianFlow", "TrackerMedianFlow_create"),
 (2, "Boosting", "TrackerBoosting_create"),
 (3, "MIL", "TrackerMIL_create"),
 (4, "TLD", "TrackerTLD_create"),
 (5, "KCF", "TrackerKCF_create"),
 (6, "MOSSE", "TrackerMOSSE_create"),
 (7, "CSRT", "TrackerCSRT_create"),
]


TRACKER_TYPES = {}
for key, name, factory_name in TRACKER_SPECS:
 factory = _get_tracker_factory(factory_name)
 if factory is not None:
  TRACKER_TYPES[key] = (name, factory)


if not TRACKER_TYPES:
 raise RuntimeError("利用可能な OpenCV トラッカーが見つかりません")


MULTITRACKER_FACTORY = _get_multitracker_factory()
if MULTITRACKER_FACTORY is None:
 raise RuntimeError("利用可能な OpenCV MultiTracker が見つかりません")


tracker_type = 1 if 1 in TRACKER_TYPES else next(iter(TRACKER_TYPES))

COLORS = [
 (0, 255, 0),
 (0, 0, 255),
 (255, 0, 0),
 (0, 255, 255),
 (255, 255, 0),
 (255, 0, 255),
 (0, 128, 255),
 (255, 128, 0),
]


def create_tracker():
 return TRACKER_TYPES[tracker_type][1]()


def create_multitracker():
 return MULTITRACKER_FACTORY()


def show_tracker_menu():
 print("\n=== 利用可能なトラッキングアルゴリズム ===")
 for key, (name, _) in TRACKER_TYPES.items():
  print(f"{key}: {name}")
 print("=======================================")
 print("キーボード操作:")
 print("  s: 一時停止")
 print("  p: 再生")
 print("  d: 現在のフレームで人物を再検出")
 print("  a: 手動で ROI を追加")
 print("  c: 全追跡の削除")
 print("  ESC: 終了")


def _cascade_paths():
 local_dir = Path(__file__).resolve().parent
 return [
  local_dir / "haarcascade_fullbody.xml",
  Path(cv2.data.haarcascades) / "haarcascade_fullbody.xml",
 ]


import os

def load_cascade():
 for path in _cascade_paths():
  if path.exists():
   old_cwd = os.getcwd()
   try:
    os.chdir(path.parent)
    cascade = cv2.CascadeClassifier(path.name)
    if not cascade.empty():
     return cascade, str(path)
   finally:
    os.chdir(old_cwd)
 raise RuntimeError("haarcascade_fullbody.xml を読み込めません")


def _iou(box1, box2):
 x1, y1, w1, h1 = box1
 x2, y2, w2, h2 = box2

 x1b = x1 + w1
 y1b = y1 + h1
 x2b = x2 + w2
 y2b = y2 + h2

 ix1 = max(x1, x2)
 iy1 = max(y1, y2)
 ix2 = min(x1b, x2b)
 iy2 = min(y1b, y2b)

 iw = max(0, ix2 - ix1)
 ih = max(0, iy2 - iy1)
 inter = iw * ih
 if inter <= 0:
  return 0.0

 area1 = w1 * h1
 area2 = w2 * h2
 union = area1 + area2 - inter
 if union <= 0:
  return 0.0

 return inter / union


def _merge_overlapping_boxes(boxes, iou_threshold=0.35):
 if not boxes:
  return []

 # 大きい候補から採用し、重複する候補は除外する。
 sorted_boxes = sorted(boxes, key=lambda b: b[2] * b[3], reverse=True)
 merged = []

 for box in sorted_boxes:
  if all(_iou(box, kept) < iou_threshold for kept in merged):
   merged.append(box)

 return merged


def detect_people(frame, cascade):
 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

 # 演習課題（図のサンプル）に合わせた高頻度な検出パラメータ
 detections = cascade.detectMultiScale(
  gray,
  scaleFactor=1.005,
  minNeighbors=1,
  minSize=(10, 20),
 )

 all_detections = []
 for x, y, w, h in detections:
  # 動画の人物サイズに合わせて、巨大過ぎる誤検出を除外
  if w * h < 5000 and w * h > 200:
   all_detections.append((int(x), int(y), int(w), int(h)))

 merged = _merge_overlapping_boxes(all_detections, iou_threshold=0.3)
 return merged


def select_multiple_rois(frame):
 selected = []

 try:
  rois = cv2.selectROIs("Select ROIs", frame, fromCenter=False, showCrosshair=False)
  for roi in rois:
   x, y, w, h = map(int, roi)
   if w > 0 and h > 0:
    selected.append((x, y, w, h))
 except cv2.error:
  selected = []

 if selected:
  cv2.destroyWindow("Select ROIs")
  return selected

 preview = frame.copy()
 while True:
  roi = cv2.selectROI("Select ROIs", preview, fromCenter=False, showCrosshair=False)
  x, y, w, h = map(int, roi)
  if w <= 0 or h <= 0:
   break
  selected.append((x, y, w, h))
  cv2.rectangle(preview, (x, y), (x + w, y + h), (0, 255, 255), 2)

 cv2.destroyWindow("Select ROIs")
 return selected


def rebuild_multitracker(frame, tracker_infos):
 multitracker = create_multitracker()
 alive_infos = []

 for info in tracker_infos:
  x, y, w, h = info["bbox"]
  if w <= 0 or h <= 0:
   continue

  tracker = create_tracker()
  try:
   ok = multitracker.add(tracker, frame, (x, y, w, h))
  except Exception:
   ok = False

  if ok:
   alive_infos.append(info)

 return multitracker, alive_infos


def build_tracker_infos(rois):
 global next_tracker_id

 tracker_infos = []
 for x, y, w, h in rois:
  tracker_id = next_tracker_id
  next_tracker_id += 1
  tracker_infos.append(
   {
    "id": tracker_id,
    "color": COLORS[(tracker_id - 1) % len(COLORS)],
    "pts": deque([(int(x + w / 2), int(y + h / 2))], maxlen=100),
    "bbox": (x, y, w, h),
   }
  )
 return tracker_infos


def initialize_from_cascade(frame, cascade):
 rois = detect_people(frame, cascade)
 tracker_infos = build_tracker_infos(rois)
 multitracker, tracker_infos = rebuild_multitracker(frame, tracker_infos)
 return multitracker, tracker_infos, len(tracker_infos)


def add_rois(frame, multitracker, tracker_infos):
 before_count = len(tracker_infos)
 new_rois = select_multiple_rois(frame)
 if not new_rois:
  return multitracker, tracker_infos, 0, "ROIが選択されませんでした"

 tracker_infos.extend(build_tracker_infos(new_rois))
 multitracker, tracker_infos = rebuild_multitracker(frame, tracker_infos)
 added_count = len(tracker_infos) - before_count
 if added_count <= 0:
  return multitracker, tracker_infos, 0, "トラッカー初期化に失敗しました"
 return multitracker, tracker_infos, added_count, ""


def update_trackers(frame, multitracker, tracker_infos):
 if not tracker_infos:
  return multitracker, []

 _, boxes = multitracker.update(frame)

 active_infos = []
 for info, bbox in zip(tracker_infos, boxes):
  x, y, w, h = bbox
  info["bbox"] = (x, y, w, h)
  cx = int(x + w / 2)
  cy = int(y + h / 2)
  info["pts"].append((cx, cy))
  active_infos.append(info)

 return multitracker, active_infos


def draw_tracks(frame, trackers):
 for t in trackers:
  pts = t["pts"]
  color = t["color"]
  if len(pts) > 1:
   for i in range(1, len(pts)):
    if pts[i - 1] is None or pts[i] is None:
     continue
    cv2.line(frame, pts[i - 1], pts[i], color, 2)


def draw_label(frame, text, origin, color):
 x, y = origin
 font = cv2.FONT_HERSHEY_SIMPLEX
 scale = 0.5
 thickness = 1
 (text_w, text_h), baseline = cv2.getTextSize(text, font, scale, thickness)
 top_left = (x, max(0, y - text_h - baseline - 4))
 bottom_right = (x + text_w + 6, y)
 cv2.rectangle(frame, top_left, bottom_right, color, -1)
 cv2.putText(frame, text, (x + 3, y - 4), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)


def draw_boxes(frame, trackers):
 for t in trackers:
  bbox = t.get("bbox")
  if bbox is None:
   continue
  x, y, w, h = bbox
  p1 = (int(x), int(y))
  p2 = (int(x + w), int(y + h))
  color = t["color"]
  cv2.rectangle(frame, p1, p2, color, 2)


def main():
 global tracker_type

 show_tracker_menu()

 cascade, cascade_path = load_cascade()
 print(f"カスケード分類器: {cascade_path}")

 video_path = r"C:\Users\ktc\Desktop\消さないでね\授業\授業\moving_peoples.mp4"
 cap = cv2.VideoCapture(video_path)
 if not cap.isOpened():
  print(f"エラー: {video_path} を開けません")
  return

 cv2.namedWindow("original", cv2.WINDOW_NORMAL)

 ret, frame = cap.read()
 if not ret:
  print("エラー: 最初のフレームを取得できません")
  cap.release()
  return

 frame_s = frame.copy()
 multitracker, tracker_infos, detected_count = initialize_from_cascade(frame_s, cascade)
 if detected_count > 0:
  print(f"初期フレームで {detected_count} 個の人物を検出しました")
 else:
  print("初期フレームで人物を検出できませんでした。d で再検出、a で手動追加できます")

 pause = False
 current_tracker_name = TRACKER_TYPES[tracker_type][0]

 while True:
  if pause:
   frame_d = frame_s.copy()
   draw_boxes(frame_d, tracker_infos)
   draw_tracks(frame_d, tracker_infos)

   title = f"Paused | Tracker: {current_tracker_name} | d: detect, a: add ROI, p: play"
   cv2.setWindowTitle("original", title)
   cv2.imshow("original", frame_d)
  else:
   ret, frame = cap.read()
   if not ret:
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, frame = cap.read()
    if not ret:
     break

   frame_s = frame.copy()
   multitracker, tracker_infos = update_trackers(frame, multitracker, tracker_infos)
   draw_boxes(frame, tracker_infos)
   draw_tracks(frame, tracker_infos)

   title = f"Tracking | Tracker: {current_tracker_name} | s: pause"
   cv2.setWindowTitle("original", title)
   cv2.imshow("original", frame)

  key = cv2.waitKey(30) & 0xFF

  if key == 27:
   break
  if key == ord("s"):
   pause = True
   continue
  if key == ord("p"):
   pause = False
   continue
  if key == ord("d") and pause:
   multitracker, tracker_infos, n = initialize_from_cascade(frame_s, cascade)
   if n > 0:
    print(f"人物を {n} 個再検出しました")
   else:
    print("人物を再検出できませんでした")
   continue
  if key == ord("a") and pause:
   multitracker, tracker_infos, n, reason = add_rois(frame_s, multitracker, tracker_infos)
   if n > 0:
    print(f"ROIを {n} 個追加しました")
   else:
    print(f"ROIの追加に失敗しました: {reason}")
   continue
  if key == ord("c"):
   tracker_infos.clear()
   multitracker = create_multitracker()
   print("追跡をすべて削除しました")
   continue
  if key in range(ord("1"), ord("8")):
   new_type = int(chr(key))
   if new_type in TRACKER_TYPES:
    tracker_type = new_type
    current_tracker_name = TRACKER_TYPES[tracker_type][0]
    print(f"\nトラッカーを '{current_tracker_name}' に変更しました")
    pause = True
    multitracker, tracker_infos = rebuild_multitracker(frame_s, tracker_infos)

 cap.release()
 cv2.destroyAllWindows()


if __name__ == "__main__":
 main()

