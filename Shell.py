# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:14:45 2019

@author: Даня
"""

import csv
from PyQt5.QtGui import (QPixmap,
                         QIcon,
                         QMovie)
from PyQt5.QtCore import (QSize, QTimer)
from PyQt5.Qt import QEvent
from PyQt5.QtWidgets import (QLabel,
                             QVBoxLayout,
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
                             QMenu)

from Cloud_Folder import Cloud_Folder
from nanachi import nanachi

class Shell(QMainWindow):
    def __init__(self):
        super().__init__()

        self.listOfNormalIcons = {'Download from server':'Download.png',
                                  'Upload to server':'Upload.png',
                                  'Delete':'Delete.png',
                                  'Find someone':'Find_someone.png',
                                  'Sign out':'logOut.png'}
        self.listOfAnimeIcons = {'Download from server':'Download.jpg',
                                  'Upload to server':'Upload.jpg',
                                  'Delete':'Delete.jpg',
                                  'Find someone':'Find_somechan.png',
                                  'Sign out':'sleepy.jpg'}
        self.listOfCuteIcons = {'Download from server':'',
                                  'Upload to server':'',
                                  'Delete':'',
                                  'Find someone':'',
                                  'Sign out':''}
        self.ToolBarElements = [['Download.png', 'Download from server', self.Download],
                                ['Upload.png','Upload to server', self.Upload],
                                ['Delete.png', 'Delete', self.Delete],
                                ['Find_someone.png', 'Find someone', self.Find_someone],
                                ['logOut.png', 'Sign out', self.signOut]]

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

        self.signIn()

    def signIn(self):
        self.toolbar.setVisible(False)
        self.begining = QWidget() #Нужны комментарии?
        self.setWindowIcon(QIcon(QPixmap("Icons//hot.jpg")))
        self.setWindowTitle("Try me.")
        with open('user.csv', newline='') as csvfile:
            fresh = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in fresh:
                self.check, name, password = row
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
        if self.check == "True":
            self.userName.setText(name)
            self.userPass.setText(password)
            self.logIn()
        else:
            self.setCentralWidget(self.begining)

    def logIn(self):
        self.logInError.setVisible(False) #Если была ошибка - скрываем
        login = self.userName.text() #эта штука в QString
        if login in ['admin', 'krutovsky']: #здесь, конечно, будет сетевая часть
            password = 'admin' #по логину будем сравнивать пароли
            if self.userPass.text() == password:
                if self.remeberme.isChecked():
                    with open('user.csv', 'w', newline='') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        spamwriter.writerow(["True"] + [login] + [password])
                else:
                    with open('user.csv', 'w', newline='') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        spamwriter.writerow(["False"] + [""] + [""])
                self.user_id = 0
                #загружаем сет папок и файлов

                #Пока грузит
                first = QLabel()
                dance = QMovie('Icons//loading.gif')
                first.setMovie(dance)
                dance.start()
                self.setCentralWidget(first)
                self.setWindowTitle('Loading')
                self.setWindowIconText(nanachi)
                self.setWindowIcon(QIcon(QPixmap('Icons//Tsu.jpg')))

                if self.check == "False":
                    self.timerScreen = QTimer()
                    self.timerScreen.setInterval(5000)
                    self.timerScreen.start()
                    self.timerScreen.setSingleShot(True)
                    self.timerScreen.timeout.connect(self.mainMission)
                else:
                    self.mainMission()

            else:
                self.logInError.setText("Login and password do not match.")
                self.logInError.setVisible(True)
                self.userPass.setText(None)
        else:
            print("admin\nadmin")
            self.logInError.setVisible(True)
            self.logInError.setText("Login does not exist.")
            self.userPass.setText(None)

    def mainMission(self):
        self.toolbar.setVisible(True)

        self.main_widget = Cloud_Folder()

        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Cloud Folder")
        self.setWindowIcon(QIcon(QPixmap('Icons//mega.jpg')))
        self.setGeometry(300, 300, 600, 300)

    def Download(self):
        if len(self.main_widget.WindowForUserFolders.selectedItems()) != 0 and self.main_widget.ID != None:
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
        with open('user.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["False"] + [""] + [""])
        self.signIn()

    def changeThemeToNormal(self):
        for i in self.listOfActions:
            self.listOfActions[i].setIcon(QIcon('Icons//' + self.listOfNormalIcons[i]))

    def changeThemeToAnime(self):
        for i in self.listOfActions:
            self.listOfActions[i].setIcon(QIcon('Icons//' + self.listOfAnimeIcons[i]))
        self.normal.setIcon(QIcon('Icons//supa.png'))


    def eventFilter(self, obj, event):
        if obj.objectName() == 'ShowListOfDownloads':
            if event.type() == QEvent.Enter:
                x1, y1, x2, y2 = self.geometry().getCoords()
                self.main_widget.WindowForProgBars.move(x2 - 300, y1 + 40) #Тут вроде понятно
                self.main_widget.WindowForProgBars.show()

            if event.type() == QEvent.Leave:
                self.main_widget.WindowForProgBars.hide()

        return QWidget.eventFilter(self, obj, event)
