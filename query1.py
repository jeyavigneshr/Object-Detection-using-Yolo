# Organized Import Statements
from __future__ import print_function
import json
import socket
import sys
import threading
from datetime import datetime
import numpy as np
from PIL import Imag
from client_send_message import MessageSender
from color_classifier import colordetection
from yolo import YOLO

try:
    import cPickle as pickle
except ImportError:
    import pickle

#Creating a message sender
sender = MessageSender()
#Object for yolo
yolo = YOLO()
#Creating a socket
sock = socket.socket()
print("Establishing Socket Connection")
sock.bind((b'',6000))
sock.listen(1)

index = 0
while True:
    conn, address = sock.accept()
    data_list = []
    while True:
        blk = conn.recv(4096)
        if not blk: 
            break
        data_list.append(blk)
    data = b"".join(data_list)
    #Loading unserialized input using pickle
    if sys.version_info.major < 3:
        uni_input = pickle.loads(data)
    else:
        uni_input = pickle.loads(data,encoding='bytes')
    if uni_input is not None:
        image = Image.fromarray(uni_input)
        rec = datetime.now()
        response = yolo.detect_image(image)
        response_class = len(response)
        proc_time = "{:f}".format(float((datetime.now() -rec).total_seconds()))
        has_car = False
        
        if response_class > 0:
            has_car = True
        resp_json = dict()
        resp_json['has_car'] = has_car
        resp_json['no_cars'] = response_class
        resp_json['no_cars_time'] = proc_time
        rec = datetime.now()
        detected_colours = list()
        for _i,_r in enumerate(response):
                cropped_image = image.crop(_r)
                cropped_image = cropped_image.resize((224,224))
                cropped_image = np.array(cropped_image)
                car_color = colordetection(cropped_image)
                detected_colours.append(car_color)
        det_col = "|".join(detected_colours)
        processed_time = "{:f}".format(float((datetime.now() - rec).total_seconds()))
        if not has_car:
            processed_time = ""

        resp_json['colours_detected'] = det_col
        resp_json['colours_detected_time'] = processed_time
        print("Colour Detected ---------",resp_json)
        conn.sendall(pickle.dumps(resp_json,protocol=2))
        conn.close()
        index = index + 1
