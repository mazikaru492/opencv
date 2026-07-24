import os

import cv2


def main():
	img_path = os.path.join(os.path.dirname(__file__), "..", "ball.jpg")
	img = cv2.imread(img_path)

	if img is None:
		print("ball.jpg が見つかりません")
		return

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	blue_mask = cv2.inRange(hsv, (100, 80, 50), (110, 255, 255))
	green_mask = cv2.inRange(hsv, (86, 80, 50), (100, 255, 255))
	mask = cv2.bitwise_or(blue_mask, green_mask)

	result = img.copy()
	result[mask > 0] = (0, 0, 255)

	cv2.imshow("Image", img)
	cv2.imshow("HSV", hsv)
	cv2.imshow("Red Balls", result)

	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()