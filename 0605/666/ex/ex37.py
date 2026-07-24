from pathlib import Path

import cv2


def main():
	base_dir = Path(__file__).resolve().parent
	candidates = [
		base_dir.parent / 'people_move.mp4',
		base_dir.parent / 'people move.mp4',
	]

	video_path = next((path for path in candidates if path.exists()), candidates[0])
	cap = cv2.VideoCapture(str(video_path))

	if not cap.isOpened():
		print('動画ファイルを読み込めませんでした。ファイル名を確認してください:', video_path)
		return

	fps = cap.get(cv2.CAP_PROP_FPS)
	delay = int(1000 / fps) if fps > 0 else 33
	total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	frame_no = 0
	play = True

	while True:
		if play:
			ret, frame = cap.read()
			if not ret:
				print('動画の再生が終了しました。')
				break

			frame_no += 1
			text = f'{frame_no}/{total_frames}'
			cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2, cv2.LINE_AA)
			cv2.imshow('camera', frame)

		key = cv2.waitKey(delay)
		if key == 27:
			break
		elif key == 115:
			play = False
		elif key == 112:
			play = True
			
	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()