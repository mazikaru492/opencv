import cv2
import numpy as np


def main():
    img_path = r"C:\Users\ktc\Desktop\Opencv\0605\666\MURATA.jpg"
    img = cv2.imread(img_path)

    if img is None:
        print(f"エラー: 画像が読み込めませんでした。:\n{img_path}")
        return

    # --- 画面サイズを小さくするための縮小処理 ---
    scale_factor = 0.5  # 0.5で半分の大きさ（好みに合わせて 0.3 や 0.7 に変更してください）
    img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)
    # ----------------------------------------

    h, w = img.shape[:2]
    diagonal = int(np.sqrt(w**2 + h**2))

    canvas = np.zeros((diagonal, diagonal, 3), dtype=np.uint8)

    pad_x = (diagonal - w) // 2
    pad_y = (diagonal - h) // 2
    canvas[pad_y : pad_y + h, pad_x : pad_x + w] = img

    center = (diagonal // 2, diagonal // 2)
    scale = 1.0

    angle = 0
    while angle <= 360:
        trans = cv2.getRotationMatrix2D(center, float(angle), scale)
        r_img = cv2.warpAffine(canvas, trans, (diagonal, diagonal))

        cv2.imshow("Continuous Rotation", r_img)

        if cv2.waitKey(30) & 0xFF == 27:
            break

        angle += 2

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()