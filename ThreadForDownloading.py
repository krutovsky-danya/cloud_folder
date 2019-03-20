import socket
from PyQt5.QtCore import (QThread,
                          pyqtSignal)

class ThreadForDownloading(QThread):

    progress_signal = pyqtSignal(list) #По какой-то причине у сигналов такой синтаксис

    def __init__(self, ID, text, host, port, path):
        super().__init__()
        self.ID = ID
        self.text = text
        self.percent = 0
        self.host = host
        self.port = port
        self.path = path

    def run(self):
        client = socket.socket()
        client.connect((self.host, self.port))
        client.send("Download".encode())
        client.recv(1024).decode()
        client.send(str(self.ID).encode())
        size = client.recv(1024).decode()
        client.send("Ready".encode())
        file = open(self.path + '/' + self.text, 'wb')
        downloaded = 0
        l = client.recv(1024)
        downloaded += len(l)
        while downloaded < int(size):#Отправляем обратно пару ID - процент
            file.write(l)
            self.percent = downloaded / int(size) * 100
            self.progress_signal.emit([self.ID, self.percent])
            l = client.recv(1024)
            downloaded += len(l)
        file.write(l)
        file.close()
        self.percent = downloaded / int(size) * 100
        self.progress_signal.emit([self.ID, self.percent])
        client.send('Ready'.encode())
        client.close()
