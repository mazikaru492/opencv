import numpy as np
import cv2

def main():

    cascade_path = './haarcascade_frontalface_default.xml'
    cascade = cv2.CascadeClassifier(cascade_path)

    img = cv2.imread("./faces.jpg")
    
    img = cv2.resize(img,None,fx=0.3,fy=0.3)
    height = img.shape[0]
    width = img.shape[1]
    print(height, width)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(gray,scaleFactor=1.1, minNeighbors=4, minSize=(50,50))

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
    
    cv2.imshow('Faces', img)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()