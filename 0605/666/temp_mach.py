import cv2
import numpy as np

def load_img(path):
    with open(path, 'rb') as f:
        return cv2.imdecode(np.frombuffer(f.read(), dtype=np.uint8), cv2.IMREAD_COLOR)

def main():
    img_path = r"C:\Users\ktc\Desktop\消さないでね\授業\授業\360_F_582923026_kQi1CuHQRnzoCw3Xu6qnMmrcCAxXkyw9.jpg"
    temp_path = r"C:\Users\ktc\Desktop\消さないでね\授業\授業\temp.jpg"

    img = load_img(img_path)
    template = load_img(temp_path)

    algorithms = [
        ("SSD", cv2.TM_SQDIFF),
        ("SAD", cv2.TM_SQDIFF_NORMED),
        ("NCC", cv2.TM_CCORR_NORMED),
        ("ZNCC", cv2.TM_CCOEFF_NORMED)
    ]

    print("1: SSD, 2: SAD, 3: NCC, 4: ZNCC")
    try:
        choice = int(input("アルゴリズムの番号を選択してください (1-4): ")) - 1
        algo_name, method = algorithms[choice]
    except (ValueError, IndexError):
        print("無効な入力です。")
        return

    print(f"{algo_name} でマッチングを実行します")

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_temp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    match = cv2.matchTemplate(gray_img, gray_temp, method)
    min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_pt
        val = min_value
    else:
        top_left = max_pt
        val = max_value

    h, w = template.shape[:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 3)
    cv2.putText(img, f"Val: {val:.3f}", (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # 画面に収まるようにリサイズ表示
    h_img, w_img = img.shape[:2]
    if h_img > 800 or w_img > 1200:
        scale = min(1200 / w_img, 800 / h_img)
        img = cv2.resize(img, None, fx=scale, fy=scale)

    cv2.imshow("Template", template)
    cv2.imshow("Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()