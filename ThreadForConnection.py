import socket, time
from PyQt5.QtCore import (QThread,
                          pyqtSignal)

class ThreadForConnection(QThread):

    signal = pyqtSignal(list)

    def __init__(self, type = None, host = None, port = None, client = None):
        super().__init__()
        self.type = type
        self.host = host
        self.port = port
        self.client = client
        self.connectionStatus = False

    def run(self):
        time.sleep(3)
        if self.type == 1:
            self.client = socket.socket()
            while self.connectionStatus == False:
                try:
                    self.client.connect((self.host, self.port))
                    self.connectionStatus = True
                except ConnectionRefusedError:
                    time.sleep(1)
            self.signal.emit([1, self.client])

        else:
            self.client.send("Ready".encode())
            file = open('Data//' + 'FoldersDataFromServer.csv', 'wb')
            l = self.client.recv(1024)
            while (l):
                if len(l) < 1024:
                    break
                file.write(l)
                l = self.client.recv(1024)
            file.write(l)
            file.close()

            self.client.send("Ready".encode())

            file = open('Data//' + 'FilesDataFromServer.csv', 'wb')
            l = self.client.recv(1024)
            while (l):
                if len(l) < 1024:
                    break
                file.write(l)
                l = self.client.recv(1024)

            file.write(l)
            file.close()

            self.signal.emit([2])
