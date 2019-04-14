# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:20:42 2019

@author: Даня
"""

import csv, os, socket
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
                             QFileDialog,
                             QSplitter,
                             QMenu,
                             QDialog,
                             QVBoxLayout,
                             QLabel,
                             QLineEdit,
                             QPushButton)


from Folder import Folder
from QCustomWidget import QCustomQWidget
from ThreadForDownloading import ThreadForDownloading
from ThreadForUploading import ThreadForUploading
from WindowForUserFolders import WindowForUserFolders

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
    def __init__(self, host, port, parent):
        super().__init__()
        self.host = host
        self.port = port
        self.parent = parent

        self.ListOfDowloads = {}
        self.ListOfDownloadThreads = []
        self.CopyOfBars = {}
        self.createWindowForProgBars()


        self.ListOfUploads = {}
        self.ListOfUploadThreads = []
        self.createWindowForUploadings()

        self.ClickInTheTree = False
        self.ClickInTheList = False

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

        self.max_idOfFiles = -1

        for parent in self.FilesDataFromServer:
            for file, id in self.FilesDataFromServer[parent]:
                if id > self.max_idOfFiles:
                    self.max_idOfFiles = id
                self.ListOfUserFolders[int(parent)].addFile((file, id))

        self.pathToFolders = {}

        self.createUserSide()
        self.WindowForUserFolders = WindowForUserFolders(shell = self.parent, cloud_folder = self)
        self.WindowForUserFolders.itemPressed.connect(self.listClickEmitted)
        self.WindowForUserFolders.setContextMenuPolicy(Qt.CustomContextMenu)
        self.WindowForUserFolders.customContextMenuRequested.connect(self.contextMenuForList)
        self.WindowForUserFolders.itemClicked.connect(self.listClickCompleted)

        layout = QHBoxLayout()
        splitter = QSplitter()
        splitter.addWidget(self.UserTree)
        splitter.addWidget(self.WindowForUserFolders)
        layout.addWidget(splitter)

        self.setLayout(layout)

    def createUserSide(self):
        self.UserTree = QTreeWidget()
        self.UserTree.header().setVisible(False)
        self.createTree(parent = self.UserTree, obj = self.ListOfUserFolders[0])
        self.UserTree.itemPressed.connect(self.treeClickEmitted)
        self.UserTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.UserTree.customContextMenuRequested.connect(self.contextMenuForTree)
        self.UserTree.itemClicked.connect(self.treeClickCompleted)
        self.UserTree.itemSelectionChanged.connect(self.updateWindow)

    def treeClickCompleted(self):
        self.ClickInTheTree = False

    def treeClickEmitted(self):
        self.ClickInTheTree = True
        self.updateWindow()

    def contextMenuForTree(self, event):
        if self.ClickInTheTree:
            self.ClickInTheTree = False
            TreeMenu = QMenu(self.UserTree)
            NewFolder = TreeMenu.addAction(QIcon("Icons//new_folder.png"), "Add new folder to this one")
            NewFolder.triggered.connect(self.newFolder)
            ChangeName = TreeMenu.addAction(QIcon("Icons//change_name.png"), "Change the name")
            ChangeName.triggered.connect(self.changeName)
            Delete = TreeMenu.addAction(QIcon("Icons//Delete.png"), "Delete")
            Delete.triggered.connect(self.delete)
            TreeMenu.exec_(self.UserTree.mapToGlobal(event))

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
        self.WindowForUserFolders.itemPressed.connect(self.item_clicked)
        self.WindowForUserFolders.itemDoubleClicked.connect(self.item_double_clicked)

    def listClickEmitted(self):
        self.ClickInTheList = True

    def listClickCompleted(self):
        self.ClickInTheList = False

    def item_clicked(self, item):
        file = self.WindowForUserFolders.itemWidget(item)
        self.ID = file.getID()
        self.obj = file.getObject()
        self.type = file.getType()
        self.text = file.getText()

    def item_double_clicked(self, item):
        if self.type == "Folder":
            self.UserTree.setCurrentItem(self.obj)

    def contextMenuForList(self, event):
        if len(self.UserTree.selectedItems()) != 0:
            if self.ClickInTheList:
                if self.type != "UploadingFile":
                    self.ClickInTheList = False
                    ListMenu = QMenu(self.WindowForUserFolders)
                    if self.type == "File":
                        Download = ListMenu.addAction(QIcon("Icons//Download.png"), "Download")
                        Download.triggered.connect(self.startNewDownloading)
                    ChangeName = ListMenu.addAction(QIcon("Icons//change_name.png"), "Change the name")
                    ChangeName.triggered.connect(self.changeName)
                    Delete = ListMenu.addAction(QIcon("Icons//Delete.png"), "Delete")
                    Delete.triggered.connect(self.delete)
                    ListMenu.exec_(self.WindowForUserFolders.mapToGlobal(event))

            else:
                ListMenu = QMenu(self.WindowForUserFolders)
                Upload = ListMenu.addAction(QIcon("Icons//Upload.png"), "Upload here")
                Upload.triggered.connect(self.upload)
                NewFolder = ListMenu.addAction(QIcon("Icons//new_folder.png"), "Add new folder here")
                NewFolder.triggered.connect(self.newFolder)
                ListMenu.exec_(self.WindowForUserFolders.mapToGlobal(event))

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

    def startNewDownloading(self):
        if self.type == "File":
            path = QFileDialog.getExistingDirectory(self, "Open a folder",
                                                    '//home', QFileDialog.ShowDirsOnly)
            if path != "":
                host = self.host
                port = self.port
                newbar = QProgressBar()
                newbar.setStyleSheet(STYLE)
                self.ListOfDowloads[self.ID] = [self.text, newbar]
                self.updateWindowForProgBars()
                self.updateWindow()

                a = os.listdir(path)
                name = self.text
                if name in a:
                    name = name[0:name.rfind(".")] + "(1)" + name[name.rfind("."):]
                while name in a:
                    name = name[0:name.rfind("(") + 1] + str(int(name[name.rfind("(") + 1:name.rfind(")")]) + 1) + name[name.rfind(")"):]
                newthread = ThreadForDownloading(self.ID, name, host, port, path)
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

    def upload(self, paths = None):
        self.UploadingPaths = []
        if paths == None or paths == False:
            self.UploadingPaths.append(QFileDialog.getOpenFileName(self, "File")[0])
        else:
            self.UploadingPaths = paths
        if self.UploadingPaths[0] != "":
            self.uploadingDialog = QDialog(self)
            self.uploadingDialog.setWindowTitle("Uploading")
            layout = QVBoxLayout()
            if len(self.UploadingPaths) == 1:
                textlabel = QLabel("Файл: " + self.UploadingPaths[0][self.UploadingPaths[0].rfind('/') + 1:])
                tasklabel = QLabel("будет загружен в папку: " + (self.UserTree.currentItem().text(0)))
            else:
                textlabel = QLabel("Файлы (" + str(len(self.UploadingPaths)) + ")" )
                tasklabel = QLabel("будут загружены в папку: " + (self.UserTree.currentItem().text(0)))
            layout.addWidget(textlabel)
            layout.addWidget(tasklabel)
            buttonLayout = QHBoxLayout()
            okButton = QPushButton("OK")
            okButton.clicked.connect(self.startNewUploading)
            buttonLayout.addWidget(okButton)
            cancelButton = QPushButton("Cancel")
            cancelButton.clicked.connect(lambda: self.uploadingDialog.close())
            buttonLayout.addWidget(cancelButton)
            layout.addLayout(buttonLayout)
            self.uploadingDialog.setLayout(layout)
            self.uploadingDialog.exec_()

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

    def startNewUploading(self):
        for path in self.UploadingPaths:
            UploadingName = path[path.rfind('/') + 1:]
            a = [self.ListOfUserFolders[i].getName() for i in self.pathToFolders[str(self.UserTree.currentItem())].folders]
            b = [text for text, id in self.pathToFolders[str(self.UserTree.currentItem())].files]
            if UploadingName in a or UploadingName in b:
                UploadingName = UploadingName[0:UploadingName.rfind(".")] + "(1)" + UploadingName[UploadingName.rfind("."):]
            while UploadingName in a or UploadingName in b:
                UploadingName = UploadingName[0:UploadingName.rfind("(") + 1] + str(int(UploadingName[UploadingName.rfind("(") + 1:UploadingName.rfind(")")]) + 1) + UploadingName[UploadingName.rfind(")"):]
            self.ListOfUserFolders[self.pathToFolders[str(self.UserTree.currentItem())].id].files.append((UploadingName, self.max_idOfFiles + 1))
            newbar = QProgressBar()
            self.ListOfUploads[self.max_idOfFiles + 1] = [UploadingName, newbar]
            self.updateWindowForUploadings()
            self.updateWindow()
            newthread = ThreadForUploading(UploadingName, self.max_idOfFiles + 1, self.pathToFolders[str(self.UserTree.currentItem())].id, path, self.host, self.port)
            newthread.signal.connect(self.updateValueForUploadingBars)
            self.ListOfUploadThreads.append(newthread)
            self.max_idOfFiles += 1
            newthread.start()
        self.uploadingDialog.close()

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

    def newFolder(self):
        if len(self.UserTree.selectedItems()) != 0:
            self.NewFolderDialog = QDialog(self)
            self.NewFolderDialog.setWindowTitle("New folder")
            layout = QVBoxLayout()
            textlabel = QLabel("Новая папка будет создана в: " + (self.UserTree.currentItem().text(0)))
            layout.addWidget(textlabel)
            tasklabel = QLabel("Введите название:")
            layout.addWidget(tasklabel)
            self.NewFolderName = QLineEdit()
            layout.addWidget(self.NewFolderName)
            self.NewFolderInError = QLabel("Недопустимое название папки")
            layout.addWidget(self.NewFolderInError)
            self.NewFolderInError.setStyleSheet("QLabel { color : red; }")
            self.NewFolderInError.setVisible(False)
            buttonLayout = QHBoxLayout()
            okButton = QPushButton("OK")
            okButton.clicked.connect(self.newFolderOK)
            buttonLayout.addWidget(okButton)
            cancelButton = QPushButton("Cancel")
            cancelButton.clicked.connect(lambda: self.NewFolderDialog.close())
            buttonLayout.addWidget(cancelButton)
            layout.addLayout(buttonLayout)
            self.NewFolderDialog.setLayout(layout)
            self.NewFolderDialog.exec_()

    def newFolderOK(self):
        name = self.NewFolderName.text()
        if (name in  [self.ListOfUserFolders[i].getName() for i in self.pathToFolders[str(self.UserTree.currentItem())].folders]
            or name == ''):
            self.NewFolderInError.setVisible(True)
            self.NewFolderName.setText(None)
        else:
            self.client = socket.socket()
            self.client.connect((self.host, self.port))
            self.client.send("NewFolder".encode())
            self.client.recv(1024).decode()
            self.client.send(name.encode())

            self.client.recv(1024).decode()
            self.client.send(str(max(self.ListOfUserFolders) + 1).encode())

            self.client.recv(1024).decode()
            self.client.send(str(self.pathToFolders[str(self.UserTree.currentItem())].id).encode())
            self.client.recv(1024).decode()
            self.client.close()

        id = max(self.ListOfUserFolders) + 1
        parentId = self.pathToFolders[str(self.UserTree.currentItem())].id
        newFolder = Folder(name = name, id = id)
        self.ListOfUserFolders[parentId].addFolder(id)
        self.ListOfUserFolders[id] = newFolder
        parent = self.UserTree.currentItem()

        path = QTreeWidgetItem(parent, [name])
        path.setIcon(0, QIcon(QPixmap('Icons//Folder.png')))
        newFolder.setPath(path)
        self.pathToFolders[str(path)] = newFolder
        self.updateWindow()

        self.NewFolderDialog.close()

    def changeName(self):
        if (len(self.UserTree.selectedItems()) != 0
            and (len(self.WindowForUserFolders.selectedItems()) == 0
                 or self.type != "UploadingFile")):
            self.ChangeNameDialog = QDialog(self)
            self.ChangeNameDialog.setWindowTitle("Change the name")
            layout = QVBoxLayout()
            textlabel = QLabel()
            layout.addWidget(textlabel)
            tasklabel = QLabel("Введите новое название:")
            layout.addWidget(tasklabel)
            if ((len(self.WindowForUserFolders.selectedItems()) == 0
                  or self.type == "Folder")):
                self.ChangeNameType = "Folder"
                if len(self.WindowForUserFolders.selectedItems()) == 0:
                    textlabel.setText("Название папки " + self.UserTree.currentItem().text(0)
                                      + " будет изменено")
                else:
                    textlabel.setText("Название папки " + self.text
                                      + " будет изменено")
                self.ChangeNameName = QLineEdit()
                layout.addWidget(self.ChangeNameName)

            else:
                self.ChangeNameType = "File"
                textlabel.setText("Название файла " + self.text
                                  + " будет изменено")
                locallayout = QHBoxLayout()
                self.ChangeNameName = QLineEdit()
                locallayout.addWidget(self.ChangeNameName)
                format = QLabel(self.text[self.text.rfind('.'):])
                locallayout.addWidget(format)
                layout.addLayout(locallayout)

            self.ChangeNameInError = QLabel("Недопустимое название")
            layout.addWidget(self.ChangeNameInError)
            self.ChangeNameInError.setStyleSheet("QLabel { color : red; }")
            self.ChangeNameInError.setVisible(False)
            buttonLayout = QHBoxLayout()
            okButton = QPushButton("OK")
            okButton.clicked.connect(self.changeNameOK)
            buttonLayout.addWidget(okButton)
            cancelButton = QPushButton("Cancel")
            cancelButton.clicked.connect(lambda: self.ChangeNameDialog.close())
            buttonLayout.addWidget(cancelButton)
            layout.addLayout(buttonLayout)

            self.ChangeNameDialog.setLayout(layout)
            self.ChangeNameDialog.exec_()

    def changeNameOK(self):
        print(self.pathToFolders[str(self.UserTree.currentItem())].id)
        name = self.ChangeNameName.text()
        if name == '':
            self.ChangeNameInError.setVisible(True)
            self.ChangeNameName.setText(None)
        elif (self.ChangeNameType == "Folder" #Если выбрана папка в листе, но новое название уже есть в родительской папке(у папки/файла)
            and len(self.WindowForUserFolders.selectedItems()) != 0
            and (name in [self.ListOfUserFolders[i].getName() for i in self.pathToFolders[str(self.UserTree.currentItem())].folders]
                 or name in [text for text, id in self.pathToFolders[str(self.UserTree.currentItem())].files])):
            self.ChangeNameInError.setVisible(True)
            self.ChangeNameName.setText(None)
        elif (self.ChangeNameType == "Folder"#Если выбрана папка в дереве, но она корневая/ новое название уже есть в родительской папке(у папки/файла)
              and len(self.WindowForUserFolders.selectedItems()) == 0
              and (self.pathToFolders[str(self.UserTree.currentItem())].id == 0
                   or  name in [self.ListOfUserFolders[i].getName() for i in self.pathToFolders[str(self.UserTree.currentItem().parent())].folders]
                   or  name in [text for text, id in self.pathToFolders[str(self.UserTree.currentItem().parent())].files])):
            self.ChangeNameInError.setVisible(True)
            self.ChangeNameName.setText(None)
        elif (self.ChangeNameType == "File"#Если выбран файл в листе, он новое название == предыдущему/ совпадает с другим файлом
              and (name + self.text[self.text.rfind('.'):]) in [text for text, id in self.pathToFolders[str(self.UserTree.currentItem())].files]):
            self.ChangeNameInError.setVisible(True)
            self.ChangeNameName.setText(None)
        else:
            self.client = socket.socket()
            self.client.connect((self.host, self.port))
            self.client.send("ChangeName".encode())
            self.client.recv(1024).decode()
            if self.ChangeNameType == "File":
                self.client.send("File".encode())
                self.client.recv(1024).decode()
                self.client.send((str(self.ID)).encode())
                self.client.recv(1024).decode()
                self.client.send((name + self.text[self.text.rfind('.'):]).encode())
                self.client.recv(1024).decode()
                self.client.send(str(self.pathToFolders[str(self.UserTree.currentItem())].id).encode())
            else:
                self.client.send("Folder".encode())
                self.client.recv(1024).decode()
                if len(self.WindowForUserFolders.selectedItems()) != 0:
                    self.client.send((str(self.ID)).encode())
                else:
                    self.client.send(str(self.pathToFolders[str(self.UserTree.currentItem())].id).encode())
                self.client.recv(1024).decode()
                self.client.send(name.encode())
            self.client.recv(1024).decode()
            self.client.close()

            if self.ChangeNameType == "File":
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
            self.ChangeNameDialog.close()

    def delete(self):
        if (len(self.UserTree.selectedItems()) != 0
            and (len(self.WindowForUserFolders.selectedItems()) == 0
                 or self.type != "UploadingFile")
            and not (len(self.WindowForUserFolders.selectedItems()) == 0
                     and self.pathToFolders[str(self.UserTree.currentItem())].id == 0)):
            self.DeleteDialog = QDialog(self)
            self.DeleteDialog.setWindowTitle("Delete")
            layout = QVBoxLayout()
            textlabel = QLabel()
            layout.addWidget(textlabel)
            if ((len(self.WindowForUserFolders.selectedItems()) == 0
                  or self.type == "Folder")):
                self.DeleteType = "Folder"
                if len(self.WindowForUserFolders.selectedItems()) == 0:
                    textlabel.setText("Папка " + self.UserTree.currentItem().text(0)
                                      + " будет удалена")
                else:
                    textlabel.setText("Папка " + self.text
                                      + " будет удалена")
            else:
                self.DeleteType = "File"
                textlabel.setText("Файл " + self.text
                                  + " будет удален")
            buttonLayout = QHBoxLayout()
            okButton = QPushButton("OK")
            okButton.clicked.connect(self.deleteOK)
            buttonLayout.addWidget(okButton)
            cancelButton = QPushButton("Cancel")
            cancelButton.clicked.connect(lambda: self.DeleteDialog.close())
            buttonLayout.addWidget(cancelButton)
            layout.addLayout(buttonLayout)

            self.DeleteDialog.setLayout(layout)
            self.DeleteDialog.exec_()

    def deleteOK(self):
        if self.DeleteType == "File":
            files = []
            for text, id in self.pathToFolders[str(self.UserTree.currentItem())].files:
                if id != self.ID:
                    files.append((text, id))
            self.pathToFolders[str(self.UserTree.currentItem())].files = files
        else:
            if len(self.WindowForUserFolders.selectedItems()) != 0:
                self.folderDeleter(folder = self.ID,
                                   parent = self.pathToFolders[str(self.UserTree.currentItem())].id)
            else:
                self.folderDeleter(folder = self.pathToFolders[str(self.UserTree.currentItem())].id,
                                   parent = self.pathToFolders[str(self.UserTree.currentItem().parent())].id)
            for i in self.ListOfUserFolders:
                print(self.ListOfUserFolders[i].name)
            print()
            for i in self.pathToFolders:
                print(self.pathToFolders[i].name)
        self.DeleteDialog.close()

    def folderDeleter(self, folder, parent = None):
        if parent != None:
            for i in range(len(self.ListOfUserFolders[parent].folders)):
                if self.ListOfUserFolders[parent].folders[i] == folder:
                    self.ListOfUserFolders[parent].folders.pop(i)
                    break
        for childFolder in self.ListOfUserFolders[folder].folders:
            self.folderDeleter(folder = childFolder, parent = folder)
        self.ListOfUserFolders[parent].path.removeChild(self.ListOfUserFolders[folder].path)
        del self.pathToFolders[str(self.ListOfUserFolders[folder].path)]
        del self.ListOfUserFolders[folder]
