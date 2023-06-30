from pymongo.mongo_client import MongoClient
from PIL import Image
import io
import matplotlib.pyplot as plt


class DB:
    def __init__(self, plate_Num, img):
        self.plate_Num = plate_Num
        self.img = img
        self.db = None
        self.cluster = None
        self.fs = None
        self.fs_id = None
        self.filename = self.plate_Num

    def Connection(self):
        try:
            uri = "mongodb+srv://anassh23:anassh23@graduationproject.mvnqqsu.mongodb.net/?retryWrites=true&w=majority"
            self.cluster = MongoClient(uri)

            self.cluster.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")

        except Exception as err:
            print(f"Error in mongodb connection: {err}")

    def Upload(self):
        self.db = self.cluster.Data
        collection = self.db["data"]

        im = Image.open(self.img)

        image_bytes = io.BytesIO()
        im.save(image_bytes, format='JPEG')

        post = {
            "-id": 0,
            "plate number": self.plate_Num,
            'data': image_bytes.getvalue()
        }

        collection.insert_one(post)
