import shutil

from ultralytics import YOLO
import cv2
import os
from PIL import Image
from phone import PhoneDetection
import cvzone
import math
import time


class Car():
    def __init__(self, cap):
        self.frame = 0
        self.c = 0
        self.cap = cap
        self.m1 = r"..\TwoModels\weight\yolov8m.pt"

        self.mask = cv2.imread(r"C:\Users\noora\Desktop\maskb.png")

        self.carDetection()

    def carDetection(self):

        model = YOLO(self.m1)

        while True:

            success, img = self.cap.read()
            imgRegion = cv2.bitwise_and(img, self.mask)
            img = imgRegion
            if self.frame % 30 == 0:
                results = model(img, stream=True)
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        if box.cls[0].item() == 2.0 or box.cls[0].item() == 5.0 or box.cls[0].item() == 7.0:
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            self.save_Frames(img, x1, y1, x2, y2)
            else:
                self.frame += 1

            cv2.waitKey(1)

    def save_Frames(self, img, x1, y1, x2, y2):
        box = (x1, y1, x2, y2)
        if not os.path.exists("car_frames"):
            os.mkdir("car_frames")
        if self.frame % 30 == 0:  # assuming the cam takes 60 fps
            cv2.imwrite("car_frames/%d.jpg" % self.c, img)
            self.calldetect2(f"car_frames/{self.c}.jpg", box)

            self.frame += 1
            self.c += 1
        else:
            self.frame += 1

    def calldetect2(self, img, box):
        img2 = Image.open(img)
        img3 = img2.crop(box)
        if not os.path.exists("cropped_car"):
            os.mkdir("cropped_car")
        os.chdir("cropped_car")
        img3.save("test.jpg")
        phone = PhoneDetection()
        phone.detect2("test.jpg")
        os.chdir(r"..")


cap = cv2.VideoCapture(r"C:\Users\noora\Downloads\IMG_3935.MOV")

v1 = Car(cap)
