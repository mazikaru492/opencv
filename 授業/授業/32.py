import cv2
import numpy as np
import argparse
from pathlib import Path


def imread_unicode(path):
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return img


def imwrite_unicode(path, img):
    ext = Path(path).suffix
    result, encoded = cv2.imencode(ext, img)
    if result:
        encoded.tofile(str(path))


def cluster_values(values, tolerance):
    """
    近い座標をまとめて、行・列の代表座標にする
    """
    values = sorted(values)
    clusters = []

    for v in values:
        if not clusters:
            clusters.append([v])
        else:
            center = np.median(clusters[-1])
            if abs(v - center) <= tolerance:
                clusters[-1].append(v)
            else:
                clusters.append([v])

    return [int(round(np.median(c))) for c in clusters]


def find_template_peaks(gray, template, threshold):
    """
    ZNCCでテンプレートと似ている場所を探す
    """
    h, w = template.shape[:2]

    result = cv2.matchTemplate(
        gray,
        template,
        cv2.TM_CCOEFF_NORMED
    )

    # 局所最大だけを取り出す
    kernel_w = max(3, w // 2)
    kernel_h = max(3, h // 2)
    kernel = np.ones((kernel_h, kernel_w), np.uint8)

    local_max = cv2.dilate(result, kernel)
    mask = (result == local_max) & (result >= threshold)

    ys, xs = np.where(mask)

    points = []
    for x, y in zip(xs, ys):
        points.append((x, y, result[y, x]))

    # スコア順に並べる
    points.sort(key=lambda p: p[2], reverse=True)

    # 近すぎる重複を削除
    picked = []
    for x, y, score in points:
        duplicate = False
        for px, py, _ in picked:
            if abs(x - px) < w * 0.6 and abs(y - py) < h * 0.6:
                duplicate = True
                break

        if not duplicate:
            picked.append((x, y, score))

    return picked


def local_zncc(gray, template, x, y, search_range=4):
    """
    予想位置の少し周辺を探して、一番ZNCCが高い位置とスコアを返す
    """
    h, w = template.shape[:2]
    img_h, img_w = gray.shape[:2]

    x1 = max(0, x - search_range)
    y1 = max(0, y - search_range)
    x2 = min(img_w, x + w + search_range)
    y2 = min(img_h, y + h + search_range)

    area = gray[y1:y2, x1:x2]

    if area.shape[0] < h or area.shape[1] < w:
        return x, y, -1.0

    result = cv2.matchTemplate(area, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    best_x = x1 + max_loc[0]
    best_y = y1 + max_loc[1]

    return best_x, best_y, max_val


def process_image(image_path, match_th=0.72, diff_th=None):
    image_path = Path(image_path)

    img = imread_unicode(image_path)
    if img is None:
        print(f"画像を読み込めませんでした: {image_path}")
        return

    print(f"\n処理中: {image_path.name}")

    # マウスで正しい漢字を1つ選択
    roi = cv2.selectROI(
        "正しい漢字を1文字だけドラッグして選択 → Enter",
        img,
        showCrosshair=True,
        fromCenter=False
    )
    cv2.destroyWindow("正しい漢字を1文字だけドラッグして選択 → Enter")

    x, y, w, h = roi

    if w == 0 or h == 0:
        print("選択がキャンセルされました")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = gray[y:y + h, x:x + w]

    # ZNCCで正しい漢字と似ている位置を探す
    peaks = find_template_peaks(gray, template, match_th)

    if len(peaks) < 3:
        print("テンプレートに似ている文字が少なすぎます。")
        print("match_thを下げてください。例: --match-th 0.65")
        return

    xs = [p[0] for p in peaks]
    ys = [p[1] for p in peaks]

    # 行・列の推定
    cols = cluster_values(xs, tolerance=max(2, int(w * 0.45)))
    rows = cluster_values(ys, tolerance=max(2, int(h * 0.45)))

    print(f"推定: {len(rows)} 行 × {len(cols)} 列")

    scores = []
    cells = []

    # 全マスをZNCCで比較
    for row_y in rows:
        for col_x in cols:
            best_x, best_y, score = local_zncc(
                gray,
                template,
                col_x,
                row_y,
                search_range=max(3, min(w, h) // 5)
            )

            scores.append(score)
            cells.append((best_x, best_y, score))

    scores_np = np.array(scores)

    # diff_thを指定しない場合は自動で決める
    if diff_th is None:
        median = np.median(scores_np)
        mad = np.median(np.abs(scores_np - median))

        diff_th = median - max(0.07, mad * 3)
        diff_th = max(0.55, min(0.95, diff_th))

    print(f"違う文字判定しきい値: {diff_th:.3f}")

    output = img.copy()
    diff_count = 0

    for cx, cy, score in cells:
        if score < diff_th:
            cv2.rectangle(
                output,
                (cx, cy),
                (cx + w, cy + h),
                (0, 0, 255),
                2
            )
            diff_count += 1

    print(f"違う文字候補: {diff_count} 個")

    save_path = image_path.with_name(image_path.stem + "_result.jpg")
    imwrite_unicode(save_path, output)

    cv2.imshow("result", output)
    print(f"結果を保存しました: {save_path}")
    print("何かキーを押すと次へ進みます")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "images",
        nargs="+",
        help="処理する画像ファイル"
    )
    parser.add_argument(
        "--match-th",
        type=float,
        default=0.72,
        help="正しい漢字を探すZNCCしきい値"
    )
    parser.add_argument(
        "--diff-th",
        type=float,
        default=None,
        help="違う漢字と判定するZNCCしきい値。未指定なら自動"
    )

    args = parser.parse_args()

    for image in args.images:
        process_image(
            image,
            match_th=args.match_th,
            diff_th=args.diff_th
        )


if __name__ == "__main__":
    main()