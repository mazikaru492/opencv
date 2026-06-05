from pathlib import Path
import numpy as np
import cv2

def imread_unicode(path: Path):
    data = np.fromfile(str(path), dtype=np.uint8)
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)

def main():

    base_dir = Path(__file__).resolve().parent

    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        print('カスケードファイルを読み込めません:', cascade_path)
        return

    image_path = base_dir / 'model.jpg'
    img = imread_unicode(image_path)
    if img is None:
        print('画像を読み込めません:', image_path)
        return
    
    img = cv2.resize(img,None,fx=2,fy=2)
    height = img.shape[0]
    width = img.shape[1]
    print(height, width)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(20,20))

    for x, y, w, h in faces:
        face = img[y:y+h,x:x+w,:]
        # ガウシアンフィルタのカーネルサイズは必ず「奇数」である必要があります
        mosaic = cv2.GaussianBlur(face, (79, 79), 0)
        img[y:y+h,x:x+w,:] = mosaic
    
    cv2.imshow('Mosaic', img)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()