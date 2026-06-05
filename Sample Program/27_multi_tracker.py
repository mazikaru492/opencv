import numpy as np
import cv2
import time
from collections import deque

drawing = False
ix,iy = None,None
ex,ey = None,None
tracker_type = 1  # デフォルトはMedianFlow

# トラッカーの辞書
TRACKER_TYPES = {
    1: ('MedianFlow', cv2.legacy.TrackerMedianFlow_create),
    2: ('Boosting', cv2.legacy.TrackerBoosting_create),
    3: ('MIL', cv2.legacy.TrackerMIL_create),
    4: ('TLD', cv2.legacy.TrackerTLD_create),
    5: ('KCF', cv2.legacy.TrackerKCF_create),
    6: ('MOSSE', cv2.legacy.TrackerMOSSE_create),
    7: ('CSRT', cv2.legacy.TrackerCSRT_create),
}

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

def show_tracker_menu():
    """利用可能なトラッカーのメニューを表示"""
    print("\n=== 利用可能なトラッキングアルゴリズム ===")
    for key, (name, _) in TRACKER_TYPES.items():
        print(f"{key}: {name}")
    print("=======================================")
    print("キーボード操作:")
    print("  s: 動画一時停止 → ROI指定 → 追跡開始")
    print("  p: 動画再開")
    print("  1-7: 追跡アルゴリズム選択")
    print("  ESC: 終了")

def main():
    global ix,iy,ex,ey,frame,tracker,tracker_type

    # トラッカーを選択
    show_tracker_menu()

    cap = cv2.VideoCapture('./moving_vehicles.mp4')

    if not cap.isOpened():
        print("エラー: moving_vehicles.mp4 を開けません")
        return

    cv2.namedWindow("original",cv2.WINDOW_NORMAL)
    param = "original"
    cv2.setMouseCallback("original", draw_rectangle, param)

    pause = False
    track_start = -1
    current_tracker_name = TRACKER_TYPES[tracker_type][0]
    # 追跡軌跡を保持するバッファ（最大100点）
    pts = deque(maxlen=100)

    while True:
        if pause == True:
            frame_d = frame_s.copy()

            # ROI指定中の矩形を描画
            if ix is not None and iy is not None:
                cv2.rectangle(frame_d,(ix,iy),(ex,ey),(0,255,255),2)

            # ウィンドウタイトルに現在のトラッカーと状態を表示
            window_title = f"Tracker: {current_tracker_name} | Press s to select ROI, p to start tracking"
            cv2.setWindowTitle("original", window_title)
            # 追跡軌跡を描画
            if len(pts) > 1:
                for i in range(1, len(pts)):
                    if pts[i - 1] is None or pts[i] is None:
                        continue
                    cv2.line(frame_d, pts[i - 1], pts[i], (0, 255, 0), 2)

            cv2.imshow('original',frame_d)
            track_start = 0
        else:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame_s = frame.copy()

            if track_start == 0:
                # ROI指定が完了したら、トラッカーを初期化
                if ex is not None and ey is not None and ix is not None and iy is not None:
                    w = ex-ix
                    h = ey-iy
                    if w > 0 and h > 0:
                        try:
                            tracker = TRACKER_TYPES[tracker_type][1]()
                            print(f"\nトラッカー: {current_tracker_name}")
                            print(f"ROI座標: ({ix},{iy}) サイズ: {w}×{h}")
                            ok = tracker.init(frame,(ix,iy,w,h))
                            if ok:
                                # 軌跡をリセットし、初期位置を追加
                                pts.clear()
                                center = (int(ix + w/2), int(iy + h/2))
                                pts.append(center)
                                track_start = 1
                            else:
                                print("エラー: トラッカーの初期化に失敗")
                                pause = True
                        except Exception as e:
                            print(f"エラー: {e}")
                            pause = True

            if track_start == 1:
                try:
                    track, bbox = tracker.update(frame)
                    if track:
                        p1 = (int(bbox[0]), int(bbox[1]))
                        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                        cv2.rectangle(frame,p1,p2,(0,255,255),2)
                        # 中心点を算出して軌跡に追加
                        cx = int(bbox[0] + bbox[2] / 2)
                        cy = int(bbox[1] + bbox[3] / 2)
                        pts.append((cx, cy))
                    else:
                        # 追跡が失敗した場合は状態をリセット
                        track_start = -1
                except Exception as e:
                    print(f"追跡エラー: {e}")
                    track_start = -1

            # 追跡軌跡を描画
            if len(pts) > 1:
                for i in range(1, len(pts)):
                    if pts[i - 1] is None or pts[i] is None:
                        continue
                    cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0), 2)

            # ウィンドウタイトルに現在のトラッカーを表示
            window_title = f"Tracker: {current_tracker_name} | Press 's' to pause"
            cv2.setWindowTitle("original", window_title)
            cv2.imshow('original',frame)

        key = cv2.waitKey(30) & 0xFF

        if key == 27:  # ESC
            break
        elif key == ord('s'):  # s キー: 一時停止してROI指定
            pause = True
            ix, iy = None, None
            ex, ey = None, None
            # ROI指定中は軌跡を消しておく
            pts.clear()
        elif key == ord('p'):  # p キー: 再開
            pause = False
        elif key in range(ord('1'), ord('8')):  # 1-7 キー: トラッカー選択
            new_type = int(chr(key))
            if new_type in TRACKER_TYPES:
                tracker_type = new_type
                current_tracker_name = TRACKER_TYPES[tracker_type][0]
                print(f"\nトラッカーを '{current_tracker_name}' に変更しました")
                pause = True
                ix, iy = None, None
                ex, ey = None, None
                track_start = -1
                pts.clear()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()