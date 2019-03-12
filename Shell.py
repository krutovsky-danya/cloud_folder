# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:14:45 2019

@author: Даня
"""

import csv
from PyQt5.QtGui import (QPixmap,
                         QIcon)
from PyQt5.QtWidgets import (QLabel,
                             QVBoxLayout,
                             QPushButton,
                             QWidget,
                             QMainWindow,
                             QFileDialog,
                             QAction,
                             QLineEdit,
                             QRadioButton)

from Cloud_Folder import Cloud_Folder

class Shell(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.begining = QWidget() #Нужны комментарии?
        self.setWindowIcon(QIcon(QPixmap("Icons//hot.jpg")))
        self.setWindowTitle("Try me.")
        with open('user.csv', newline='') as csvfile:
            fresh = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in fresh:
                cheсk, name, password = row
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
        if cheсk == "True":
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
                
                self.main_widget = Cloud_Folder()
                
                self.setCentralWidget(self.main_widget)
                self.setWindowTitle("Cloud Folder")
                self.setWindowIcon(QIcon(QPixmap('Icons//mega.jpg')))
                self.setGeometry(300, 300, 600, 300)
        
                self.ToolBarElements = [['Download.png', 'Download from server', self.Download],
                                        ['Upload.png','Upload to server', self.Upload],
                                        ['Delete.png', 'Delete', self.Delete],
                                        ['Find_someone.png', 'Find_someone', self.Find_someone],
                                        ['sleepy.jpg', 'Log out', self.logOut]]
        
                self.toolbar = self.addToolBar('Commands')
                self.toolbar.setMovable(False)
                
                for path, text, action in self.ToolBarElements:
                    newAction = QAction(QIcon('Icons//' + path), text, self)
                    newAction.triggered.connect(action)
                    self.toolbar.addAction(newAction)
            
            else:
                self.logInError.setText("Login and password do not match.")
                self.logInError.setVisible(True)
                self.userPass.setText(None)
        else:
            print("admin\nadmin")
            self.logInError.setVisible(True)
            self.logInError.setText("Login does not exist.")
            self.userPass.setText(None)
    
    def Download(self):
        if len(self.main_widget.WindowForUserFolders.selectedItems()) != 0 and self.main_widget.ID != None:
            print(self.main_widget.ID)

    def Upload(self):
        print("Upload")
        path = "Lul"
        path = QFileDialog.getOpenFileName(self, "File", "*.*") #возвращает пару путь и еще что-то, непонятно, зачем
        print(path)

    def Delete(self):
        print("Delete")

    def Find_someone(self):
        print("Find_someone")
    
    def logOut(self):
        with open('user.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["False"] + [""] + [""])
        self.close()