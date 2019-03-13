# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:20:42 2019

@author: Даня
"""

import csv
from PyQt5.QtGui import (QPixmap,
                         QIcon)
from PyQt5.QtCore import (Qt,
                          pyqtSignal)
from PyQt5.QtWidgets import (QHBoxLayout,
                             QTreeWidget,
                             QTreeWidgetItem,
                             QWidget,
                             QListWidget,
                             QListWidgetItem,
                             QProgressBar)


from Folder import Folder
from QCustomWidget import QCustomQWidget
from ThreadForDownloading import ThreadForDownloading

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

        self.user_id = 0 #А вообще это загружается при логине
        self.FoldersDataFromServer = []
        with open('FoldersDataFromServer.csv', newline='') as csvfile:
            fresh = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in fresh:
                name, self_id, parent_id = row
                if parent_id == '':
                    parent_id = None
                else:
                    parent_id = int(parent_id)
                self.FoldersDataFromServer.append([name, int(self_id), parent_id])

        self.FilesDataFromServer = {}
        with open('FilesDataFromServer.csv', newline='') as csvfile:
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

        for parent in self.FilesDataFromServer:
            for file, id in self.FilesDataFromServer[parent]:
                self.ListOfUserFolders[int(parent)].addFile((file, id))

        self.pathToFolders = {}

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
        self.createTree(parent = self.UserTree, obj = self.ListOfUserFolders[self.user_id])
        self.UserTree.itemSelectionChanged.connect(self.updateWindow)

    def createTree(self, parent = None, obj = None):
        newFolder = QTreeWidgetItem(parent, [obj.getName()])
        newFolder.setIcon(0, QIcon(QPixmap('Icons//Folder.png')))
        obj.setPath(newFolder)
        self.pathToFolders[str(newFolder)] = obj
        for folder in obj.folders:
            self.createTree(parent = newFolder, obj = self.ListOfUserFolders[folder])

    def createUserFolder(self):
        self.WindowForUserFolders = QListWidget()

    def updateWindow(self):
        self.WindowForUserFolders.clear()
        self.CopyOfBars.clear()
        for index in self.pathToFolders[str(self.UserTree.currentItem())].folders:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(self.ListOfUserFolders[index].getName())
            myQCustomQWidget.setType("Folder")
            myQCustomQWidget.setObject(self.ListOfUserFolders[index].path)
            myQListWidgetItem = QListWidgetItem(self.WindowForUserFolders)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.WindowForUserFolders.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            myQListWidgetItem.setIcon(QIcon(QPixmap('Icons//Folder.png')))

        for text, id in self.pathToFolders[str(self.UserTree.currentItem())].files:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(text)
            myQCustomQWidget.setID(id)
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

    def item_clicked(self, item):
        file = self.WindowForUserFolders.itemWidget(item)
        self.ID = file.getID()
        self.obj = file.getObject()
        self.type = file.getType()
        self.text = file.getText()

    def item_double_clicked(self, item):
        if self.type == "Folder":
            self.UserTree.setCurrentItem(self.obj)

    def createWindowForProgBars(self):
        self.WindowForProgBars = QWidget()
        self.ListWithProgBars = QListWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.ListWithProgBars)
        self.WindowForProgBars.setLayout(layout)
        myQCustomQWidget = QCustomQWidget()
        myQCustomQWidget.setAnim('Icons//loading.gif')
        myQListWidgetItem = QListWidgetItem(self.ListWithProgBars)
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
        self.ListWithProgBars.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.WindowForProgBars.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool) #Убирает рамку и заголовок, окно не отображается в панели задач
        self.WindowForProgBars.setFixedSize(300, 450)

    def startNewDownloading(self):
        if ((len(self.WindowForUserFolders.selectedItems())) != 0
            and self.ID != None and self.ID not in self.ListOfDowloads):
            newbar = QProgressBar()
            newbar.setStyleSheet(STYLE)
            self.ListOfDowloads[self.ID] = [self.text, newbar]
            self.updateWindowForProgBars()
            self.updateWindow()
            newthread = ThreadForDownloading(self.ID)
            newthread.progress_signal.connect(self.updateValuesOfProgBars)
            self.ListOfDownloadThreads.append(newthread)
            self.WindowForProgBars.setFixedHeight(60 * len(self.ListOfDowloads))
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

    def updateValuesOfProgBars(self, data):#Получаем из потока данные для бара
        ID, percent = data
        self.ListOfDowloads[ID][1].setValue(percent)
        if ID in self.CopyOfBars:
            self.CopyOfBars[ID].setValue(percent)
        if percent == 100:
            del self.ListOfDowloads[ID]
            self.updateWindowForProgBars()
            self.updateWindow()
            self.WindowForProgBars.setFixedHeight(70 * len(self.ListOfDowloads))
