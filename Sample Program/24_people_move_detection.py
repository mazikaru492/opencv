from pathlib import Path
import numpy as np
import cv2

def main():
    base_dir = Path(__file__).resolve().parent
    video_path = base_dir / 'people_move.mp4'

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print("動画を読み込めません:", video_path)
        return

    avg = None

    while True:
        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.GaussianBlur(frame, (5,5), 0)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if avg is None:
            avg = gray.copy().astype("float")

        cv2.accumulateWeighted(gray, avg, 0.6)
        
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
        th,bin = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)

        contours, hierachy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 100:
                x,y,w,h = cv2.boundingRect(contour)
                
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)

        cv2.imshow('original',frame)
        cv2.imshow('thresh',bin)

        key =cv2.waitKey(30)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()