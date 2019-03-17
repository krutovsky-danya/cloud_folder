import socket, time
from PyQt5.QtCore import (QThread,
                          pyqtSignal)

class ThreadForUploading(QThread):

    signal = pyqtSignal(list)

    def __init__(self, name, id, parent_id, path, host, port):
        super().__init__()
        self.name = name
        self.id = id
        self.parent_id = parent_id
        self.path = path
        self.host = host
        self.port = port

    def run(self):
        client = socket.socket()
        client.connect((self.host, self.port))
        client.send("Uploading".encode())
        client.recv(1024).decode()
        client.send(self.name.encode())
        client.recv(1024).decode()
        client.send(str(self.id).encode())
        client.recv(1024).decode()
        client.send(str(self.parent_id).encode())
        client.recv(1024).decode()
        file = open(self.path, 'rb')
        l = file.read(1024)
        while (l):
            client.send(l)
            l = file.read(1024)
        file.close()
        client.recv(1024).decode()
        client.close()
        self.signal.emit([self.name, self.parent_id, self.id])
