import requests
import os
from data import DB
import cv2


class Plate:

    def __init__(self, img):
        self.img = img
        self.plateNum = ""
        # self.plate_Recognition()

    def plate_Recognition(self):
        regions = ['jo', 'jo']  # Change to your country
        with open(self.img, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),  # Optional
                files=dict(upload=fp),
                headers={'Authorization': 'Token 8fffeb34f4eca6304cff6d133e458c9031bc2939'})
        # pprint(response.json())
        response = response.json()
        self.plateNum = (response["results"][0]["candidates"][0]["plate"])

        if os.path.exists(self.plateNum):
            pass
        else:
            os.mkdir(self.plateNum)
        return str(self.plateNum)
