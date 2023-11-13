#set number random to variable each 5 second
#where number is like timestamp 
from more_itertools import last
from numpy import rec
import pymongo
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
import time
import datetime
from dotenv import load_dotenv
from time import sleep, perf_counter
from threading import Thread
import json 
from bson import json_util
from recongnize import recongnize
from utils import utils
from flask_cors import CORS
from flask import send_from_directory
load_dotenv()

# https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1525/snap_c1.jpg?
mongoURI = os.getenv('MONGO_URI')

myclient = pymongo.MongoClient(mongoURI)
mydb = myclient["Cameras"]
myCamera = mydb["Camera"]
myCount = mydb["Count"]

cameras = recongnize()
_utils = utils()
cameras.main()

app = Flask(__name__, static_url_path='', 
            static_folder='public/static')
CORS(app)

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
    
@app.route("/api/v1/cameras/", methods=["GET"])
def getCameras():
    count_from_db = list(myCamera.aggregate(pipeline))
    if count_from_db:
        resultJson = _utils.toJson(count_from_db)
        return jsonify({"cameras":resultJson}), 200
    else:
        return jsonify({'msg': 'Camera not found'}), 404

@app.route('/<int:number>/')
def incrementer(number):
    return jsonify(number=number+1)

@app.route('/<string:name>/')
def hello(name):
    return "Hello " + name

app.run()







