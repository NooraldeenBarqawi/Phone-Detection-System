import os
from ultralytics import YOLO
import cv2
from os import listdir
from data import DB
from save_output import Plate


class PhoneDetection:
    def __init__(self):
        self.__m1 = r"C:\Users\noora\Desktop\TwoModels\weight\yolov8x.pt"
        self.cord = []
        self.counter = 0

    def detect2(self, path):
        print("from Phone")
        model = YOLO(self.__m1)
        results = model(path, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                if box.cls[0].item() == 67.0:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    self.cord = [x1, y1, x2, y2]
                    start_point = (self.cord[0], self.cord[1])
                    end_point = (self.cord[2], self.cord[3])
                    color = (255, 0, 0)
                    thickness = 2
                    image = cv2.imread(path)
                    try:
                        image = cv2.rectangle(image, start_point, end_point, color, thickness)
                        cv2.imwrite("img.jpg", image)
                        plate = Plate("img.jpg")
                        p1 = plate.plate_Recognition()
                        os.chdir(p1)

                        cv2.imwrite("img.jpg", image)
                        # db = DB(p1, "img.jpj")
                        # db.Connection()
                        # db.Upload()

                        os.chdir(r"..")
                        cv2.imshow("img", image)
                    except:
                        print("did not find plate")
