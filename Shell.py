# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:14:45 2019

@author: Даня
"""

import csv, socket
from PyQt5.QtGui import (QPixmap,
                         QIcon,
                         QMovie)
from PyQt5.QtCore import (QSize, QTimer, Qt)
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
                             QDialog,
                             QMessageBox,
                             QToolBar)

from Cloud_Folder import Cloud_Folder
from nanachi import nanachi
from ThreadForConnection import ThreadForConnection

class Shell(QMainWindow):
    def __init__(self):
        super().__init__()

        self.backgrouds = {"Anime": ["CuteUserTree.jpg", "CuteUserFolders.jpg"]}

        self.listOfNormalIcons = {'Download from server':'Download.png',
                                  'Upload to server':'Upload.png',
                                  'Delete':'Delete.png',
                                  'Sign out':'logOut.png',
                                  'New folder':'new_folder.png',
                                  'Change name':'change_name.png' }
        self.listOfAnimeIcons = {'Download from server':'Download.jpg',
                                  'Upload to server':'Upload.jpg',
                                  'Delete':'Delete.jpg',
                                  'Sign out':'sleepy.jpg',
                                  'New folder':'thinking.png',
                                  'Change name':'writing.png'}
        self.listOfCuteIcons = {'Download from server':'',
                                  'Upload to server':'',
                                  'Delete':'',
                                  'Sign out':'',
                                  'New Folder':'',
                                  'Change name':''}
        self.ToolBarElements = [['Download.png', 'Download from server', self.Download],
                                ['Upload.png','Upload to server', self.Upload],
                                ['Delete.png', 'Delete', self.Delete],
                                ['new_folder.png', 'New folder', self.New_folder],
                                ['change_name.png', 'Change name', self.Change_name],
                                ['logOut.png', 'Sign out', self.signOut],]

        self.toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

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
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(self.spacer)

        for path, text in [("Icons//listofdowloads.png", 'ShowListOfDownloads'),
                           ("Icons//listofuploads.png", 'ShowListOfUploads')]:
            button = QPushButton(QIcon(path), '')
            button.setObjectName(text)
            button.setFlat(True)
            button.setFixedSize(30, 30)
            button.setIconSize(QSize(25, 25))
            self.toolbar.addWidget(button)

        qApp.installEventFilter(self)

        self.setMinimumSize(300, 300)

        self.host = 'localhost'
        self.port = 60000
        self.connectionStatus = False

        self.style = "Normal"

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
        #widgetForConnecting.setSizeHint(self.gifLabel.sizeHint())
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

        self.main_widget = Cloud_Folder(host = self.host, port = self.port, parent = self)

        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Cloud Folder")
        self.setWindowIcon(QIcon(QPixmap('Icons//mega.jpg')))
        self.setGeometry(50, 50, 1200, 600)

    def Download(self):
        if len(self.main_widget.WindowForUserFolders.selectedItems()) != 0:
            self.main_widget.startNewDownloading()

    def Upload(self):
        self.main_widget.upload()

    def Delete(self):
        self.main_widget.delete()

    def signOut(self):
        with open('Data//user.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["False"] + [""] + [""])
        self.close()

    def changeThemeToNormal(self):
        for i in self.listOfActions:
            self.listOfActions[i].setIcon(QIcon('Icons//' + self.listOfNormalIcons[i]))
        self.main_widget.UserTree.setStyleSheet("background: white;")
        self.main_widget.WindowForUserFolders.setStyleSheet("background: white;")
        self.style = "Normal"

    def changeThemeToAnime(self):
        for i in self.listOfActions:
            self.listOfActions[i].setIcon(QIcon('Icons//' + self.listOfAnimeIcons[i]))
        self.normal.setIcon(QIcon('Icons//supa.png'))
        self.style = "Anime"
        self.backgroundChanger()

    def backgroundChanger(self):
        if self.style != "Normal":
            x1, y1, x2, y2 = self.geometry().getCoords()
            for path in self.backgrouds[self.style]:
                image = QPixmap("Icons//" + path)
                image = image.scaled((x2 + 50 - x1) / 4, y2 - 50 - y1)
                image.save("Icons//Scaled" + path, "JPG")
            self.main_widget.UserTree.setStyleSheet("background-image: url(Icons//Scaled" + self.backgrouds[self.style][0] + ");")
            self.main_widget.WindowForUserFolders.setStyleSheet("background-image: url(Icons//Scaled" + self.backgrouds[self.style][1] + ");")

    def New_folder(self):
        self.main_widget.newFolder()

    def Change_name(self):
        self.main_widget.changeName()

    def eventFilter(self, obj, event):
        if obj.objectName() == 'ShowListOfDownloads':
            if event.type() == QEvent.Enter:
                x1, y1, x2, y2 = self.geometry().getCoords()
                self.main_widget.WindowForProgBars.move(x2 - 300, y1 + 40) #Тут вроде понятно
                self.main_widget.WindowForProgBars.show()

            if event.type() == QEvent.Leave:
                self.main_widget.WindowForProgBars.hide()

        elif obj.objectName() == 'ShowListOfUploads':
            if event.type() == QEvent.Enter:
                x1, y1, x2, y2 = self.geometry().getCoords()
                self.main_widget.WindowForUploadings.move(x2 - 300, y1 + 40) #Тут вроде понятно
                self.main_widget.WindowForUploadings.show()

            if event.type() == QEvent.Leave:
                self.main_widget.WindowForUploadings.hide()

        return QWidget.eventFilter(self, obj, event)

    def resizeEvent(self, event):
        self.backgroundChanger()

    def closeEvent(self, event):
        if len(self.main_widget.ListOfDowloads) != 0 or len(self.main_widget.ListOfUploads) != 0:
            reply = QMessageBox.question(self, "Warning!",
                                         "You have unfinished deals...", QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                event.ignore()
            else:
                event.ignore()

        else:
            self.client = socket.socket()
            self.client.connect((self.host, self.port))
            self.client.send("Exit".encode())
            self.client.recv(1024).decode()
            self.client.close()
