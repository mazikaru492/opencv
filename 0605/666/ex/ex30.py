import os
import cv2
import numpy as np


def main():
	base_dir = os.path.dirname(os.path.abspath(__file__))
	image_path = os.path.join(base_dir, "..", "ball.jpg")

	img = cv2.imread(image_path)
	if img is None:
		raise FileNotFoundError(f"画像を読み込めません: {image_path}")

	# 平滑化
	img_blur = cv2.GaussianBlur(img, (11, 11), 0)

	# HSV に変換
	hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)

	# 色領域の閾値（ここは pink を想定）
	# OpenCV の H は 0-179
	h_lower = 165
	h_upper = 180
	s_lower = 32
	v_lower = 0

	lower = (h_lower, s_lower, v_lower)
	upper = (h_upper, 255, 255)

	# マスク作成
	mask = cv2.inRange(hsv, lower, upper)

	# ノイズ除去（オープン/クローズ）
	kernel = np.ones((5, 5), np.uint8)
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

	# 輪郭抽出
	contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# 元画像に輪郭を描画
	out = img.copy()
	cv2.drawContours(out, contours, -1, (0, 255, 255), 2)

	cv2.imshow('Mask', mask)
	cv2.imshow('Contours', out)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()

