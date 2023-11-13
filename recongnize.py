import pybase64
import cv2
from ultralytics import YOLO
import supervision as sv
import random
from PIL import Image
import requests
from io import BytesIO
import requests  
from bs4 import BeautifulSoup
from torch import rand  
from flask import Flask, jsonify
import os
import datetime
from dotenv import load_dotenv
from threading import Thread
import pymongo
import time
from time import sleep, perf_counter

load_dotenv()

mongoURI = os.getenv('MONGO_URI')

myclient = pymongo.MongoClient(mongoURI)
mydb = myclient["Cameras"]
myCamera = mydb["Camera"]
myCount = mydb["Count"]

class recongnize:
    #get data from URL and save in database
    def getCameras(self):
        url = "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/"
        arquivo = "snap_c1.jpg"
        
        pipeline = [
            {"$sort": {
            "lastUpdate": -1
            }},
            {"$group": {
            "_id": {
                "id": "$id"
            },
            "id": {
                "$first": "$id"
            },
            "camera": {
                "$first": "$camera"
            },
            "rua": {
                "$first": "$rua"
            },
            "url": {
                "$first": "$url"
            },
            "count": {
                "$first": "$count"
            },
            "lastUpdate": {
                "$first": "$lastUpdate"
            }
            }},
        ]
        
        cameras = list(myCamera.aggregate(pipeline))
        resultCamera = []
        
        
        for camera in cameras:
            randomNumber = random.randint(10000000, 99999999)
            idCamera = camera["id"]   
            cameraName = camera["camera"]
            rua = camera["rua"]
            urlCam = url + cameraName + "/" + arquivo + "?" + str(randomNumber)
            
            
            response = requests.get(urlCam)
            #Transformando ela em Bytes para o PIL ler
            newImage = Image.open(BytesIO(response.content))
            newImage.save("public/image.jpg")
            
            model = YOLO("yolov8n.pt")
            image = cv2.imread("public/image.jpg")
            results = model(image)[0]
            detections = sv.Detections.from_ultralytics(results)
            detections = detections[detections.confidence > 0.1]
            bounding_box_annotator = sv.BoundingBoxAnnotator()
            label_annotator = sv.LabelAnnotator()

            labels = [
                results.names[class_id]
                for class_id in detections.class_id
            ]

            annotated_image = bounding_box_annotator.annotate(
                scene=image, detections=detections)
            annotated_image = label_annotator.annotate(
                scene=annotated_image, detections=detections, labels=labels) 
            imgPath = "public/static/cameras/" + idCamera + ".jpg"
            cv2.imwrite(imgPath, annotated_image)
            with open(imgPath, "rb") as img_file:
                timeNow = datetime.datetime.now()
                # my_string = pybase64.standard_b64encode(img_file.read())
                countLabels = {i:labels.count(i) for i in labels}
                myCamera.insert_one({"id": idCamera, "camera": cameraName, "rua": rua,"url": urlCam,"count": countLabels,"lastUpdate": timeNow,})         

            #TO DECODE STRING TO IMAGE
            # decoded_data=pybase64.standard_b64decode((my_string))
            # img_file = open('image3.jpg', 'wb')
            # img_file.write(decoded_data)
            # img_file.close()

    def loopCameras(self):
        while True:
            start_time = perf_counter()
            self.getCameras()
            end_time = perf_counter()
            print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
            time.sleep(5)
        
    def main(self):
        t1 = Thread(target=self.loopCameras)
        t1.start()
    