from pathlib import Path
import cv2

def main():
    base_dir = Path(__file__).resolve().parent
    video_path = base_dir / 'moving_vehicles.mp4'

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print("動画を読み込めません:", video_path)
        return

    # 利用可能なトラッキングアルゴリズムのリスト
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
    current_tracker_index = 4  # デフォルトは MEDIANFLOW

    tracker = None
    tracking = False

    print("=== トラッキングアルゴリズムの切り替え機能 ===")
    print("動画上でキーボードの 0～6 を押すとアルゴリズムを変更できます。")
    for i, t in enumerate(tracker_types):
        print(f"  {i}: {t}")
    print("==============================================")

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # トラッキング中の場合は追跡を更新して四角を描画
        if tracking and tracker is not None:
            success, bbox = tracker.update(frame)
            if success:
                # 追跡成功：矩形を描画
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 255), 2)
                cv2.putText(frame, f"{tracker_types[current_tracker_index]} Tracking", (20, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            else:
                # 追跡失敗（見失った場合）
                cv2.putText(frame, "Lost", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            # トラッキングしていない時の表示
            cv2.putText(frame, f"Tracker: {tracker_types[current_tracker_index]} (Press 's' to select ROI)", 
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Tracking", frame)

        key = cv2.waitKey(30)
        
        if key == 27: # ESCキーで終了
            break
        elif key == ord('s'): # sキーで一時停止し、領域指定(ROI)
            roi = cv2.selectROI("Tracking", frame, showCrosshair=True, fromCenter=False)
            
            # 正しく領域が選択された場合
            if roi != (0, 0, 0, 0):
                # 選択されているアルゴリズムのトラッカーを作る
                alg = tracker_types[current_tracker_index]
                if alg == 'BOOSTING':   tracker = cv2.legacy.TrackerBoosting_create()
                elif alg == 'MIL':      tracker = cv2.legacy.TrackerMIL_create()
                elif alg == 'KCF':      tracker = cv2.legacy.TrackerKCF_create()
                elif alg == 'TLD':      tracker = cv2.legacy.TrackerTLD_create()
                elif alg == 'MEDIANFLOW': tracker = cv2.legacy.TrackerMedianFlow_create()
                elif alg == 'MOSSE':    tracker = cv2.legacy.TrackerMOSSE_create()
                elif alg == 'CSRT':     tracker = cv2.legacy.TrackerCSRT_create()
                
                # 指定した矩形でトラッカーを初期化
                tracker.init(frame, roi)
                tracking = True
                
        # 0〜6の数字キーが押されたらアルゴリズムを切り替える
        elif ord('0') <= key <= ord('6'):
            current_tracker_index = key - ord('0')
            print(f"アルゴリズムを {tracker_types[current_tracker_index]} に変更しました！ 再度 's' を押して指定してください。")
            tracking = False # 切り替えたら一旦トラッキングをリセットする

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()