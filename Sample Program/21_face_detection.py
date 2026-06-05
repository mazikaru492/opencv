from pathlib import Path
import numpy as np
import cv2


def imread_unicode(path: Path):
    # cv2.imread can fail with non-ASCII paths on some Windows builds.
    data = np.fromfile(str(path), dtype=np.uint8)
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)

def main():

    base_dir = Path(__file__).resolve().parent

    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        print('カスケードファイルを読み込めません:', cascade_path)
        return

    image_path = base_dir / 'model.jpg'
    img = imread_unicode(image_path)
    if img is None:
        print('画像を読み込めません:', image_path)
        print('このスクリプトと同じフォルダに model.jpg があるか確認してください。')
        return
    
    img = cv2.resize(img,None,fx=2,fy=2)
    height = img.shape[0]
    width = img.shape[1]
    print(height, width)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 顔が小さい画像でも認識できるように minSize を 20,20 に小さくします
    faces = cascade.detectMultiScale(gray,scaleFactor=1.05, minNeighbors=3, minSize=(20,20))

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    cv2.imshow('Faces', img)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()