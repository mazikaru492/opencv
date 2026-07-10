import os

import cv2


def on_mouse(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		window_name, rgb_image, display_image, hsv_image = param

		cv2.circle(display_image, (x, y), 5, (0, 0, 255), -1)
		cv2.imshow(window_name, display_image)

		r, g, b = rgb_image[y, x]
		h, s, v = hsv_image[y, x]

		print(f"x={x}, y={y}")
		print(f"RGB=({r}, {g}, {b})")
		print(f"HSV=({h}, {s}, {v})")
		print()


def main():
	base_dir = os.path.dirname(os.path.abspath(__file__))
	image_path = os.path.join(base_dir, "..", "ball.jpg")

	bgr_image = cv2.imread(image_path)
	if bgr_image is None:
		raise FileNotFoundError(f"画像を読み込めません: {image_path}")

	rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
	hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
	display_image = bgr_image.copy()

	window_name = "Ball"
	cv2.imshow(window_name, display_image)
	cv2.setMouseCallback(window_name, on_mouse, (window_name, rgb_image, display_image, hsv_image))

	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
