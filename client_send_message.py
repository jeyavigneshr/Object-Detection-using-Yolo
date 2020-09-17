import socket

'''
Base class to emulate producer consumer 
'''
class MessageSender():
    
    #Initialization variables
    def __init__(self, host="localhost",port=7777):
        self.port = port
        self.host = host

    #Method to send data to the cosumer
    def send_message(self , message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.send(message.encode())
        sock.close()
