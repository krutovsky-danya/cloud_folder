# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 19:27:10 2019
@author: Даня
"""
#from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import QEvent

#from PyQt5.QtCore import Qt
import time, threading, random
from PyQt5.QtCore import (QThreadPool,
                          QRunnable,
                          pyqtSignal,
                          QObject,
                          QThread,
                          Qt
                          )


from PyQt5.QtWidgets import (QApplication,
                             QDialog,
                             # QGridLayout,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                              QPushButton,
                             # QTabWidget,
                             QTreeWidget,
                             QTreeWidgetItem,
                             QWidget,
                             QMainWindow,
                             # QFileDialog,
                             QAction,
                             QListWidget,
                             QListWidgetItem,
                             # QTreeWidgetItemIterator,
                             qApp,
                             QSizePolicy,
                             QProgressBar
                             )

class Folder():
    def __init__(self, name=None, id=None, parent_id=None):
        self.name = name
        self.id = id
        self.parent_id = parent_id
        self.folders = []
        self.files = []
        self.path = None  # Это же все таки путь

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
'''
class Work(QThread):

    progress_signal = pyqtSignal(list)

    def __init__(self, num, bar):
        super().__init__()
        self.num = num
        self.bar = bar

    def run(self):
        for i in range(1, 101):
            self.progress_signal.emit([self.bar, i])
            time.sleep(random.uniform(0.05, 1))
'''
class Thread_for_dowloading(QThread):

    progress_signal = pyqtSignal(list)

    def __init__(self, ID):
        super().__init__()
        self.ID = ID
        self.percent = 0

    def run(self):
        while self.percent != 100:
            self.percent += 1
            self.progress_signal.emit([self.ID, self.percent])
            time.sleep(1/5)

class QWidgetForBars (QWidget):
    def __init__(self, text, bar):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.textLabel = QLabel()
        self.textLabel.setText(text)
        self.layout.addWidget(self.textLabel)
        self.layout.addWidget(bar)


class Shell(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    '''
    def test_for_threads(self):
        self.threads = []
        self.dialog = QWidget()
        layout = QVBoxLayout(self.dialog)
        #self.pool = QThreadPool()
        for i in range(3):
            newbar = QProgressBar()
            layout.addWidget(newbar)

            work = Work(i, newbar)
            work.progress_signal.connect(self.setProgress)
            self.threads.append(work)
            work.start()
            #self.pool.start(work)

        self.dialog.show()

    def setProgress(self, data):
        bar, num = data
        bar.setValue(num)
    '''
    def update_thing_with_bars(self):
        self.forBars.clear()
        for ID in self.list_of_dowloads:
            myQCustomQWidget = QWidgetForBars(self.list_of_dowloads[ID][0], self.list_of_dowloads[ID][2])
            myQListWidgetItem = QListWidgetItem(self.forBars)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.forBars.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            myQListWidgetItem.setIcon(QIcon(QPixmap('Icons//File.png')))


    def initUI(self):
        self.main_widget = Cloud_Folder()
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Cloud Folder")
        self.setWindowIcon(QIcon(QPixmap('Icons//mega.jpg')))
        self.setGeometry(300, 300, 600, 300)

        self.list_of_dowloads = {}
        self.list_of_dowloadthreads = []

        self.thing_with_bars = QWidget()
        self.forBars = QListWidget()
        layout = QVBoxLayout(self.thing_with_bars)
        layout.addWidget(self.forBars)
        self.thing_with_bars.setWindowFlags(Qt.FramelessWindowHint)

        #self.test_for_threads()
        '''
        self.thread = threading.Thread(target = self.test_for_threads)
        self.thread.start()
        '''
        self.ToolBarElements = [['Download.png', 'Download from server', self.Download],
                                ['Upload.png', 'Upload to server', self.Upload],
                                ['Delete.png', 'Delete', self.Delete],
                                ['Find_someone.png', 'Find_someone', self.Find_someone]]

        self.toolbar = self.addToolBar('Commands')
        self.toolbar.setMovable(False)
        self.toolbar.setObjectName("toolbar")
        for path, text, action in self.ToolBarElements:
            newAction = QAction(QIcon('Icons//' + path), text, self)
            newAction.triggered.connect(action)
            self.toolbar.addAction(newAction)

        self.spacer = QWidget()
        self.spacer.setObjectName("spacer")
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(self.spacer)

        self.Downloads = QPushButton(QIcon("Icons//Downloads.png"),'')
        self.Downloads.setObjectName('Downloads')
        self.Downloads.setFlat(True)
        self.Downloads.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.toolbar.addWidget(self.Downloads)

        qApp.installEventFilter(self)

    def eventFilter(self, obj, event):
        '''
        print(obj.objectName())
        return QWidget.eventFilter(self, obj, event)
        '''
        if obj.objectName() == 'Downloads':
            if event.type() == QEvent.Enter:
                print("Enter")
                self.thing_with_bars.show()

            if event.type() == QEvent.Leave:
                print("Leave")
                self.thing_with_bars.hide()
        return QWidget.eventFilter(self, obj, event)

    def Download(self):
        if (len(self.main_widget.WindowForUserFolders.selectedItems()) != 0
            and self.main_widget.ID != None and self.main_widget.ID not in self.list_of_dowloads):
            print(self.main_widget.ID)
            newbar = QProgressBar()
            self.list_of_dowloads[self.main_widget.ID] = [self.main_widget.currentFileName, 0, newbar]
            print(self.list_of_dowloads)
            self.update_thing_with_bars()

            newthread = Thread_for_dowloading(self.main_widget.ID)
            newthread.progress_signal.connect(self.updateForBars)
            self.list_of_dowloadthreads.append(newthread)
            newthread.start()

    def updateForBars(self, data):
        ID, percent = data
        self.list_of_dowloads[ID][1] = percent
        self.list_of_dowloads[ID][2].setValue(percent)
        if percent == 100:
            del self.list_of_dowloads[ID]
            self.update_thing_with_bars()

    def Upload(self):
        print("Upload")

    def Delete(self):
        print("Delete")

    def Find_someone(self):
        print("Find_someone")
        print(self.list_of_dowloads)


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

        self.user_name = "Danya"
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

        # Попробуем хранить словарь "имя файла - id файла на сервере", ты вроде был согласен
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
            newFolder = Folder(name=name, id=id)
            if parent_id != None:
                self.ListOfUserFolders[parent_id].addFolder(id)
            self.ListOfUserFolders[id] = newFolder

        for parent in self.FilesDataFromServer:
            for file, id in self.FilesDataFromServer[parent]:
                self.ListOfUserFolders[int(parent)].addFile((file, id))

        self.pathToFolders = {}

        self.createUserSide()
        self.createUserFolder()

        # createServerFolders
        # createServerTree

        layout = QHBoxLayout()
        layout.addWidget(self.UserTree)
        layout.addWidget(self.WindowForUserFolders)

        self.setLayout(layout)

    def createUserSide(self):
        self.UserTree = QTreeWidget()
        self.UserTree.header().setVisible(False)
        self.createTree(parent=self.UserTree, obj=self.ListOfUserFolders[0])
        self.UserTree.itemSelectionChanged.connect(self.updateWindow)

    def createTree(self, parent=None, obj=None):
        newFolder = QTreeWidgetItem(parent, [obj.getName()])
        newFolder.setIcon(0, QIcon(QPixmap('Icons//Folder.png')))
        obj.setPath(newFolder)
        self.pathToFolders[str(newFolder)] = obj
        for folder in obj.folders:
            self.createTree(parent=newFolder, obj=self.ListOfUserFolders[folder])

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
        self.currentFileName = file.getText()

    def item_double_clicked(self, item):
        if self.type == "Folder":
            self.UserTree.setCurrentItem(self.obj)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Shell()
    win.show()
sys.exit(app.exec_())
