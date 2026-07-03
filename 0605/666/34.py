import cv2
import numpy as np


def main():
    img_path = r"C:\Users\ktc\Desktop\Opencv\0605\666\poster.jpg"
    img = cv2.imread(img_path)

    if img is None:
        print(f"エラー: 画像が読み込めませんでした。:\n{img_path}")
        return

    pt1 = (85, 52)
    pt2 = (228, 115)
    pt3 = (237, 332)
    pt4 = (103, 422)

    w = 300
    h = 300
    d = 100

    pp1 = (d, d)
    pp2 = (w + d, d)
    pp3 = (w + d, h + d)
    pp4 = (d, h + d)

    p_original = np.float32([pt1, pt2, pt3, pt4])
    p_trans = np.float32([pp1, pp2, pp3, pp4])

    M = cv2.getPerspectiveTransform(p_original, p_trans)

    canvas_w = w + 2 * d
    canvas_h = h + 2 * d
    img_p = cv2.warpPerspective(img, M, (canvas_w, canvas_h))

    cv2.imshow("Original", img)
    cv2.imshow("Perspective Correction", img_p)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()