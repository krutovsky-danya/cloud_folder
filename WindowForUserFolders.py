import os, sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QListWidget,
                             QAbstractItemView,
                             QWidget,
                             QLabel,
                             QHBoxLayout)

class WindowForUserFolders(QListWidget):
    def __init__(self, shell, cloud_folder):
        super().__init__()
        self.setAcceptDrops(True)
        self.shell = shell
        self.cloud_folder = cloud_folder
        #self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.uploadBackground()

    def uploadBackground(self):
        self.UploadBack = QWidget()
        self.UploadBack.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.UploadBack.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.UploadBack.setStyleSheet("background: #8b9897;")
        text = QLabel("Перетащите сюда файлы\n для загрузки в облако")
        text.setAlignment(Qt.AlignCenter)
        font = QFont("Times", 20)
        text.setFont(font)
        layout = QHBoxLayout(self.UploadBack)
        layout.addWidget(text)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if len(self.cloud_folder.UserTree.selectedItems()) != 0:
                x1, y1, x2, y2 = self.geometry().getCoords()
                x12, y12, x22, y22 = self.shell.geometry().getCoords()
                self.UploadBack.setFixedSize(x2 - x1, y2 - y1)
                self.UploadBack.move(x12 + x1 + 9, y22 - y2 - 9)
                self.UploadBack.show()
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            listForUploads = []
            if len(self.cloud_folder.UserTree.selectedItems()) != 0:
                self.UploadBack.hide()
                for url in event.mimeData().urls():
                    if os.path.isfile(str(url.toLocalFile())):
                        listForUploads.append(str(url.toLocalFile()))
                self.cloud_folder.upload(paths = listForUploads)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.UploadBack.hide()
