# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:20:42 2019

@author: Даня
"""

import csv
from PyQt5.QtGui import (QPixmap,
                         QIcon)
from PyQt5.QtWidgets import (QHBoxLayout,
                             QTreeWidget,
                             QTreeWidgetItem,
                             QWidget,
                             QListWidget,
                             QListWidgetItem)

from Folder import Folder
from QCustomWidget import QCustomQWidget


class Cloud_Folder(QWidget):
    def __init__(self):
        super().__init__()
        
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
            myQListWidgetItem = QListWidgetItem(self.WindowForUserFolders)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.WindowForUserFolders.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            myQListWidgetItem.setIcon(QIcon(QPixmap('Icons//File.png')))
        self.WindowForUserFolders.itemClicked.connect(self.item_clicked)
        self.WindowForUserFolders.itemDoubleClicked.connect(self.item_double_clicked)

    def item_clicked(self, item):
        file = self.WindowForUserFolders.itemWidget(item)
        self.ID = file.getID()
        self.obj = file.getObject()
        self.type = file.getType()

    def item_double_clicked(self, item):
        if self.type == "Folder":
            self.UserTree.setCurrentItem(self.obj)
