# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 19:27:10 2019
@author: Даня
"""
#from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication,
                             #QDialog,
                             #QGridLayout,
                             QLabel,
                             QHBoxLayout,
                             #QVBoxLayout,
                             #QPushButton,
                             #QTabWidget,
                             QTreeWidget,
                             QTreeWidgetItem,
                             QWidget,
                             QMainWindow,
                             #QFileDialog,
                             QAction,
                             QListWidget,
                             QListWidgetItem,
                             QTreeWidgetItemIterator)

class Folder():
    def __init__(self, name = None, id = None, parent_id = None):
        self.name = name
        self.id = id
        self.parent_id = parent_id
        self.folders = []
        self.files = []
        self.parent = None

    def changeName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def addFile(self, file):
        self.files.append(file)

    def addFolder(self, folder):
        self.folders.append(folder)
    
    def setParent(self, item):
        self.parent = item

class Shell(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_widget = Cloud_Folder()
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Cloud Folder")
        self.setWindowIcon(QIcon(QPixmap('Icons//mega.jpg')))
        self.setGeometry(300, 300, 600, 300)

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
        if len(self.main_widget.WindowForUserFolders.selectedItems()) != 0:
            print(self.main_widget.PathToFile)

    def Upload(self):
        print("Upload")

    def Delete(self):
        print("Delete")

    def Find_someone(self):
        print("Find_someone")

class QCustomQWidget (QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.textLabel = QLabel()
        self.layout.addWidget(self.textLabel)
        self.setLayout(self.layout)
        self.obj = None
        
    def setText(self, text):
        self.text = text
        self.textLabel.setText(text)
    
    def setObject(self, obj):
        self.obj = obj
    
    def getText(self):
        return self.text

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type
    
    def getObject(self):
        return self.obj

class Cloud_Folder(QWidget):
    def __init__(self):
        super().__init__()

        self.user_name = "Danya"
        #                               Name, id, parent_id
        self.FoldersDataFromServer = [["Danya", 0, None],
                                      ["Downloads", 1, 0],
                                      ["Desktop", 2, 0],
                                      ["Homeworks", 3, 0],
                                      ["Downloads", 4, 1],
                                      ["Drivers", 5, 1],
                                      ["Python", 6, 2],
                                      ["Trash", 7, 2],
                                      ["Economics", 8, 3],
                                      ["Under13", 9, 3]]

        self.FilesDataFromServer = {'0': [],
                                    '1': ["It's.txt", "Hard.pdf"],
                                    '2': ["To.jpg", "Think up.docx"],
                                    '3': ["File.pptx", "Names.mp3"],
                                    '4': ["We choose to go.txt", "To the Moon in this.txt"],
                                    '5': ["Decade and do the.txt", "Other things, not.txt"],
                                    '6': ["Because they are.txt", "Easy, but because.txt"],
                                    '7': ["They are hard.txt", "Because that goal.txt"],
                                    '8': ["Will serve to.txt", "Organize and measure.txt"],
                                    '9': ["The best of our.txt", "Energies and skills.txt"]}
        
        self.ListOfUserFolders = {}
        for name, id, parent_id in self.FoldersDataFromServer:
            newFolder = Folder(name = name, id = id)
            if parent_id != None:
                self.ListOfUserFolders[parent_id].addFolder(id)
            self.ListOfUserFolders[id] = newFolder

        for parent in self.FilesDataFromServer:
            for file in self.FilesDataFromServer[parent]:
                self.ListOfUserFolders[int(parent)].addFile(file)
        
        self.itemToFolder = {}
        
        self.createUserSide()
        self.createUserFolder()
        
        #createServerFolders
        #createServerTree
        
        layout = QHBoxLayout()
        layout.addWidget(self.UserTree)
        layout.addWidget(self.WindowForUserFolders)
        

        self.setLayout(layout)

    def createUserSide(self):
        self.UserTree = QTreeWidget()
        self.UserTree.header().setVisible(False)
        self.createTree(parent = self.UserTree, obj = self.ListOfUserFolders[0])
        self.PathToFolder = ""
        self.UserTree.itemSelectionChanged.connect(self.FullPathToFolder)

    def createUserFolder(self):
        self.WindowForUserFolders = QListWidget()

    def updateWindow(self):
        self.WindowForUserFolders.clear()
        for index in self.ListOfUserFolders[self.FilesFromFolder()].folders:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(self.ListOfUserFolders[index].getName())
            myQCustomQWidget.setType("Folder")
            myQCustomQWidget.setObject(self.ListOfUserFolders[self.FilesFromFolder()])
            myQListWidgetItem = QListWidgetItem(self.WindowForUserFolders)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.WindowForUserFolders.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            myQListWidgetItem.setIcon(QIcon(QPixmap('Icons//Folder.png')))

        for text in self.ListOfUserFolders[self.FilesFromFolder()].files:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(text)
            myQCustomQWidget.setType("File")
            
            myQListWidgetItem = QListWidgetItem(self.WindowForUserFolders)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.WindowForUserFolders.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            myQListWidgetItem.setIcon(QIcon(QPixmap('Icons//File.png')))
        self.WindowForUserFolders.itemClicked.connect(self.item_clicked)
        self.WindowForUserFolders.itemDoubleClicked.connect(self.item_double_clicked)

    def item_clicked(self, item):
        file = self.WindowForUserFolders.itemWidget(item)
        self.PathToFile = self.PathToFolder +  file.getText()
        self.type = file.getType()

    def item_double_clicked(self, item):
        if self.type == "Folder":
            folder = self.getObject
            self.UserTree.setCurrentItem(folder.parent)

    def createTree(self, parent = None, obj = None):
        newFolder = QTreeWidgetItem(parent, [obj.getName()])
        newFolder.setIcon(0, QIcon(QPixmap('Icons//Folder.png')))
        obj.setParent(newFolder)
        self.itemToFolder[str(newFolder)] = obj
        for folder in obj.folders:
            self.createTree(parent = newFolder, obj = self.ListOfUserFolders[folder])

    def FullPathToFolder(self):
        self.PathToFolder = ""
        item = self.UserTree.currentItem()
        text = item.text(0)
        while text != self.user_name:
            self.PathToFolder = text + "//" + self.PathToFolder
            item = item.parent()
            text = item.text(0)
        self.PathToFolder = text + "//" + self.PathToFolder
        self.updateWindow()

    def FilesFromFolder(self):
        index = 0
        localpath = self.PathToFolder[self.PathToFolder.find("//") + 2:]
        while len(localpath) != 0:
            for folder in self.ListOfUserFolders[index].folders:
                if self.ListOfUserFolders[folder].getName() == localpath[0:localpath.find("//")]:
                    index = folder
                    localpath = localpath[localpath.find("//") + 2:]
                    break
        return index

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    win = Shell()
    win.show()
sys.exit(app.exec_())