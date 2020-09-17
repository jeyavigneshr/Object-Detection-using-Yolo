import socket
import csv
import sys
import pickle
from datetime import datetime


sock = socket.socket()
print("Establishing the connection")
sock.bind((b'',7000))
sock.listen(5)

response = list()
try :
    
    while True:
        conn, addr = sock.accept()
        out_msg = list()
        while True:
            stream_data = conn.recv(4096)
            if not stream_data: break
            out_msg.append(stream_data)
        conn.close()
        final = dict()
        out_msg = b"".join(out_msg)
        if sys.version_info.major < 3:
            final = pickle.loads(out_msg)
        else:
            final = pickle.loads(out_msg,encoding='bytes')
        response.append(final)
        if len(list(filter(None,response))) >= 1495:
            break
except KeyboardInterrupt:
    print("Exiting")
response = list(filter(None,response))
if len(sys.argv) >1 :
    out_file = sys.argv[1]
else:
    out_file = "../TestingResults/response.csv"
if len(response) > 0:
    header_details = ["no_cars","frame","no_cars_time","colours_detected","colours_detected_time","car_type","car_type_time"]
    with open(out_file , "w") as w:
        writer = csv.DictWriter(w,fieldnames=header_details)
        writer.writeheader()
        for row in response:
            for h in header_details:
                if h not in row:
                    row[h] = None
            if 'no_cars' not in row:
                row['no_cars'] = 0
            if 'car_type'  in row:
                if row['no_cars'] == '0' or row['no_cars'] == 0:
                    row['car_type'] = None
            writer.writerow(row)
    