from pathlib import Path
import numpy as np
import cv2

def main():
    base_dir = Path(__file__).resolve().parent
    video_path = base_dir / 'people_move.mp4'
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print("動画ファイルを読み込めませんでした。ファイル名を確認してください:", video_path)
        return

    # フレームレートを取得し、それに合わせた待機時間(ミリ秒)を計算
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps) if fps > 0 else 33

    play = True

    while True:
        if play == True:
            ret, frame = cap.read()
            if not ret:
                print("動画の再生が終了しました。")
                break
            cv2.imshow('camera' , frame)
        key = cv2.waitKey(delay)
        if key == 115:
            play = False
        elif key == 112:
            play = True
        elif key == 27:
            break
        

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()