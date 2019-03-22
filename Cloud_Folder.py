# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:20:42 2019

@author: Даня
"""

import csv, os
from PyQt5.QtGui import (QPixmap,
                         QIcon)
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QHBoxLayout,
                             QTreeWidget,
                             QTreeWidgetItem,
                             QWidget,
                             QListWidget,
                             QListWidgetItem,
                             QProgressBar,
                             QFileDialog)


from Folder import Folder
from QCustomWidget import QCustomQWidget
from ThreadForDownloading import ThreadForDownloading
from ThreadForUploading import ThreadForUploading

STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: orangered;
    width: 10px;
    margin: 0.5px;
}
"""

class Cloud_Folder(QWidget):
    def __init__(self):
        super().__init__()

        self.ListOfDowloads = {} #Костыли
        self.ListOfDownloadThreads = []
        self.CopyOfBars = {}
        self.createWindowForProgBars()


        self.ListOfUploads = {}
        self.listOfUploadThreads = []
        self.createWindowForUploadings()


        self.user_id = 0 #А вообще это загружается при логине
        self.FoldersDataFromServer = []
        with open('Data//FoldersDataFromServer.csv', newline='') as csvfile:
            fresh = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in fresh:
                name, self_id, parent_id = row
                if parent_id == '':
                    parent_id = None
                else:
                    parent_id = int(parent_id)
                self.FoldersDataFromServer.append([name, int(self_id), parent_id])

        self.FilesDataFromServer = {}
        with open('Data//FilesDataFromServer.csv', newline='') as csvfile:
            fresh = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in fresh:
                data = row[1][1:-1]
                a = data.split('), (')
                for i in range(len(a)):
                    if len(a[i]) > 0:
                        if a[i][0] == '(':
                            a[i] = a[i][1:]
                        if a[i][-1] == ')':
                            a[i] = a[i][:-1]
                        n = a[i].rfind(' ')
                        x = a[i][:n - 1]
                        y = a[i][n + 1:]
                        a[i] = (x[1:-1] , int(y))
                    else:
                        a = []

                self.FilesDataFromServer[row[0]] = a

        self.ListOfUserFolders = {}
        for name, id, parent_id in self.FoldersDataFromServer:
            newFolder = Folder(name = name, id = id)
            if parent_id != None:
                self.ListOfUserFolders[parent_id].addFolder(id)
            self.ListOfUserFolders[id] = newFolder

        self.ListOfServerFolders = {}
        for name, id, parent_id in [['Server', 0, None]]:
            newFolder = Folder(name = name, id = id)
            if parent_id != None:
                self.ListOfServerFolders[parent_id].addFolder(id)
            self.ListOfServerFolders[id] = newFolder

        self.max_idOfFiles = -1

        for parent in self.FilesDataFromServer:
            for file, id in self.FilesDataFromServer[parent]:
                if id > self.max_idOfFiles:
                    self.max_idOfFiles = id
                self.ListOfUserFolders[int(parent)].addFile((file, id))

        self.pathToFolders = {}

        self.createUserSide()
        self.WindowForUserFolders = QListWidget()

        self.WindowForServerFolders = QListWidget()
        self.createServerSide()

        layout = QHBoxLayout()
        layout.addWidget(self.UserTree)
        layout.addWidget(self.WindowForUserFolders)
        layout.addWidget(self.WindowForServerFolders)
        layout.addWidget(self.ServerTree)

        self.setLayout(layout)

    def createUserSide(self):
        self.UserTree = QTreeWidget()
        self.UserTree.header().setVisible(False)
        self.createTree(parent = self.UserTree, obj = self.ListOfUserFolders[self.user_id])
        self.UserTree.itemSelectionChanged.connect(self.updateWindow)

    def createServerSide(self):
        self.ServerTree = QTreeWidget()
        self.ServerTree.header().setVisible(False)
        self.createTree(parent = self.ServerTree, obj = self.ListOfServerFolders[0])
        self.ServerTree.itemSelectionChanged.connect(self.updateServerWindow)

    def createTree(self, parent = None, obj = None):
        newFolder = QTreeWidgetItem(parent, [obj.getName()])
        newFolder.setIcon(0, QIcon(QPixmap('Icons//Folder.png')))
        obj.setPath(newFolder)
        self.pathToFolders[str(newFolder)] = obj
        for folder in obj.folders:
            self.createTree(parent = newFolder, obj = self.ListOfUserFolders[folder])

    def updateWindow(self):
        self.WindowForUserFolders.clear()
        self.CopyOfBars.clear()
        for index in self.pathToFolders[str(self.UserTree.currentItem())].folders:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(self.ListOfUserFolders[index].getName())
            myQCustomQWidget.setType("Folder")
            myQCustomQWidget.setObject(self.ListOfUserFolders[index].path)
            myQCustomQWidget.setID(index)
            myQListWidgetItem = QListWidgetItem(self.WindowForUserFolders)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.WindowForUserFolders.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            myQListWidgetItem.setIcon(QIcon(QPixmap('Icons//Folder.png')))

        for text, id in self.pathToFolders[str(self.UserTree.currentItem())].files:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(text)
            myQCustomQWidget.setID(id)
            if id in self.ListOfUploads:
                newbar = QProgressBar()
                self.CopyOfBars[id] = newbar
                myQCustomQWidget.setBar(newbar)
                myQCustomQWidget.setType("UploadingFile")
            else:
                myQCustomQWidget.setType("File")
                if id in self.ListOfDowloads:
                    newbar = QProgressBar()
                    self.CopyOfBars[id] = newbar
                    myQCustomQWidget.setBar(newbar)
            myQListWidgetItem = QListWidgetItem(self.WindowForUserFolders)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.WindowForUserFolders.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            myQListWidgetItem.setIcon(QIcon(QPixmap('Icons//File.png')))
        self.WindowForUserFolders.itemClicked.connect(self.item_clicked)
        self.WindowForUserFolders.itemDoubleClicked.connect(self.item_double_clicked)
        #Весь этот костыль с дубликатами баров нужен, потому что я не могу дублировать один и тот же бар в оба окна.
        #Более того, если я сначала привязал бар к элементу листа, а потом удалил этот элемент,
        #обновив лист, тот питон ловит ошибку, что-то свзянное с удалением родителя/контролем мусора,
        #было лень до конца разбираться. Так что такой способ, где программа явно удаляет все бары до удаления их родителей

    def updateServerWindow(self):
        self.WindowForServerFolders.clear()
        for text, id in [('B.jpg', 0),
                         ('E.jpg', 0),
                         ('S.jpg', 0),
                         ('T.jpg', 0),
                         ('G.jpg', 0),
                         ('I.jpg', 0),
                         ('R.jpg', 0),
                         ('L.jpg', 0)]:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(text)
            myQCustomQWidget.setID(id)
            myQCustomQWidget.setType("File")

            myQListWidgetItem = QListWidgetItem(self.WindowForServerFolders)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.WindowForServerFolders.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            myQListWidgetItem.setIcon(QIcon(QPixmap('Icons//File.png')))
        self.WindowForServerFolders.itemClicked.connect(self.serverItemClicked)
        self.WindowForServerFolders.itemDoubleClicked.connect(self.serverItemDoubleClicked)

    def item_clicked(self, item):
        file = self.WindowForUserFolders.itemWidget(item)
        self.ID = file.getID()
        self.obj = file.getObject()
        self.type = file.getType()
        self.text = file.getText()

    def serverItemClicked(self, item):
        file = self.WindowForServerFolders.itemWidget(item)
        self.S_ID = file.getID()
        self.S_obj = file.getObject()
        self.S_type = file.getType()
        self.S_text = file.getText()

    def item_double_clicked(self, item):
        if self.type == "Folder":
            self.UserTree.setCurrentItem(self.obj)

    def serverItemDoubleClicked(self, item):
        if self.S_type == "Folder":
            self.ServerTree.setCurrentItem(self.S_obj)

    def createWindowForProgBars(self):
        self.WindowForProgBars = QWidget()
        self.ListWithProgBars = QListWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.ListWithProgBars)
        self.WindowForProgBars.setLayout(layout)
        myQCustomQWidget = QCustomQWidget()
        myQCustomQWidget.setAnim('Icons//topLoading.gif')
        myQListWidgetItem = QListWidgetItem(self.ListWithProgBars)
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
        self.ListWithProgBars.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.WindowForProgBars.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool) #Убирает рамку и заголовок, окно не отображается в панели задач
        self.WindowForProgBars.setFixedSize(375, 170)

    def startNewDownloading(self, host, port):
        if ((len(self.WindowForUserFolders.selectedItems())) != 0
            and self.ID != None and self.ID not in self.ListOfDowloads
            and self.type == "File"):
            newbar = QProgressBar()
            newbar.setStyleSheet(STYLE)
            self.ListOfDowloads[self.ID] = [self.text, newbar]
            self.updateWindowForProgBars()
            self.updateWindow()
            path = QFileDialog.getExistingDirectory(self, "Open a folder",
                                                    '//home', QFileDialog.ShowDirsOnly)
            newthread = ThreadForDownloading(self.ID, self.text, host, port, path)
            newthread.progress_signal.connect(self.updateValuesOfProgBars)
            self.ListOfDownloadThreads.append(newthread)
            newthread.start() #Создали поток для нового бара, запихнули его в словарь, обновили главный лист и всплывающее окно

    #Тут вроде все понятно
    def updateWindowForProgBars(self):
        self.ListWithProgBars.clear()
        for ID in self.ListOfDowloads:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(self.ListOfDowloads[ID][0])
            myQCustomQWidget.setBar(self.ListOfDowloads[ID][1])
            myQCustomQWidget.setHeight()
            myQListWidgetItem = QListWidgetItem(self.ListWithProgBars)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.ListWithProgBars.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            myQListWidgetItem.setIcon(QIcon(QPixmap('Icons//File.png')))
        self.WindowForProgBars.setFixedHeight(70 * len(self.ListOfDowloads))

    def updateValuesOfProgBars(self, data):#Получаем из потока данные для бара
        ID, percent = data
        self.ListOfDowloads[ID][1].setValue(percent)
        if ID in self.CopyOfBars:
            self.CopyOfBars[ID].setValue(percent)
        if percent == 100:
            del self.ListOfDowloads[ID]
            self.updateWindowForProgBars()
            self.updateWindow()

    def createWindowForUploadings(self):
        self.WindowForUploadings = QWidget()
        self.ListForUploadings = QListWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.ListForUploadings)
        self.WindowForUploadings.setLayout(layout)
        myQCustomQWidget = QCustomQWidget()
        myQCustomQWidget.setAnim('Icons//pikachu.gif')
        myQListWidgetItem = QListWidgetItem(self.ListForUploadings)
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
        self.ListForUploadings.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.WindowForUploadings.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool) #Убирает рамку и заголовок, окно не отображается в панели задач
        self.WindowForUploadings.setFixedSize(375, 260)

    def startNewUploading(self, path, host, port):
        name = path[path.rfind('/') + 1:]
        self.ListOfUserFolders[self.pathToFolders[str(self.UserTree.currentItem())].id].files.append((name, self.max_idOfFiles + 1))
        newbar = QProgressBar()
        self.ListOfUploads[self.max_idOfFiles + 1] = [name, newbar]
        self.updateWindowForUploadings()
        self.updateWindow()
        newthread = ThreadForUploading(name, self.max_idOfFiles + 1, self.pathToFolders[str(self.UserTree.currentItem())].id, path, host, port)
        newthread.signal.connect(self.updateValueForUploadingBars)
        self.listOfUploadThreads.append(newthread)
        self.max_idOfFiles += 1
        newthread.start()

    def updateWindowForUploadings(self):
        self.ListForUploadings.clear()
        for ID in self.ListOfUploads:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(self.ListOfUploads[ID][0])
            myQCustomQWidget.setBar(self.ListOfUploads[ID][1])
            myQCustomQWidget.setHeight()
            myQListWidgetItem = QListWidgetItem(self.ListForUploadings)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.ListForUploadings.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            myQListWidgetItem.setIcon(QIcon(QPixmap('Icons//File.png')))
        self.WindowForUploadings.setFixedHeight(70 * len(self.ListOfUploads))

    def updateValueForUploadingBars(self, data):
        ID, percent = data
        if percent == "Finish":
            del self.ListOfUploads[ID]
            self.updateWindow()
            self.updateWindowForUploadings()
        else:
            self.ListOfUploads[ID][1].setValue(percent)
            if ID in self.CopyOfBars:
                self.CopyOfBars[ID].setValue(percent)

    def newFolder(self, name):
        id = max(self.ListOfUserFolders) + 1
        parent_id = self.pathToFolders[str(self.UserTree.currentItem())].id
        newFolder = Folder(name = name, id = id)
        self.ListOfUserFolders[parent_id].addFolder(id)
        self.ListOfUserFolders[id] = newFolder
        parent = self.UserTree.currentItem()

        path = QTreeWidgetItem(parent, [name])
        path.setIcon(0, QIcon(QPixmap('Icons//Folder.png')))
        newFolder.setPath(path)
        self.pathToFolders[str(path)] = newFolder
        self.updateWindow()

    def changeName(self, name, type):
        if type == "File":
            files = []
            for text, id in self.pathToFolders[str(self.UserTree.currentItem())].files:
                if text == self.text:
                     text = name + self.text[self.text.rfind('.'):]
                files.append((text, id))
            self.pathToFolders[str(self.UserTree.currentItem())].files = files
            self.updateWindow()
        else:
            if len(self.WindowForUserFolders.selectedItems()) != 0:
                self.ListOfUserFolders[self.ID].changeName(name)
                self.ListOfUserFolders[self.ID].path.setText(0, name)
                self.updateWindow()
            else:
                self.pathToFolders[str(self.UserTree.currentItem())].changeName(name)
                self.pathToFolders[str(self.UserTree.currentItem())].path.setText(0, name)
