# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:14:45 2019

@author: Даня
"""

import csv, socket, time
from PyQt5.QtGui import (QPixmap,
                         QIcon,
                         QMovie)
from PyQt5.QtCore import (QSize, QTimer, Qt)
from PyQt5.Qt import QEvent
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import (QLabel,
                             QVBoxLayout,
                             QPushButton,
                             QWidget,
                             QMainWindow,
                             QAction,
                             QLineEdit,
                             QRadioButton,
                             qApp,
                             QSizePolicy,
                             QToolButton,
                             QMenu,
                             QMessageBox,
                             QToolBar)

from Cloud_Folder import Cloud_Folder
from ThreadForConnection import ThreadForConnection

class Shell(QMainWindow):
    def __init__(self):
        super().__init__()

        self.backgrounds = {"Anime": ["CuteUserTree.jpg", "CuteUserFolders.jpg"],
                            "Elon": ["Elon.jpg", "Musk.jpg"],
                            "Gachi": ["Boss.jpg", "Dungeon.jpg"]}

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
        self.listOfElonIcons = {'Download from server':'E.jpg',
                                  'Upload to server':'L.jpg',
                                  'Delete':'O.jpg',
                                  'Sign out':'M.jpg',
                                  'New folder':'U.jpg',
                                  'Change name':'S.jpg'}
        self.listOfGachiIcons = {'Download from server':'Sneaky.jpg',
                                  'Upload to server':'Gasm.jpg',
                                  'Delete':'Master.jpg',
                                  'Sign out':'Sneaky.jpg',
                                  'New folder':'Gasm.jpg',
                                  'Change name':'Master.jpg'}
        self.ToolBarElements = [['Download.png', 'Download from server', self.Download],
                                ['Upload.png','Upload to server', self.Upload],
                                ['Delete.png', 'Delete', self.Delete],
                                ['new_folder.png', 'New folder', self.New_folder],
                                ['change_name.png', 'Change name', self.Change_name],
                                ['logOut.png', 'Sign out', self.signOut],]

        self.music = {'Ass we can': QSound("Sounds//Ass we can.wav")}

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
        self.anime = menu.addAction(QIcon('Icons//changer.jpg'), "Anime")
        self.anime.triggered.connect(self.changeThemeToAnime)
        self.elon = menu.addAction(QIcon('Icons//Tsu.jpg'), "Elon")
        self.elon.triggered.connect(self.changeThemeToElon)
        self.gachi = menu.addAction(QIcon('Icons//Elisium.png'), "Gachi")
        self.gachi.triggered.connect(self.changeThemeToGachi)

        self.changer.setMenu(menu)
        self.changer.setPopupMode(self.changer.MenuButtonPopup)
        self.toolbar.addWidget(self.changer)

        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(self.spacer)

        for path, text in [("Icons//listofdownloads.png", 'ShowListOfDownloads'),
                           ("Icons//listofuploads.png", 'ShowListOfUploads')]:
            button = QPushButton(QIcon(path), '')
            button.setObjectName(text)
            button.setFlat(True)
            button.setFixedSize(30, 30)
            button.setIconSize(QSize(25, 25))
            self.toolbar.addWidget(button)

        qApp.installEventFilter(self)

        self.setMinimumSize(300, 300)

        self.host = '18.224.110.176'
        self.port = 60000
        self.connectionStatus = False
        self.login, self.password, self.answer = "", "", ""

        self.style = "Normal"

        self.signIn()

    def connectionProblem(self, type):
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

        self.thread = ThreadForConnection(type = type, host = self.host, port = self.port)
        self.thread.signal.connect(self.defForThread)
        self.thread.start()

    def defForThread(self, data):
        if data[0] == "logIn" or data[0] == "registration":
            self.client = data[1]
            self.connectionStatus = True
            gif = QMovie('Icons//successfulpepega.gif')
            self.gifLabel.setMovie(gif)
            gif.start()
            self.timerScreen = QTimer()
            self.timerScreen.setInterval(3000)
            self.timerScreen.start()
            self.timerScreen.setSingleShot(True)
            if data[0] == "logIn":
                self.timerScreen.timeout.connect(self.logIn)
            else:
                self.timerScreen.timeout.connect(self.registration)

        else:
            self.client.send("Ready".encode())
            self.client.close()
            self.mainMission()

    def signIn(self):
        self.toolbar.setVisible(False)
        self.begining = QWidget()
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
        self.nameInstruction = QLabel("Enter your username:")
        layout.addWidget(self.nameInstruction)
        self.userName = QLineEdit()
        layout.addWidget(self.userName)
        self.passInstruction = QLabel("Enter your password:")
        layout.addWidget(self.passInstruction)
        self.userPass = QLineEdit()
        self.userPass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.userPass)
        self.remeberme = QRadioButton("Rememeber me")
        self.remeberme.setChecked(True)
        layout.addWidget(self.remeberme)
        self.log = QPushButton("Sign in")
        self.log.clicked.connect(self.logIn)
        self.log.setShortcut("Enter")
        layout.addWidget(self.log)
        self.sign = QPushButton("Sign up")
        self.sign.clicked.connect(self.signUp)
        layout.addWidget(self.sign)
        self.begining.setLayout(layout)
        self.setCentralWidget(self.begining)
        self.mode = "logIn"
        if self.check == "True":
            self.userName.setText(self.login)
            self.userPass.setText(self.password)
            self.logIn()

    def logIn(self):
        if self.mode == "logIn":
            self.logInError.setVisible(False) #Если была ошибка - скрываем
            print(self.connectionStatus)

            if self.connectionStatus == False:
                if self.answer != "Success":
                    self.login = self.userName.text()
                    self.password = self.userPass.text()
                try:
                    self.client = socket.socket()
                    self.client.connect((self.host, self.port))
                    self.connectionStatus = True
                    self.logIn()
                except (ConnectionRefusedError, TimeoutError):
                    self.connectionProblem(type = "logIn")

            else:
                self.client.send("Login".encode())
                self.client.recv(1024).decode()

                data = self.login + '~' + self.password

                self.client.send(data.encode())

                self.answer = self.client.recv(1024).decode()
                print(self.answer)

                if self.answer == 'Passed':

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
                    self.setWindowIcon(QIcon(QPixmap('Icons//Tsu.jpg')))
                    self.setMinimumSize(360, 350)

                    self.thread = ThreadForConnection(type = "Passed", client = self.client)
                    self.thread.signal.connect(self.defForThread)
                    self.thread.start()

                elif self.answer == 'LogIn':
                    self.logInError.setText("Login and password do not match.")
                    self.logInError.setVisible(True)
                    self.userPass.setText(None)
                    self.client.close()
                    self.connectionStatus = False

                elif self.answer == 'Password':
                    self.logInError.setVisible(True)
                    self.logInError.setText("Login does not exist.")
                    self.userPass.setText(None)
                    self.userName.setText(None)
                    self.client.close()
                    self.connectionStatus = False

                elif self.answer == "AlreadyUsed":
                    self.logInError.setVisible(True)
                    self.logInError.setText("This login is used in another session.")
                    self.userPass.setText(None)
                    self.userName.setText(None)
                    self.client.close()
                    self.connectionStatus = False

    def signUp(self):
        self.mode = "signUp"
        self.nameInstruction.setText("Registration\n\nEnter your new username:")
        self.log.setText("Sign up")
        self.log.clicked.connect(self.registration)
        self.sign.setText("Back to sign in")
        self.sign.clicked.connect(self.signIn)

    def registration(self):
        if self.mode == "signUp":
            if self.connectionStatus == False:
                self.login = self.userName.text()
                self.password = self.userPass.text()
                if (len(self.login) == 0 or len(self.password) == 0
                    or " " in self.login or " " in self.password
                    or "~" in self.login or "~" in self.password):
                    self.logInError.setVisible(True)
                    self.logInError.setText("Invalid data")
                    self.userPass.setText(None)
                    self.userName.setText(None)
                else:
                    try:
                        self.client = socket.socket()
                        self.client.connect((self.host, self.port))
                        self.connectionStatus = True
                        self.registration()
                    except (ConnectionRefusedError, TimeoutError):
                        self.connectionProblem(type = "registration")
            else:
                self.client.send("Registration".encode())
                self.client.recv(1024).decode()

                data = self.login + '~' + self.password

                self.client.send(data.encode())

                self.answer = self.client.recv(1024).decode()
                self.client.close()
                print(self.answer)

                if self.answer == "Success":
                    time.sleep(3)
                    self.mode = "logIn"
                    self.connectionStatus = False
                    self.logIn()

                elif self.answer == "AlreadyUsed":
                    self.logInError.setVisible(True)
                    self.logInError.setText("This login is already used.")
                    self.userPass.setText(None)
                    self.userName.setText(None)
                    self.connectionStatus = False

    def mainMission(self):
        self.toolbar.setVisible(True)

        self.main_widget = Cloud_Folder(host = self.host, port = self.port,
                                        parent = self,
                                        login = self.login + '~' + self.password)

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
        self.main_widget.updateWindow()

    def changeThemeToAnime(self):
        for i in self.listOfActions:
            self.listOfActions[i].setIcon(QIcon('Icons//' + self.listOfAnimeIcons[i]))
        self.normal.setIcon(QIcon('Icons//supa.png'))
        self.style = "Anime"
        self.backgroundChanger()
        self.main_widget.updateWindow()

    def changeThemeToElon(self):
        for i in self.listOfActions:
            self.listOfActions[i].setIcon(QIcon('Icons//' + self.listOfElonIcons[i]))
        self.normal.setIcon(QIcon('Icons//supa.png'))
        self.style = "Elon"
        self.backgroundChanger()
        self.main_widget.updateWindow()

    def changeThemeToGachi(self):
        for i in self.listOfActions:
            self.listOfActions[i].setIcon(QIcon('Icons//' + self.listOfGachiIcons[i]))
        self.normal.setIcon(QIcon('Icons//supa.png'))
        self.style = "Gachi"
        self.music["Ass we can"].play()
        self.backgroundChanger()
        self.main_widget.updateWindow()


    def backgroundChanger(self):
        if self.style != "Normal":
            x1, y1, x2, y2 = self.main_widget.UserTree.geometry().getCoords()
            x12, y12, x22, y22 = self.main_widget.WindowForUserFolders.geometry().getCoords()
            TreeImage = QPixmap("Icons//" + self.backgrounds[self.style][0])
            TreeImage = TreeImage.scaled(x2 - x1, y2 - y1)
            TreeImage.save("Icons//Scaled" + self.backgrounds[self.style][0], "JPG")

            ListImage = QPixmap("Icons//" + self.backgrounds[self.style][1])
            ListImage = ListImage.scaled(x22 - x12, y22 - y12)
            ListImage.save("Icons//Scaled" + self.backgrounds[self.style][1], "JPG")
            self.main_widget.UserTree.setStyleSheet("background-image: url(Icons//Scaled" + self.backgrounds[self.style][0] + ");")
            self.main_widget.WindowForUserFolders.setStyleSheet("background-image: url(Icons//Scaled" + self.backgrounds[self.style][1] + ");")

    def New_folder(self):
        self.main_widget.newFolder()

    def Change_name(self):
        self.main_widget.changeName()

    def eventFilter(self, obj, event):
        if obj.objectName() == 'ShowListOfDownloads':
            if event.type() == QEvent.Enter:
                x1, y1, x2, y2 = self.geometry().getCoords()
                self.main_widget.WindowForProgBars.move(x2 - 300, y1 + 40)
                self.main_widget.WindowForProgBars.show()

            if event.type() == QEvent.Leave:
                self.main_widget.WindowForProgBars.hide()

        elif obj.objectName() == 'ShowListOfUploads':
            if event.type() == QEvent.Enter:
                x1, y1, x2, y2 = self.geometry().getCoords()
                self.main_widget.WindowForUploadings.move(x2 - 300, y1 + 40)
                self.main_widget.WindowForUploadings.show()

            if event.type() == QEvent.Leave:
                self.main_widget.WindowForUploadings.hide()

        return QWidget.eventFilter(self, obj, event)

    def resizeEvent(self, event):
        self.backgroundChanger()

    def closeEvent(self, event):
        if (self.toolbar.isVisible()
            and (len(self.main_widget.ListOfDownloads) != 0 or len(self.main_widget.ListOfUploads) != 0)):
            reply = QMessageBox.question(self, "Warning!",
                                         "You have unfinished deals...", QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                event.ignore()
            else:
                event.ignore()

        elif self.answer == "Passed":
            try:
                self.client = socket.socket()
                self.client.connect((self.host, self.port))
                self.client.send("Exit".encode())
                self.client.recv(1024).decode()
                self.client.send((self.login + '~' + self.password).encode())
                self.client.recv(1024).decode()
                self.client.close()
            except:
                pass
