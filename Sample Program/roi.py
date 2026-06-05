from pathlib import Path
import numpy as np
import cv2

def main():
    base_dir = Path(__file__).resolve().parent
    video_path = base_dir / 'moving_vehicles.mp4'

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print("動画を読み込めません:", video_path)
        return

    pause = False
    roi = None
    paused_frame = None

    while True:
        if not pause:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            paused_frame = frame
        else:
            frame = paused_frame

        # ROIが指定されていれば、毎フレーム黄色い四角を描画
        display_frame = frame.copy()
        if roi is not None:
            x, y, w, h = roi
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        cv2.imshow('roi_window', display_frame)

        key = cv2.waitKey(30)
        
        if key == 27: # ESCキーで終了
            break
        elif key == ord('s'): # 's'キーで一時停止し、selectROIで領域指定
            pause = True
            # selectROIを呼び出してマウスでドラッグして領域を決める
            # 決定はスペースかエンター、キャンセルはc
            roi = cv2.selectROI('roi_window', frame, showCrosshair=True, fromCenter=False)
            if roi == (0, 0, 0, 0):
                roi = None
            
            # 再生を再開したい場合はスペース/エンターを押した後に 'p' で再開（またはそのまま自動再開）
            pause = False # 領域指定が終わったら再生再開するようにする

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()