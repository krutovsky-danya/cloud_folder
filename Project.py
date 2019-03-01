# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 19:27:10 2019

@author: Даня
"""

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication,
                             QDialog,
                             QGridLayout,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                             QPushButton,
                             QTabWidget,
                             QTreeWidget,
                             QTreeWidgetItem,
                             QWidget,
                             QMainWindow,
                             QFileDialog,
                             QAction,
                             QListWidget,
                             QListWidgetItem)

class Shell(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_widget = Cloud_Folder()
        self.setCentralWidget(self.main_widget)

        self.ToolBarElements = [['Download.png', 'Download from server', self.Download],
                                ['Upload.png','Upload to server', self.Upload],
                                ['Delete.png', 'Delete', self.Delete],
                                ['Find_someone.png', 'Find_someone', self.Find_someone]]

        self.toolbar = self.addToolBar('Commands')
        self.toolbar.setMovable(False)
        for path, text, action in self.ToolBarElements:
            newAction = QAction(QIcon('Icons//' + path), text, self)
            newAction.triggered.connect(action)
            self.toolbar.addAction(newAction)

    def Download(self):
        print("Download")

    def Upload(self):
        print("Upload")

    def Delete(self):
        print("Delete")

    def Find_someone(self):
        print("Find_someone")

class QCustomQWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel    = QLabel()
        self.textDownQLabel  = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QHBoxLayout()
        self.iconQLabel      = QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath))
    
    def num(self):
        return 666

class Cloud_Folder(QWidget):
    def __init__(self, parent=None):
        super(Cloud_Folder, self).__init__(parent)

        self.home = "Danya"
        self.folders = {"Danya" : ["HomeWork_OfCourse.", "Pictures.",
                                   "Documents."],
                        "Server" : ["ReadMe.txt"],
                        "Nickita" : ["Do Not Touch.f"],
                        "Vald" : ["Do Not Touch Me!.f"],
                        "Homework 4Tb" : ["Hmmmmm.f"]}

        self.createTree()
        self.createLists()
        self.createInventory()
        self.createServer()

        layout = QHBoxLayout()
        #layout.addWidget(QLabel("Path[S:Dnaya//"), 0, 0, 1, 3)
        layout.addWidget(self.Tree)
        layout.addLayout(self.Inventory)
        layout.addWidget(self.Server)

        self.setLayout(layout)

        self.setWindowTitle("Cloud Folder")
        #self.setWindowIcon()
        self.setGeometry(100, 100, 900, 250)

    def createTree(self):
        self.Tree = QTreeWidget()
        self.Tree.header().setVisible(False)
        self.createLay(self.Tree, self.home)

    def createInventory(self):
        self.Inventory = QVBoxLayout()
        self.Boxes = QHBoxLayout()
        self.UserBox = self.myQListWidget
        self.ServerBox = QListWidget()
        self.Boxes.addWidget(self.UserBox)
        self.Boxes.addWidget(self.ServerBox)
        self.Inventory.addLayout(self.Boxes)

    def createServer(self):
        self.Server = QTreeWidget()
        self.Server.header().setVisible(False)
        connections = ["Server", "Nickita", "Vald", "Homework 4Tb"]
        for i in connections:
            self.createLay(self.Server, i)

        #tab_2.setPixmap(QPixmap("bebop.jpg"))
    
    def createLists(self):
        self.myQListWidget = QListWidget(self)
        for index, name, icon in [
            ('No.1', 'Meyoko',  'Icons//mega-min.jpg'),
            ('No.2', 'Nyaruko', 'Icons//mega-min.jpg'),
            ('No.3', 'Louise',  'Icons//mega-min.jpg')]:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQCustomQWidget.setIcon(icon)
            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.myQListWidget.itemClicked.connect(self.item_clicked)
    
    def item_clicked(self, item):
        puk =self.myQListWidget.itemWidget(item)
        print(puk.num())

    def changeInventory(self, _name=None):
        self.Inventory = QVBoxLayout()
        if _name == None:
            _name = self.home
        for i in self.folders[_name]:
            btn = QPushButton(i)
            print(i)
            self.Inventory.addWidget(btn)

    def createLay(self, home, lay):
        a = QTreeWidgetItem(home, [lay])
        if lay.count('.') == 0:
            for i in self.folders[lay]:
                self.createLay(a, i)



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    win = Shell()
    win.show()
    sys.exit(app.exec_())
