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

class Obj():
    def __init__(self, name=None, kind=None):
        self.name = name
        self.kind = kind
    
    def changeName(self, name):
        self.name = name
    
    def info(self):
        return self.name
    
    def getKind(self):
        return self.kind

class File(Obj):
    def _init__(self, name=None, path=None):
        super().__init__(name=name, kind='File')
        self.path = path

class Folder(Obj):
    def __init__(self, name=None, f_id=None, parent=None):
        super().__init__(name=name, kind='Folder')
        self.id = f_id
        self.parent = parent
        self.folders = []
        self.files = []
    
    def addFile(self, file):
        self.files.append(file)
        
    def addFolder(self, folder):
        self.folders.append(folder)
    
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
        self.txt = text
        self.textDownQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath))
    
    def num(self):
        return self.txt

class Cloud_Folder(QWidget):
    def __init__(self, parent=None):
        super(Cloud_Folder, self).__init__(parent)

        self.home = Folder(name='Danya', f_id=0)
        for i in ["HomeWork_OfCourse.", "Pictures.", "Documents."]:
            file = File(name=i)
            self.home.addFile(file)
        
        self.createTree()
        self.createLists()
        self.createInventory()
        self.createServer()
        
        names = ["Server", "Nikita", "Vlad", "Homework 4Tb"]
        files = ["ReadMe.txt","Do Not Touch.file", "Do Not Touch Me.file", 
                 "Homework 4Tb"]
        self.folders = []
        for i in names:
            self.folders.append(Folder(name=i, f_id=len(self.folders),
                                       parent=self.Server))
            self.folders[len(self.folders) - 1].addFile(File(name=files[len(self.folders) - 1]))
        
        for i in self.folders:
            self.createLay(home=self.Server, obj=i)
        
        layout = QHBoxLayout()
        #layout.addWidget(QLabel("Path[S:Dnaya//"), 0, 0, 1, 3)
        layout.addWidget(self.Tree)
        layout.addLayout(self.Inventory)
        layout.addWidget(self.Server)

        self.setLayout(layout)

        self.setWindowTitle("Cloud Folder")
        self.setWindowIcon(QIcon(QPixmap('Icons//mega.jpg')))
        self.setGeometry(100, 100, 900, 250)

    def createTree(self):
        self.Tree = QTreeWidget()
        self.Tree.header().setVisible(False)
        self.createLay(home=self.Tree, obj=self.home)

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

    def createLay(self, home=None, obj=None):
        a = QTreeWidgetItem(home, [obj.info()])
        if obj.getKind() == 'Folder':
            a.setIcon(0, QIcon(QPixmap('Icons//folder.png')))
            for i in obj.folders:
                self.createLay(home=a, obj=i)
            for i in obj.files:
                self.createLay(home=a, obj=i)
        else:
            a.setIcon(0, QIcon(QPixmap('Icons//file.png')))



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    win = Shell()
    win.show()
    sys.exit(app.exec_())
