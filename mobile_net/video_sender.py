import numpy as np
import cv2
import sys
import csv
import socket
import os
import time
import sys
from io import BytesIO
import pickle
from datetime import datetime

from client_send_message import MessageSender
from time import time as timer
from PIL import Image

start = datetime.now()
port = 5000
host = "localhost"
sender = MessageSender()
print("Established Server Connection")
query = "query3"

'''
Method uses opencv method to read the video and stream the video as frames
made use of tiny yolo method to replicate the video read function
'''
def video_reader(path):
    video = cv2.VideoCapture(path)
    if not video.isOpened():
        raise IOError("Couldn't open webcam or video")
    fps = video.get(cv2.CAP_PROP_FPS)
    print("FPS" , fps)
    fps /= 1000
    idx = 0
    video_FourCC = cv2.VideoWriter_fourcc(*"mp4v")
    video_fps       = video.get(cv2.CAP_PROP_FPS)   
    video_size      = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    file_name , ext = os.path.splitext(path)
    output_path = "{0}_out{1}".format(file_name,ext)     
    print(output_path)
    out_video_obj = cv2.VideoWriter(output_path, video_FourCC, 25, video_size)
    
    while True:
        
        retreived, frame = video.read()
        final_message = ""
        
        if retreived:
            
            _frame = np.array(frame)
            img = cv2.resize(frame , (224,224))
            
            if query in ["query1","query2","query3"]:
                
                s = socket.socket(socket.AF_INET,   socket.SOCK_STREAM)
                s.connect((host, 6000))
                serialized_data = pickle.dumps(img, protocol=2)
                s.sendall(serialized_data)
                s.shutdown(socket.SHUT_WR)
                data = b''
                block = s.recv(4096)
                data = block
                s.close()
                hasCar = {}
                
                if sys.version_info.major < 3:
                
                    hasCar = pickle.loads(data)
                
                else:
                
                    hasCar = pickle.loads(data,encoding='bytes')
                
                final = dict()
                final.update(hasCar)
                car_type = {}
                final_message += " Number of cars {0} \n".format(final['no_cars'])
                
                if query == "query3":
                
                    final_message += " Colour:  {0} \n".format(final['colours_detected'])
            
            if query in ["query2","query3"]:
            
                if 'has_car' in hasCar and hasCar['has_car']:
            
                    print("car Found... Sending to Clf")
                    s1 = socket.socket(socket.AF_INET,   socket.SOCK_STREAM)
                    s1.connect((host, port))
                    serialized_data = pickle.dumps(img, protocol=2)
                    s1.sendall(serialized_data)
                    s1.shutdown(socket.SHUT_WR)
                    block = s1.recv(4096)
                    s1.close()
                    
                    if sys.version_info.major < 3:
            
                        car_type = pickle.loads(block)
            
                    else:
            
                        car_type = pickle.loads(block,encoding='bytes')
            
                    final_message += "Type of car {0}".format(car_type['car_type'])
                
                    print("Sending the data to consumer")
                else:
                    car_type['car_type'] = ""
                    car_type['car_type_time'] = ""
                    final_message += "No cars in the frame"

            final['frame'] = idx
            
            final.update(car_type)
            final.pop('has_car')
            sender.send_message(pickle.dumps(final,protocol=2))
            idx = idx + 1
            y0, dy = 20, 15

            for i, line in enumerate(final_message.split('\n')):

                y = y0 + i * dy
                cv2.putText(_frame, text=line, org=(10, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.50, color=(0, 0, 255), thickness=2)

            print("Writing frames to output video file")
            out_video_obj.write(_frame)
            time.sleep(1/30)
        else:
            break
    out_video_obj.release()
        
   

video_reader("video.mp4")
end = datetime.now()
exec_time = (end - start).total_seconds()

print("Total time taken for execution", exec_time)