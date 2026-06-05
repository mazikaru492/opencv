import numpy as np
import cv2

def main():
	img = cv2.imread("./ktech.jpg")
	height,width = img.shape[:2]
	print(width,height)

	print("height:",img.shape[0])
	print("width:",img.shape[1])
	print(img.shape[2])
	
	cv2.imshow("Image", img)

	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()