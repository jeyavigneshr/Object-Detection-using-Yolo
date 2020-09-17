#Organized import statements
from __future__ import print_function

import socket
import numpy as np
from PIL import Image
import sys
import threading

from datetime import datetime
from client_send_message import MessageSender
from predict import PredictCarsData

try:
    import cPickle as pickle
except ImportError:
    import pickle

#Prediction for query 2 car type
sock = socket.socket()
print("Established Socket Connection")
sock.bind((b'', 5000))
sock.listen(1)
#Creating objects for sender and prediction class
sender = MessageSender()
prediction = PredictCarsData()
index = 0 
while True:
    conn, addr = sock.accept()
    outdata = b''
    while True:
        int_block = conn.recv(4096)
        if not int_block:
            break
        outdata += int_block
    if sys.version_info.major < 3:
        uni_input = pickle.loads(outdata)
    else:
        uni_input = pickle.loads(outdata, encoding='bytes')
    if uni_input is not None:
        recv_time = datetime.now()
        image = uni_input.tolist()
        images_list = list()
        images_list.append(image)
        images_list = np.array(images_list, dtype=float)
        type_class = prediction.predict(images_list)
        proc_time = "{:f}".format(float((datetime.now() - recv_time).total_seconds()))
        response_json = dict()
        response_json['car_type_time'] = proc_time
        response_json['car_type'] = type_class
        print("car_type",response_json)
        conn.sendall(pickle.dumps(response_json,protocol=2))
        conn.close()
        index = index + 1
    