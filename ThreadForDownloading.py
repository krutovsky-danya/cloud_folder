import time
from PyQt5.QtCore import (QThread,
                          pyqtSignal)

class ThreadForDownloading(QThread):

    progress_signal = pyqtSignal(list) #По какой-то причине у сигналов такой синтаксис

    def __init__(self, ID):
        super().__init__()
        self.ID = ID
        self.percent = 0

    def run(self):
        while self.percent != 100:
            self.percent += 1
            self.progress_signal.emit([self.ID, self.percent]) #Отправляем обратно пару ID - процент
            time.sleep(1/5)
