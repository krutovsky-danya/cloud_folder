import socket, time
from PyQt5.QtCore import (QThread,
                          pyqtSignal)
from PyQt5.QtWidgets import QFileDialog

class ThreadForDownloading(QThread):

    progress_signal = pyqtSignal(list) #По какой-то причине у сигналов такой синтаксис

    def __init__(self, ID, text):
        super().__init__()
        self.ID = ID
        self.text = text
        self.percent = 0

    def run(self):
        self.host = 'localhost'
        self.port = 60000

        self.client = socket.socket()
        self.client.connect((self.host, self.port))
        connecion = self.client.recv(1024)
        self.client.send(self.ID.encode())
        size = self.client.recv(1024)
        self.client.send("Launch".encode())
        path = QFileDialog.getExistingDirectory(self, "Open a folder",
                                                '//home', QFileDialog.ShowDirsOnly)
        file = open(path + self.text, 'wb')
        l = self.client.recv(1024)
        downloaded = 0
        while self.percent != 100:
            if len(l) < 1024:
                self.percent = 100
                break
            self.percent = downloaded / size
            self.progress_signal.emit([self.ID, self.percent]) #Отправляем обратно пару ID - процент
            file.write(l)
            downloaded += len(l)
            l = self.client.recv(1024)
        file.write(l)
        file.close()
        self.client.send('Sucsess'.encode())
