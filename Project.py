# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 19:27:10 2019
@author: Даня
"""
import csv
#from PyQt5.QtCore import (QRect, Qt)
from PyQt5.QtGui import (QPixmap,
                         QIcon)
from PyQt5.QtWidgets import (QApplication,
                             QDialog,
                             #QGridLayout,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                             QPushButton,
                             #QTabWidget,
                             QTreeWidget,
                             QTreeWidgetItem,
                             QWidget,
                             QMainWindow,
                             QFileDialog,
                             QAction,
                             QListWidget,
                             QListWidgetItem,
                             #QTreeWidgetItemIterator,
                             QLineEdit,
                             QRadioButton
                             )

nanachi = """
               .             .
              / \           / \
             /   \         / . \
             | .  \       /  . |
             | .   |     |  .. |
             | ..  | _._ |  .. |
              \..  ./   \.  .. |
               \. | xxxxx |  ./
                \/ x ,-. x\__/
             .--/ ,-'ZZZ`-.  \--.
             (  ,'ZZ;ZZ;Z;Z`..  )
             .,'ZZ;; ;; ; ;ZZ `..
           ._###ZZ @  .  @  Z####`
            ````Z._  ~~~  _.Z``\
             _/ ZZ `-----'  Z   \
            ;   ZZ /.....\  Z    \;;
           ;/__ ZZ/..  ...\ Z     \;
          ##'#.\_/.      _.\ZZ     |
          ##....../      |..\Z     |;
         / `-.___/|      |../Z     |
        |    ZZ   |      |./  Z    |;;
       ;|   Z    /x\____/x     Z   |;
       ;\  Z   /xxxxxxxxxxx\   Z __|
        ;\Z  /'##xxxxxxxx###`\__Z .\_
         Z|/#| ####xxxx####  |##\Z ..|
      __Z /#/   ####x####    |###\Z_..|
     /NN\|#|      `###`      \###|NN\..\
     |NN|\#\  _____.......  _/\/ \__/..|
     `-'  `-..###########\_/##/  /.../
            `|#####/   \####|   /../
              .xxx#|   |xxx.   |./
             |x' `x|   |'  `|   -
             `~~~~'    `~~~~'
"""

class Folder():
    def __init__(self, name = None, id = None, parent_id = None):
        self.name = name
        self.id = id
        self.parent_id = parent_id
        self.folders = []
        self.files = []
        self.path = None #Это же все таки путь

    def changeName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def addFile(self, file):
        self.files.append(file)

    def addFolder(self, folder):
        self.folders.append(folder)

    def setPath(self, item):
        self.path = item

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

class QCustomQWidget (QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.textLabel = QLabel()
        self.layout.addWidget(self.textLabel)
        self.setLayout(self.layout)
        self.obj = None
        self.id = None

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

    def setID(self, id):
        self.id = id

    def getID(self):
        return self.id

class Cloud_Folder(QWidget):
    def __init__(self):
        super().__init__()
        
        self.signIn()
        if not self.available:
            pass #здесь нам бы все 3акрыть
        
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

        #Попробуем хранить словарь "имя файла - id файла на сервере", ты вроде был согласен
        self.FilesDataFromServer = {'0': [],
                                    '1': [("It's.txt", 1), ("Hard.pdf", 2)],
                                    '2': [("To.jpg", 3), ("Think up.docx", 4)],
                                    '3': [("File.pptx", 5), ("Names.mp3", 6)],
                                    '4': [("We choose to go.txt", 7), ("To the Moon in this.txt", 8)],
                                    '5': [("Decade and do the.txt", 9), ("Other things, not.txt", 10)],
                                    '6': [("Because they are.txt", 11), ("Easy, but because.txt", 12)],
                                    '7': [("They are hard.txt", 13), ("Because that goal.txt", 14)],
                                    '8': [("Will serve to.txt", 15), ("Organize and measure.txt", 16)],
                                    '9': [("The best of our.txt", 17), ("Energies and skills.txt", 18)]}

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
    
    def signIn(self):   #Для получения логина и пароля
        self.setEnabled(False) #отключает окно, надо бы и ToolBar тоже офнуть...
        self.dialog = QDialog() #Нужны комментарии?
        self.dialog.setWindowIcon(QIcon(QPixmap("Icons//hot.jpg")))
        self.dialog.setWindowTitle("Try me.")
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
        self.dialog.setLayout(layout)
        self.available = False #Если юзер не войдет, то программа закроется
        if cheсk == "True":
            self.userName.setText(name)
            self.userPass.setText(password)
            self.logIn()
        else:
            self.dialog.show()
            self.dialog.exec_()  #так он ждет и не выубается
        self.logInError.setVisible(False)
        self.setEnabled(True)
        #self.parent.toolbar.setEnabled(False)
    
    def logIn(self):
        self.logInError.setVisible(False) #Если была ошибка - скрываем
        login = self.userName.text() #эта штука в QString
        if login in ['admin', 'krutovsky']: #здесь, конечно, будет сетевая часть
            password = 'admin' #по логину будем сравнивать пароли
            if self.userPass.text() == password:
                self.dialog.close()
                self.available = True
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
            else:
                self.logInError.setText("Login and password do not match.")
                self.logInError.setVisible(True)
                self.userPass.setText(None)
        else:
            print("admin\nadmin")
            self.logInError.setVisible(True)
            self.logInError.setText("Login does not exist.")
            self.userPass.setText(None)
            

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Shell()
    win.show()
sys.exit(app.exec_())
