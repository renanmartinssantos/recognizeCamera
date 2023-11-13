#set number random to variable each 5 second
#where number is like timestamp 
from more_itertools import last
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
load_dotenv()

# https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1525/snap_c1.jpg?
mongoURI = os.getenv('MONGO_URI')

myclient = pymongo.MongoClient(mongoURI)
mydb = myclient["Cameras"]
myCamera = mydb["Camera"]
myCount = mydb["Count"]

mydba = [{
        "id": "0391",
        "camera": "cam0391",
        "rua": "Nossa Senhora de Fátima - Jovino de Melo Sentido Bom Retiro",
    },{
        "id": "0393",
        "camera": "cam0393",
        "rua": "Nossa Senhora de Fátima - Jovino de Melo Sentido Tambores",
    },{
        "id": "0394",
        "camera": "cam0394",
        "rua": "Nossa Senhora de Fátima Franscisco Ferreira Canto Sentido São Jorge",
    },{
        "id": "1272",
        "camera": "cam1272",
        "rua": "Entrada da Cidade",
    },{
        "id": "1525",
        "camera": "cam1525",
        "rua": "Martins Fontes - Sentido Centro",
    },{
        "id": "1524",
        "camera": "cam1524",
        "rua": "Martins Fontes - Sentido São Paulo",
    },{
        "id": "1268",
        "camera": "cam1268",
        "rua": "Viaduto entrada da Cidade - Sentido Anchieta",
    },{
        "id": "1270",
        "camera": "cam1270",
        "rua": "Entrada da Cidade",
    },{
        "id": "1269",
        "camera": "cam1269",
        "rua": "Ponte Viaduto - Prefeito Paulo Gomes Barbosa",
    },{
        "id": "0401",
        "camera": "cam0401",
        "rua": "Subida do Morro da Nova Cintra",
    },
    {
        "id": "0399",
        "camera": "cam0399",
        "rua": "Moura Ribeiro - Sentido Carvalo de Mendonça",
    },
    {
        "id": "0377",
        "camera": "cam0377",
        "rua": "Divisa Praia - Santos/São Vicente - Sentido Itararé",
    },
    {
        "id": "0044",
        "camera": "cam0044",
        "rua": "Orquidário",
    },
    {
        "id": "0045",
        "camera": "cam0045",
        "rua": "Orquidário - Sentido Canal",
    },
    {
        "id": "1665",
        "camera": "cam1665",
        "rua": "Sentido Orquidário",
    },
    {
        "id": "1598",
        "camera": "cam1598",
        "rua": "Praia - Sentido Canal 1",
    }
]
#criar um for do mydba

for m in mydba:
    myCamera.insert_one({"id": m['id'], "camera": m['camera'], "rua": m['rua'], "lastUpdate": datetime.datetime.now()})





