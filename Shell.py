# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:14:45 2019

@author: Даня
"""

import csv, socket
from PyQt5.QtGui import (QPixmap,
                         QIcon,
                         QMovie)
from PyQt5.QtCore import (QSize, QTimer, Qt, pyqtSignal)
from PyQt5.Qt import QEvent
from PyQt5.QtWidgets import (QLabel,
                             QVBoxLayout,
                             QHBoxLayout,
                             QPushButton,
                             QWidget,
                             QMainWindow,
                             QFileDialog,
                             QAction,
                             QLineEdit,
                             QRadioButton,
                             qApp,
                             QSizePolicy,
                             QToolButton,
                             QMenu,
                             QDialog)

from Cloud_Folder import Cloud_Folder
from nanachi import nanachi
from ThreadForConnection import ThreadForConnection

class Shell(QMainWindow):
    def __init__(self):
        super().__init__()

        self.listOfNormalIcons = {'Download from server':'Download.png',
                                  'Upload to server':'Upload.png',
                                  'Delete':'Delete.png',
                                  'Find someone':'Find_someone.png',
                                  'Sign out':'logOut.png',
                                  'New folder':'new_folder.png',
                                  'Change name':'change_name.png' }
        self.listOfAnimeIcons = {'Download from server':'Download.jpg',
                                  'Upload to server':'Upload.jpg',
                                  'Delete':'Delete.jpg',
                                  'Find someone':'Find_somechan.png',
                                  'Sign out':'sleepy.jpg',
                                  'New folder':'new_folder.png',
                                  'Change name':'change_name.png'}
        self.listOfCuteIcons = {'Download from server':'',
                                  'Upload to server':'',
                                  'Delete':'',
                                  'Find someone':'',
                                  'Sign out':'',
                                  'New Folder':'',
                                  'Change name':''}
        self.ToolBarElements = [['Download.png', 'Download from server', self.Download],
                                ['Upload.png','Upload to server', self.Upload],
                                ['Delete.png', 'Delete', self.Delete],
                                ['Find_someone.png', 'Find someone', self.Find_someone],
                                ['new_folder.png', 'New folder', self.New_folder],
                                ['change_name.png', 'Change name', self.Change_name],
                                ['logOut.png', 'Sign out', self.signOut],]

        self.toolbar = self.addToolBar('Commands')
        self.toolbar.setMovable(False)

        self.listOfActions  = {}

        for path, text, action in self.ToolBarElements:
            newAction = QAction(QIcon('Icons//' + path), text, self)
            newAction.triggered.connect(action)
            self.listOfActions[text] = newAction
            self.toolbar.addAction(newAction)


        self.changer = QToolButton()
        self.changer.setIcon(QIcon('Icons//idol.jpg'))
        menu = QMenu()
        self.normal = menu.addAction(QIcon('Icons//elonger.jpg'), "Normal")
        self.normal.triggered.connect(self.changeThemeToNormal)
        anime = menu.addAction(QIcon('Icons//changer.jpg'), "Anime")
        anime.triggered.connect(self.changeThemeToAnime)
        self.changer.setMenu(menu)
        self.changer.setPopupMode(self.changer.MenuButtonPopup)
        self.toolbar.addWidget(self.changer)

        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) #Отодвигаем кнопку с загрузками
        self.toolbar.addWidget(self.spacer)

        self.ShowListOfDownloads = QPushButton(QIcon("Icons//List.png"),'')
        self.ShowListOfDownloads.setObjectName('ShowListOfDownloads')
        self.ShowListOfDownloads.setFlat(True)
        self.ShowListOfDownloads.setFixedSize(30, 30)
        self.ShowListOfDownloads.setIconSize(QSize(25, 25)) #Подгоняем кнопку под размер tollbar'овских элементов
        self.toolbar.addWidget(self.ShowListOfDownloads)
        qApp.installEventFilter(self) #Магическая штука, включающая отслеживание мыши, на сколько я понимаю

        self.setMinimumSize(300, 300)

        self.host = 'localhost'
        self.port = 60000
        self.connectionStatus = False

        self.signIn()

    def connectionProblem(self):
        widgetForConnecting = QWidget()
        layout = QVBoxLayout()
        text = QLabel("Connecting. Please stand by")
        text.setAlignment(Qt.AlignCenter)
        layout.addWidget(text)

        self.gifLabel = QLabel()
        gif = QMovie('Icons//connectingpepega.gif')
        self.gifLabel.setMovie(gif)
        gif.start()
        self.gifLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.gifLabel)
        widgetForConnecting.setLayout(layout)
        self.setCentralWidget(widgetForConnecting)
        self.setWindowTitle('Connecting')
        self.setWindowIcon(QIcon(QPixmap('Icons//hot.jpg')))

        self.thread = ThreadForConnection(type = 1, host = self.host, port = self.port)
        self.thread.signal.connect(self.defForThread)
        self.thread.start()

    def defForThread(self, data):
        if data[0] == 1:
            self.client = data[1]
            self.connectionStatus = True
            gif = QMovie('Icons//successfulpepega.gif')
            self.gifLabel.setMovie(gif)
            gif.start()
            self.timerScreen = QTimer()
            self.timerScreen.setInterval(3000)
            self.timerScreen.start()
            self.timerScreen.setSingleShot(True)
            self.timerScreen.timeout.connect(self.signIn)

        else:
            self.client.send("Ready".encode())
            self.client.close()
            self.mainMission()

    def signIn(self):
        self.toolbar.setVisible(False)
        self.begining = QWidget() #Нужны комментарии?
        self.setWindowIcon(QIcon(QPixmap("Icons//hot.jpg")))
        self.setWindowTitle("Try me.")
        with open('Data//user.csv', newline='') as csvfile:
            fresh = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in fresh:
                self.check, self.login, self.password = row
        layout = QVBoxLayout()
        self.logInError = QLabel()
        self.logInError.setStyleSheet("QLabel { background-color : white; color : red; }")
        self.logInError.setVisible(False)
        layout.addWidget(self.logInError)
        nameInstruction = QLabel("Enter username:")
        layout.addWidget(nameInstruction)
        self.userName = QLineEdit()
        layout.addWidget(self.userName)
        passInstruction = QLabel("Enter your password:")
        layout.addWidget(passInstruction)
        self.userPass = QLineEdit()
        self.userPass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.userPass)
        self.remeberme = QRadioButton("Rememeber me")
        self.remeberme.setChecked(True)
        layout.addWidget(self.remeberme)
        log = QPushButton("Log in")
        log.clicked.connect(self.logIn)
        layout.addWidget(log)
        sign = QPushButton("Sign in")
        sign.clicked.connect(lambda: print("А фигушки!"))
        layout.addWidget(sign)
        self.begining.setLayout(layout)
        self.setCentralWidget(self.begining)
        if self.check == "True" or self.connectionStatus == True:
            self.userName.setText(self.login)
            self.userPass.setText(self.password)
            self.logIn()

    def logIn(self):
        self.logInError.setVisible(False) #Если была ошибка - скрываем
        print(self.connectionStatus)

        self.login = self.userName.text()
        self.password = self.userPass.text()

        if self.connectionStatus == False:
            try:
                self.client = socket.socket()
                self.client.connect((self.host, self.port))
                self.connectionStatus = True
                self.logIn()
            except ConnectionRefusedError:
                self.connectionProblem()

        else:
            self.client.send("Login".encode())
            self.client.recv(1024).decode()

            data = self.login + '~' + self.password

            self.client.send(data.encode())

            answer = self.client.recv(1024).decode()
            print(answer)

            if answer == 'Passed':

                if self.remeberme.isChecked():
                    with open('Data//user.csv', 'w', newline='') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        spamwriter.writerow(["True"] + [self.login] + [self.password])
                else:
                    with open('Data//user.csv', 'w', newline='') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        spamwriter.writerow(["False"] + [""] + [""])
                 #self.user_id = client.recv(1024).decode() #Если вдруг у нас можнт быть ненулевой корень


                first = QLabel()
                dance = QMovie('Icons//loading.gif')
                first.setMovie(dance)
                dance.start()
                self.setCentralWidget(first)
                self.setWindowTitle('Loading')
                self.setWindowIconText(nanachi)
                self.setWindowIcon(QIcon(QPixmap('Icons//Tsu.jpg')))

                self.thread = ThreadForConnection(type = 2, client = self.client)
                self.thread.signal.connect(self.defForThread)
                self.thread.start()

            elif answer == 'LogIn':
                self.logInError.setText("Login and password do not match.")
                self.logInError.setVisible(True)
                self.userPass.setText(None)
                self.client.close()
                self.connectionStatus = False

            elif answer == 'Password':
                self.logInError.setVisible(True)
                self.logInError.setText("Login does not exist.")
                self.userPass.setText(None)
                self.userName.setText(None)
                self.client.close()
                self.connectionStatus = False

    def mainMission(self):
        self.toolbar.setVisible(True)

        self.main_widget = Cloud_Folder()

        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Cloud Folder")
        self.setWindowIcon(QIcon(QPixmap('Icons//mega.jpg')))
        self.setGeometry(300, 300, 600, 300)

    def Download(self):
        if (len(self.main_widget.WindowForUserFolders.selectedItems()) != 0 and self.main_widget.ID != None
            and self.main_widget.type != "Folder"):
            print(self.main_widget.ID)
            name = self.main_widget.text

        self.main_widget.startNewDownloading()  #Смотри Cloud_Folder

    def Upload(self):
        print("Upload")
        path = "Lul"
        path = QFileDialog.getOpenFileName(self, "File", "*.*") #возвращает пару путь и еще что-то, непонятно, зачем
        print(path)

    def Delete(self):
        print("Delete")

    def Find_someone(self):
        print("Find_someone")

    def signOut(self):
        with open('Data//user.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["False"] + [""] + [""])
        self.close()

    def changeThemeToNormal(self):
        for i in self.listOfActions:
            self.listOfActions[i].setIcon(QIcon('Icons//' + self.listOfNormalIcons[i]))

    def changeThemeToAnime(self):
        for i in self.listOfActions:
            self.listOfActions[i].setIcon(QIcon('Icons//' + self.listOfAnimeIcons[i]))
        self.normal.setIcon(QIcon('Icons//supa.png'))

    def New_folder(self):
        if len(self.main_widget.UserTree.selectedItems()) != 0:
            self.new_folderDialog = QDialog(self.main_widget)
            self.new_folderDialog.setWindowTitle("New folder")
            layout = QVBoxLayout()
            textlabel = QLabel("Новая папка будет создана в: " + (self.main_widget.UserTree.currentItem().text(0)))
            layout.addWidget(textlabel)
            tasklabel = QLabel("Введите название:")
            layout.addWidget(tasklabel)
            self.new_folderName = QLineEdit()
            layout.addWidget(self.new_folderName)
            self.new_folderInError = QLabel("Недопустимое название папки")
            layout.addWidget(self.new_folderInError)
            self.new_folderInError.setStyleSheet("QLabel { color : red; }")
            self.new_folderInError.setVisible(False)
            buttonLayout = QHBoxLayout()
            okButton = QPushButton("OK")
            okButton.clicked.connect(self.new_folderOK)
            buttonLayout.addWidget(okButton)
            cancelButton = QPushButton("Cancel")
            cancelButton.clicked.connect(lambda: self.new_folderDialog.close())
            buttonLayout.addWidget(cancelButton)
            layout.addLayout(buttonLayout)
            self.new_folderDialog.setLayout(layout)
            self.new_folderDialog.exec_()

    def new_folderOK(self):
        name = self.new_folderName.text()
        if (name in  [self.main_widget.ListOfUserFolders[i].getName() for i in self.main_widget.pathToFolders[str(self.main_widget.UserTree.currentItem())].folders]
            or name == ''):
            self.new_folderInError.setVisible(True)
            self.new_folderName.setText(None)
        else:
            self.client = socket.socket()
            self.client.connect((self.host, self.port))
            self.client.send("NewFolder".encode())
            self.client.recv(1024).decode()
            self.client.send(name.encode())

            self.client.recv(1024).decode()
            self.client.send(str(max(self.main_widget.ListOfUserFolders) + 1).encode())

            self.client.recv(1024).decode()
            self.client.send(str(self.main_widget.pathToFolders[str(self.main_widget.UserTree.currentItem())].id).encode())
            self.client.recv(1024).decode()
            self.client.close()

            self.main_widget.newFolder(name)
            self.new_folderDialog.close()

    def Change_name(self):
        if len(self.main_widget.UserTree.selectedItems()) != 0:
            self.change_nameDialog = QDialog(self.main_widget)
            self.change_nameDialog.setWindowTitle("Change the name")
            layout = QVBoxLayout()
            textlabel = QLabel()
            layout.addWidget(textlabel)
            tasklabel = QLabel("Введите новое название:")
            layout.addWidget(tasklabel)
            if ((len(self.main_widget.WindowForUserFolders.selectedItems()) == 0
                  or self.main_widget.type == "Folder")):
                self.change_nameType = "Folder"
                if len(self.main_widget.WindowForUserFolders.selectedItems()) == 0:
                    textlabel.setText("Название папки " + self.main_widget.UserTree.currentItem().text(0)
                                      + " будет изменено")
                else:
                    textlabel.setText("Название папки " + self.main_widget.text
                                      + " будет изменено")
                self.change_nameName = QLineEdit()
                layout.addWidget(self.change_nameName)

            else:
                self.change_nameType = "File"
                textlabel.setText("Название файла " + self.main_widget.text
                                  + " будет изменено")
                locallayout = QHBoxLayout()
                self.change_nameName = QLineEdit()
                locallayout.addWidget(self.change_nameName)
                format = QLabel(self.main_widget.text[self.main_widget.text.rfind('.'):])
                locallayout.addWidget(format)
                layout.addLayout(locallayout)

            self.change_nameInError = QLabel("Недопустимое название")
            layout.addWidget(self.change_nameInError)
            self.change_nameInError.setStyleSheet("QLabel { color : red; }")
            self.change_nameInError.setVisible(False)
            buttonLayout = QHBoxLayout()
            okButton = QPushButton("OK")
            okButton.clicked.connect(self.change_nameOK)
            buttonLayout.addWidget(okButton)
            cancelButton = QPushButton("Cancel")
            cancelButton.clicked.connect(lambda: self.change_nameDialog.close())
            buttonLayout.addWidget(cancelButton)
            layout.addLayout(buttonLayout)

            self.change_nameDialog.setLayout(layout)
            self.change_nameDialog.exec_()

    def change_nameOK(self):
        name = self.change_nameName.text()
        if name == '':
            self.change_nameInError.setVisible(True)
            self.change_nameName.setText(None)
        elif (self.change_nameType == "Folder" #Если выбрана папка в листе, но новое название уже есть в родительской папке(у папки/файла)
            and len(self.main_widget.WindowForUserFolders.selectedItems()) != 0
            and (name in [self.main_widget.ListOfUserFolders[i].getName() for i in self.main_widget.pathToFolders[str(self.main_widget.UserTree.currentItem())].folders]
                 or name in [text for text, id in self.main_widget.pathToFolders[str(self.main_widget.UserTree.currentItem())].files])):
            self.change_nameInError.setVisible(True)
            self.change_nameName.setText(None)
        elif (self.change_nameType == "Folder"#Если выбрана папка в дереве, но она корневая/ новое название уже есть в родительской папке(у папки/файла)
              and len(self.main_widget.WindowForUserFolders.selectedItems()) == 0
              and (self.main_widget.UserTree.currentItem().text(0) == self.login
                   or  name in [self.main_widget.ListOfUserFolders[i].getName() for i in self.main_widget.pathToFolders[str(self.main_widget.UserTree.currentItem().parent())].folders]
                   or  name in [text for text, id in self.main_widget.pathToFolders[str(self.main_widget.UserTree.currentItem().parent())].files])):
            self.change_nameInError.setVisible(True)
            self.change_nameName.setText(None)
        elif (self.change_nameType == "File"#Если выбран файл в листе, он новое название == предыдущему/ совпадает с другим файлом
              and (name + self.main_widget.text[self.main_widget.text.rfind('.'):]) in [text for text, id in self.main_widget.pathToFolders[str(self.main_widget.UserTree.currentItem())].files]):
            self.change_nameInError.setVisible(True)
            self.change_nameName.setText(None)
        else:
            self.client = socket.socket()
            self.client.connect((self.host, self.port))
            self.client.send("ChangeName".encode())
            self.client.recv(1024).decode()
            if self.change_nameType == "File":
                self.client.send("File".encode())
                self.client.recv(1024).decode()
                self.client.send((str(self.main_widget.ID)).encode())
                self.client.recv(1024).decode()
                self.client.send((name + self.main_widget.text[self.main_widget.text.rfind('.'):]).encode())
                self.client.recv(1024).decode()
                self.client.send(str(self.main_widget.pathToFolders[str(self.main_widget.UserTree.currentItem())].id).encode())
            else:
                self.client.send("Folder".encode())
                self.client.recv(1024).decode()
                if len(self.main_widget.WindowForUserFolders.selectedItems()) != 0:
                    self.client.send((str(self.main_widget.ID)).encode())
                else:
                    self.client.send(str(self.main_widget.pathToFolders[str(self.main_widget.UserTree.currentItem())].id).encode())
                self.client.recv(1024).decode()
                self.client.send(name.encode())
            self.client.recv(1024).decode()
            self.client.close()
            self.main_widget.changeName(name, self.change_nameType)
            self.change_nameDialog.close()

    def eventFilter(self, obj, event):
        if obj.objectName() == 'ShowListOfDownloads':
            if event.type() == QEvent.Enter:
                x1, y1, x2, y2 = self.geometry().getCoords()
                self.main_widget.WindowForProgBars.move(x2 - 300, y1 + 40) #Тут вроде понятно
                self.main_widget.WindowForProgBars.show()

            if event.type() == QEvent.Leave:
                self.main_widget.WindowForProgBars.hide()

        return QWidget.eventFilter(self, obj, event)

    def closeEvent(self, event):
        self.client = socket.socket()
        self.client.connect((self.host, self.port))
        self.client.send("Exit".encode())
        self.client.recv(1024).decode()
        self.client.close()
