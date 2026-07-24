import os
import cv2


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 代表的な候補パス（スペースあり/なし）
    candidates = [
        os.path.join(base_dir, "..", "people move.mp4"),
        os.path.join(base_dir, "..", "people_move.mp4"),
    ]

    video_path = None
    for p in candidates:
        if os.path.exists(p):
            video_path = p
            break

    if video_path is None:
        # 最初の候補を使って開いてみる（存在しなくてもエラーメッセージを出す）
        video_path = candidates[0]

    print(f"Opening video: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("動画を開けませんでした。ファイルパスを確認してください。")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("--- 動画プロパティ ---")
    print(f"幅 (width)         : {width}")
    print(f"高さ (height)       : {height}")
    print(f"フレームレート (fps): {fps:.2f}")
    print(f"総フレーム数       : {frame_count}")
    if fps > 0:
        duration = frame_count / fps
        print(f"再生時間 (秒)       : {duration:.2f} s")

    cap.release()


if __name__ == '__main__':
    main()
#683918