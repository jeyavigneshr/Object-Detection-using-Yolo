import socket

class MessageSender():
    def __init__(self, host="localhost",port=7000):
        self.host = host
        self.port = port

    def send_message(self , message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.sendall(message)
        sock.close()


